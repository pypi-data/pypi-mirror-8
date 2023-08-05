import os
import os.path as op
import click
from oardocker.utils import check_tarball, check_git, check_url, \
    download_file, git_pull_or_clone, touch
from oardocker.container import Container


def check_images_requirements(ctx, state, nodes, needed_tag, parent_cmd):
    available_images = [', '.join(im["RepoTags"]) for im in
                        ctx.get_images(state)]
    no_missings_images = set()
    needed_images = set(["%s/%s:%s" % (ctx.prefix, node, needed_tag)
                        for node in nodes])
    for image in needed_images:
        for available_image in available_images:
            if image in available_image:
                no_missings_images.add(image)
    missings_images = list(set(needed_images) - set(no_missings_images))
    if missings_images:
        for image in missings_images:
            image_name = click.style(image, fg="red")
            click.echo("missing image '%s'" % image_name)
        raise click.ClickException("You need build base images first with "
                                   "`%s` command" % parent_cmd)


def install(ctx, state, src, needed_tag, tag, message, parent_cmd):
    nodes = ("frontend", "server", "node")
    check_images_requirements(ctx, state, nodes, needed_tag, parent_cmd)
    if not op.exists(ctx.postinstall_dir):
        os.makedirs(ctx.postinstall_dir)
    is_git = False
    is_tarball = False
    is_remote = False
    if op.exists(src):
        src = op.realpath(src)
        is_tarball = check_tarball(src)
        is_git = check_git(src)
    else:
        if src.startswith("git+"):
            src = src[4:]
            is_git = True
            is_remote = True
        elif check_url(src):
            is_remote = True
            is_tarball = True
    if not is_tarball and not is_git:
        raise click.ClickException("Invalid src '%s'. Must be a tarball or a"
                                   " git repository" % src)
    if is_remote:
        ctx.log('Fetching OAR src from %s...' % src)
        if is_git:
            path = op.join(ctx.postinstall_dir, "oar-git")
            git_pull_or_clone(src, path)
        else:
            path = op.join(ctx.postinstall_dir, "oar-tarball.tar.gz")
            download_file(src, path)
    else:
        path = src
    ctx.log('Installing OAR from %s' % src)
    postinstall_cpath = "/tmp/postintall"
    if is_git:
        src_cpath = "%s/oar-git" % postinstall_cpath
    else:
        src_cpath = "%s/tarballs/oar-tarball.tar.gz" % postinstall_cpath
    binds = {path: {'bind': src_cpath, 'ro': True}}
    command = ["/root/install_oar.sh", src_cpath]
    for node in nodes:
        image = "%s/%s:%s" % (ctx.prefix, node, needed_tag)
        name = image.replace("/", "_").replace(":", "_")\
                    .replace("_%s" % needed_tag, "_install")
        container = Container.create(ctx.docker, image=image, name=name,
                                     command=command)
        state["containers"].append(container.short_id)
        container.start_and_attach(binds=binds)
        oar_version = container.logs().strip().split('\n')[-1]
        repository = "%s/%s" % (ctx.prefix, node)
        commit = container.commit(repository=repository, tag=tag,
                                  message=message.format(oar_version))
        ctx.save_image(commit['Id'], tag=tag, repository=repository)
        state["images"].append(commit['Id'])
        container.remove(v=False, link=False, force=True)


def add_dns_entry(ctx, ip_address, hostname):
    with open(ctx.dnsfile, "a+") as dnsfile:
        dnsfile.write("%s %s\n" % (ip_address, hostname))


def log_started(hostname):
    started = click.style("Started", fg="green")
    click.echo("Container %s --> %s" % (hostname, started))


def start_services_container(ctx, state, command, extra_binds):
    touch(ctx.dnsfile)
    image = "%s/services:latest" % ctx.prefix
    hostname = "services"
    name = image.replace("/", "_").replace(":", "_")\
                .replace("_latest", "")
    my_initd = op.join(ctx.envdir, "my_init.d")
    binds = {
        my_initd: {'bind': "/var/lib/container/my_init.d/", 'ro': True},
        ctx.dnsfile: {'bind': "/etc/dnsmasq.d/hosts", 'ro': True},
    }
    binds.update(extra_binds)
    container = Container.create(ctx.docker, image=image, name=name,
                                 detach=True, hostname=hostname, ports=[22],
                                 command=command)
    state["containers"].append(container.short_id)
    container.start(binds=binds, privileged=False, dns="127.0.0.1",
                    volumes_from=None)
    log_started(hostname)
    container.inspect()
    ipaddress = container.dictionary["NetworkSettings"]["IPAddress"]
    add_dns_entry(ctx, ipaddress, hostname)
    return container, ipaddress


