from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from comma.utils.command import Command
from comma.utils.find_command import FindCommand
from comma.utils.ftypes import CMD_ARGS


class Machine(ABC):
    @abstractmethod
    def create_cmd(self, cmd: CMD_ARGS) -> Command:
        ...

    @abstractmethod
    def code_open(self, path: str) -> None:
        ...

    def has_executable(self, executable: str) -> bool:
        return self.create_cmd(('which', executable)).run().returncode == 0

    def quick_run(self, cmd: CMD_ARGS) -> str:
        return self.create_cmd(cmd=cmd).run().stdout.strip()

    def is_dir(self, path: str) -> bool:
        return self.create_cmd(cmd=('test', '-d', path)).run().returncode == 0

    def fqdn(self) -> str:
        return self.quick_run(('hostname',))

    def is_local(self) -> bool:
        from comma.utils.machine.local_machine import LocalMachine
        return self.__class__ == LocalMachine

    def get_file_list(self, find_cmd: FindCommand) -> str:
        return self.quick_run(cmd=find_cmd.cmd())

    def project_list(self) -> list[str]:
        return self.get_file_list(
            FindCommand(
                paths=('~/projects',),
                maxdepth=1,
                mindepth=1,
                expand_paths=self.is_local(),
            ),
        ).splitlines()

    def full_path(self, path: str) -> str:
        return self.quick_run(('realpath', path))
