import os
import os.path as op
import sys
import click
import docker
import json
from functools import update_wrapper
from oardocker.utils import copy_tree
from oardocker.container import Container
from sh import chmod


HERE = op.dirname(__file__)
CONTEXT_SETTINGS = dict(auto_envvar_prefix='oardocker')


class Context(object):

    def __init__(self):
        self.version = '0.1'
        self._docker_client = None
        self.prefix = "oardocker"
        self.current_dir = os.getcwd()
        self.workdir = self.current_dir
        self.templates_dir = op.abspath(op.join(HERE, 'templates'))
        self.docker_host = None
        # oar archive url
        self.oar_website = "http://oar-ftp.imag.fr/oar/2.5/sources/stable"
        self.oar_tarball = "%s/oar-2.5.3.tar.gz" % self.oar_website

    def update(self):
        self.envdir = op.join(self.workdir, ".%s" % self.prefix)
        self.ssh_key = op.join(self.envdir, "images", "base", "config",
                               "insecure_key")
        self.ssh_config = op.join(self.envdir, "ssh_config")
        self.dnsfile = op.join(self.envdir, "dnsmasq.d", "hosts")
        self.postinstall_dir = op.join(self.envdir, "postinstall")
        self.envid_file = op.join(self.envdir, "envid")
        self.state_file = op.join(self.envdir, "state.json")

    def assert_valid_env(self):
        if not os.path.isdir(self.envdir):
            raise click.ClickException("Missing oardocker env directory."
                                       " Run `oardocker init` to create"
                                       " a new oardocker environment")

    def copy_tree(self, src, dest, overwrite=False):
        if os.path.exists(dest) and not overwrite:
            raise click.ClickException("File exists : '%s'" % dest)
        copy_tree(src, dest)
        chmod("600", self.ssh_key)

    def log(self, msg, *args):
        """Logs a message to stderr."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stderr)

    def vlog(self, msg, *args):
        """Logs a message to stderr only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)

    def save_state(self, state):
        if op.isdir(op.dirname(self.state_file)):
            with open(self.state_file, "w+") as json_file:
                state["images"] = list(set(state["images"]))
                state["containers"] = list(set(state["containers"]))
                json_file.write(json.dumps(state))

    def load_state(self):
        state = {"images": [], "containers": []}
        if op.isfile(self.state_file):
            try:
                with open(self.state_file) as json_file:
                    state = json.loads(json_file.read())
                    images = set([im[:12] for im in state["images"]])
                    state["images"] = list(images)
                    containers = set([c[:12] for c in state["containers"]])
                    state["containers"] = list(containers)
            except:
                pass
        return state

    def get_containers(self, state):
        containers = self.docker.containers(quiet=False, all=True, trunc=False,
                                            latest=False)
        for container in containers:
            if not container["Id"][:12] in state["containers"]:
                continue
            yield Container.from_id(self.docker, container["Id"])

    def get_containers_ids(self, state):
        for container in self.get_containers(state):
            yield container.short_id

    def get_images_ids(self, state):
        for image in self.get_images(state):
            yield image["Id"][:12]

    def get_images(self, state):
        images = self.docker.images(name=None, quiet=False,
                                    all=False, viz=False)
        for image in images:
            if not image["Id"][:12] in state["images"]:
                continue
            yield image

    def remove_image(self, image, force=True):
        image_name = ', '.join(image["RepoTags"])
        image_id = image["Id"]
        self.docker.remove_image(image_id, force=force)
        removed = click.style("Removed", fg="blue")
        self.log("Image %s (%s) --> %s" % (image_id, image_name, removed))

    def save_image(self, image_id, repository, tag):
        saved = click.style("Saved", fg="green")
        image_name = "%s:%s" % (repository, tag)
        self.docker.tag(image_id, repository=repository, tag=tag, force=True)
        self.log("Image %s (%s) --> %s" % (image_id, image_name, saved))

    @property
    def docker(self):
        if self._docker_client is None:
            self._docker_client = docker.Client(base_url=self.docker_host,
                                                timeout=10)
        return self._docker_client


pass_context = click.make_pass_decorator(Context, ensure=True)
cmd_folder = op.abspath(op.join(HERE, 'commands'))


class oardockerCLI(click.MultiCommand):

    def list_commands(self, ctx):
        commands = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith('.py') and filename.startswith('cmd_'):
                commands.append(filename[4:-3])
        commands.sort()
        return commands

    def get_command(self, ctx, name):
        if sys.version_info[0] == 2:
            name = name.encode('ascii', 'replace')
        if name in self.list_commands(ctx):
            mod = __import__('oardocker.commands.cmd_' + name,
                             None, None, ['cli'])
            return mod.cli


def pass_state(f):
    @click.pass_context
    def new_func(ctx, *args, **kwargs):
        ctx.obj.assert_valid_env()
        state = ctx.obj.load_state()
        state["containers"] = list(ctx.obj.get_containers_ids(state))
        state["images"] = list(ctx.obj.get_images_ids(state))
        try:
            return ctx.invoke(f, state, *args, **kwargs)
        finally:
            ctx.obj.save_state(state)

    return update_wrapper(new_func, f)


def invoke_after_stop(f):
    @click.pass_context
    def new_func(ctx, *args, **kwargs):
        stop_cmd = ctx.parent.command.get_command(ctx, "stop")
        ctx.invoke(stop_cmd)
        return ctx.invoke(f, *args, **kwargs)

    return update_wrapper(new_func, f)


def invoke_before_clean(f):
    @click.pass_context
    def new_func(ctx, *args, **kwargs):
        try:
            return ctx.invoke(f, *args, **kwargs)
        finally:
            clean_cmd = ctx.parent.command.get_command(ctx, "clean")
            click.echo("Cleanup...")
            ctx.invoke(clean_cmd)

    return update_wrapper(new_func, f)


@click.command(cls=oardockerCLI, context_settings=CONTEXT_SETTINGS, chain=True)
@click.option('--workdir', type=click.Path(exists=True, file_okay=False,
                                           resolve_path=True),
              help='Changes the folder to operate on.')
@click.option('--docker-host', default="unix://var/run/docker.sock")
@click.version_option()
@pass_context
def cli(ctx, workdir, docker_host):
    """Manage a small OAR developpement cluster with docker."""
    if workdir is not None:
        ctx.workdir = workdir
    if docker_host is not None:
        ctx.docker_host = docker_host
    ctx.update()


def main(*arg, **kwargs):
    try:
        cli(*arg, **kwargs)
    except Exception as e:
        sys.stderr.write("\nError: %s\n" % e)
        sys.exit(1)
