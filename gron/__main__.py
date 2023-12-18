#!/usr/bin/env python3
from __future__ import annotations

import json
from typing import Sequence

from gron import gron
from gron import ungron
from simple_argparser import CLIApp


class Gron(CLIApp):
    """Gron is a command line tool that makes JSON greppable."""
    COMMAND_NAME = 'gron'
    ARG_HELP = {
        'file': 'File to read from. Defaults to stdin.',
        'ungron': 'Ungron the input.',
    }
    file: str = '/dev/stdin'
    ungron: bool = False

    @classmethod
    def run(cls, argv: Sequence[str] | None = None) -> int:
        args = cls.parse_args(argv)
        if args.ungron:
            with open(args.file) as f:
                print(
                    json.dumps(
                        ungron(f),
                        indent=2,
                        sort_keys=True,
                    ),
                )
            return 0
        else:
            with open(args.file) as f:
                for line in gron(json.load(f)):
                    print(line)
            return 0


if __name__ == '__main__':
    # prog = f'python3 -m {__package__}' if __package__ and not sys.argv[0].endswith('__main_.py') else None
    # CLIApp.main(prog=prog)
    Gron.run()