def start_server_container(ctx, state, command, extra_binds, dns_ip,
                           num_nodes):
    image = "%s/server:latest" % ctx.prefix
    hostname = "server"
    name = image.replace("/", "_").replace(":", "_")\
                .replace("_latest", "")
    binds = {}
    binds.update(extra_binds)
    env = {"NUM_NODES": num_nodes}
    container = Container.create(ctx.docker, image=image, name=name,
                                 detach=True, hostname=hostname,
                                 environment=env, ports=[22],
                                 command=command)
    state["containers"].append(container.short_id)
    container.start(binds=binds, privileged=True, dns=dns_ip,
                    volumes_from=None)
    log_started(hostname)
    container.inspect()
    ipaddress = container.dictionary["NetworkSettings"]["IPAddress"]
    add_dns_entry(ctx, ipaddress, hostname)
    return container, ipaddress


def start_frontend_container(ctx, state, command, extra_binds, dns_ip,
                             num_nodes, http_port):
    image = "%s/frontend:latest" % ctx.prefix
    hostname = "frontend"
    name = image.replace("/", "_").replace(":", "_")\
                .replace("_latest", "")
    binds = {}
    binds.update(extra_binds)
    env = {"NUM_NODES": num_nodes}
    container = Container.create(ctx.docker, image=image, name=name,
                                 detach=True, hostname=hostname,
                                 environment=env, volumes=["/home"],
                                 ports=[22, 80], command=command)
    state["containers"].append(container.short_id)
    container.start(binds=binds, privileged=True, dns=dns_ip,
                    port_bindings={80: ('127.0.0.1', http_port)},
                    volumes_from=None)
    log_started(hostname)
    container.inspect()
    ipaddress = container.dictionary["NetworkSettings"]["IPAddress"]
    add_dns_entry(ctx, ipaddress, hostname)
    return container, ipaddress


def start_nodes_containers(ctx, state, command, extra_binds, dns_ip,
                           num_nodes, frontend):
    image = "%s/node:latest" % ctx.prefix
    for i in xrange(1, num_nodes + 1):
        hostname = "node%d" % i
        name = image.replace("/", "_").replace(":", "_")\
                    .replace("_latest", "%d" % i)
        binds = {}
        binds.update(extra_binds)
        container = Container.create(ctx.docker, image=image, name=name,
                                     detach=True, hostname=hostname,
                                     ports=[22], command=command)
        state["containers"].append(container.short_id)
        container.start(binds=binds, privileged=True, dns=dns_ip,
                        volumes_from=frontend.id)
        log_started(hostname)
        container.inspect()
        ipaddress = container.dictionary["NetworkSettings"]["IPAddress"]
        add_dns_entry(ctx, ipaddress, hostname)


def deploy(ctx, state, num_nodes, volumes, http_port, needed_tag, parent_cmd):
    command = ["my_init", "taillogs", "--enable-insecure-key"]
    nodes = ("services", "frontend", "server", "node")
    check_images_requirements(ctx, state, nodes, needed_tag, parent_cmd)

    my_initd = op.join(ctx.envdir, "my_init.d")
    extra_binds = {
        my_initd: {'bind': "/var/lib/container/my_init.d/", 'ro': True}
    }
    for volume in volumes:
        host_path, container_path = volume.split(":")
        extra_binds[host_path] = {'bind': container_path, "ro": False}
    _, dns_ip = start_services_container(ctx, state, command, extra_binds)
    start_server_container(ctx, state, command, extra_binds, dns_ip, num_nodes)
    frontend, _ = start_frontend_container(ctx, state, command, extra_binds,
                                           dns_ip, num_nodes, http_port)
    start_nodes_containers(ctx, state, command, extra_binds, dns_ip,
                           num_nodes, frontend)
    generate_ssh_config(ctx, state)


def generate_ssh_config(ctx, state):
    touch(ctx.ssh_config)
    entry = """
Host {}
  HostName {}
"""
    default = """Host *
  User docker
  IdentityFile {}
  UserKnownHostsFile /dev/null
  StrictHostKeyChecking no
  PasswordAuthentication no
  IdentitiesOnly yes
  LogLevel FATAL
  ForwardAgent yes
  Compression yes
  Protocol 2
""".format(ctx.ssh_key)
    key_sort = lambda c: c.dictionary["NetworkSettings"]["IPAddress"]
    with open(ctx.ssh_config, "w") as ssh_config:
        ssh_config.write(default)
        for c in sorted(ctx.get_containers(state), key=key_sort):
            ipaddress = c.dictionary["NetworkSettings"]["IPAddress"]
            hostname = c.dictionary["Config"]["Hostname"]
            ssh_config.write(entry.format(hostname, ipaddress))
