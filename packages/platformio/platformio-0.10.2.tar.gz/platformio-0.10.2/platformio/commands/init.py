# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

from os import getcwd, makedirs
from os.path import isdir, isfile, join
from shutil import copyfile

import click

from platformio import app
from platformio.exception import ProjectInitialized, UnknownBoard
from platformio.util import get_boards, get_source_dir


@click.command("init", short_help="Initialize new PlatformIO based project")
@click.option("--project-dir", "-d", default=getcwd(),
              type=click.Path(exists=True, file_okay=False, dir_okay=True,
                              writable=True, resolve_path=True))
@click.option("--board", "-b", multiple=True, metavar="TYPE")
@click.option("--disable-auto-uploading", is_flag=True)
def cli(project_dir, board, disable_auto_uploading):

    project_file = join(project_dir, "platformio.ini")
    src_dir = join(project_dir, "src")
    lib_dir = join(project_dir, "lib")
    if all([isfile(project_file), isdir(src_dir), isdir(lib_dir)]):
        raise ProjectInitialized()

    builtin_boards = set(get_boards().keys())
    if board and not set(board).issubset(builtin_boards):
        raise UnknownBoard(", ".join(set(board).difference(builtin_boards)))

    if project_dir == getcwd():
        click.secho("The current working directory", fg="yellow", nl=False)
        click.secho(" %s " % project_dir, fg="cyan", nl=False)
        click.secho(
            "will be used for the new project.\n"
            "You can specify another project directory via\n"
            "`platformio init -d %PATH_TO_THE_PROJECT_DIR%` command.\n",
            fg="yellow"
        )

    click.echo("The next files/directories will be created in %s" %
               click.style(project_dir, fg="cyan"))
    click.echo("%s - Project Configuration File" %
               click.style("platformio.ini", fg="cyan"))
    click.echo("%s - a source directory. Put your source code here" %
               click.style("src", fg="cyan"))
    click.echo("%s - a directory for the project specific libraries" %
               click.style("lib", fg="cyan"))

    if (not app.get_setting("enable_prompts") or
            click.confirm("Do you want to continue?")):
        for d in (src_dir, lib_dir):
            if not isdir(d):
                makedirs(d)
        if not isfile(project_file):
            copyfile(join(get_source_dir(), "projectconftpl.ini"),
                     project_file)
            if board:
                fill_project_envs(project_file, board, disable_auto_uploading)
        click.secho(
            "Project has been successfully initialized!\n"
            "Now you can process it with `platformio run` command.",
            fg="green"
        )
    else:
        click.secho("Aborted by user", fg="red")


def fill_project_envs(project_file, board_types, disable_auto_uploading):
    builtin_boards = get_boards()
    content = []
    for type_ in board_types:
        if type_ not in builtin_boards:
            continue
        else:
            content.append("")

        data = builtin_boards[type_]
        framework = data.get("build", {}).get("core", None)
        if framework in ("msp430", "lm4f"):
            framework = "energia"

        content.append("[env:autogen_%s]" % type_)
        content.append("platform = %s" % data['platform'])

        if framework:
            content.append("framework = %s" % framework)
        content.append("board = %s" % type_)

        content.append("%stargets = upload" % ("# " if disable_auto_uploading
                                               else ""))

    with open(project_file, "a") as f:
        f.write("\n".join(content))
