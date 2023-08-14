from __future__ import annotations

import itertools
import os
import shutil

from comma.utils.command import Command
from comma.utils.ftypes import CMD_ARGS
from comma.utils.machine.machine import Machine
from comma.utils.persistent_cache import sqlite_cache


@sqlite_cache(minutes=20)
def all_git_projects() -> list[str]:
    return [
        os.path.dirname(x)
        for x in Command(
            cmd=(
                'find',
                os.path.expanduser('~/dev'), os.path.expanduser('~/worktrees'), os.path.expanduser('~/projects'),
                '-mindepth', '2',
                '-maxdepth', '3',
                '-name', '.git',
                '-prune',
                # '-exec', 'dirname', '{}', ';',
            ),
        ).quick_run().splitlines()
    ]


class LocalMachine(Machine):
    def create_cmd(self, cmd: CMD_ARGS) -> Command:
        return Command(cmd=cmd)

    def is_dir(self, path: str) -> bool:
        return os.path.isdir(path)

    def code_open(self, path: str) -> None:
        Command(cmd=('code', self.full_path(path))).execvp()

    def has_executable(self, executable: str) -> bool:
        return shutil.which(executable) is not None

    def full_path(self, path: str) -> str:
        return os.path.realpath(path)

    def project_list(self) -> list[str]:
        projects = os.path.expanduser('~/projects')
        foo = (os.path.join(projects, x) for x in os.listdir(projects))
        return list(
            {
                x
                for x in itertools.chain(foo, all_git_projects())
                if 'trash' not in x and os.path.isdir(x)
            },
        )