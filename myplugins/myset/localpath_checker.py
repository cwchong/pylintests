from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
from pylint.lint import PyLinter
import re

class LocalPathChecker(BaseChecker):
    __implements__ = IAstroidChecker
    _blacklists = [
        re.compile(r'/(home|cdsw)(/.*)?$'),
        # prob not great, but it's a start
        # might need optional prefix / or start of string
    ]

    name = 'local-path-checker'
    priority = -1
    msgs = {
        'W9001': (
            'Uses a local path.',
            'local-path',
            'Avoid using local paths.',
        ),
    }

    def visit_const(self, node):
        if isinstance(node.value, str) and any(map(lambda x: re.search(x, node.value), self._blacklists)):
            self.add_message('W9001', node=node)


def register(linter: "PyLinter") -> None:
    linter.register_checker(LocalPathChecker(linter))
