from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
from pylint.lint import PyLinter

class HelloWorldASTChecker(BaseChecker):
    __implements__ = IAstroidChecker

    name = 'hello-world-ast'
    priority = -1
    msgs = {
        'C9001': (
            'Uses a "Hello, world!" string.',
            'hello-world',
            'No code should use "Hello, world!" statements.',
        ),
    }

    def visit_const(self, node):
        if node.value == "Hello, world!":
            self.add_message(
                'C9001', node=node)
        else:
            pass
            # print('nope: ', node.value)
            # means not good enough, since concat is missed out
            # need combined string or function args instead


def register(linter: "PyLinter") -> None:
    linter.register_checker(HelloWorldASTChecker(linter))
