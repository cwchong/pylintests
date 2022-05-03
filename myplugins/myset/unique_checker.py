from astroid import nodes
from typing import TYPE_CHECKING, Optional
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker

if TYPE_CHECKING:
    from pylint.lint import PyLinter


class UniqueReturnChecker(BaseChecker):
    __implements__ = IAstroidChecker

    name = 'unique-returns'
    msgs = {
        'W8001': (
            'Return value is not unique',
            'non-unique-returns',
            'All returns should be unique (ie ur func should not have 2 returns that are the same).',
        )
    }
    options = (
        (
            "ignore-ints",
            {
                "default": False,
                "type": "yn",
                "metavar": "<y or n>",
                "help": "Allow returning non-unique integers",
            },
        ),
    )

    def __init__(self, linter: Optional["PyLinter"] = None) -> None:
        super().__init__(linter)
        self._function_stack = []

    def visit_functiondef(self, node: nodes.FunctionDef) -> None:
        print("enter func", node.name)
        self._function_stack.append([])

    def leave_functiondef(self, node: nodes.FunctionDef) -> None:
        self._function_stack.pop()

    def visit_assign(self, node: nodes.Assign) -> None:
        print(">> assign", node.targets[0].name)
        if isinstance(node.value, nodes.Const):
            print("const value", node.value.value)
        else:
            print(node.value)
        # for BinOp, cant really evaluate since is runtime
        # can include assignattr as well

    
    def visit_call(self, node: nodes.Call) -> None:
        print(">> call", node.func)
        # print(list(node.get_children()))
        children = node.get_children()
        fname = next(children)
        print('name:::', fname)
        print(fname.as_string()) # this ithe code call though
        print(vars(fname).get('attrname')) # this is the attrname/funcname
        print(fname)
        print(type(fname))

        grandchild = list(fname.get_children())
        print(grandchild)
        print(len(grandchild))
        for g in grandchild:
            print(g) # this works, but not grandchild[0]
            print(g.as_string()) # module name, as aliased
        # print(grandchild[0])
        
        fattr = next(children)
        print('attr:::', fattr)


    def visit_return(self, node: nodes.Return) -> None:
        if not isinstance(node.value, nodes.Const):
            print('not const')
            return
        print('current node', node.value.value)
        for other_return in self._function_stack[-1]:
            print('checking')
            if node.value.value == other_return.value.value and not (
                self.config.ignore_ints and node.value.pytype() == int
            ):
                print('failing')
                self.add_message(
                    'non-unique-returns',
                    node=node,
                    # args=(node.value.value,),
                )
            else:
                print('OK', node.value.value, other_return.value.value)

        print('next')
        self._function_stack[-1].append(node)


def register(linter: "PyLinter") -> None:
    linter.register_checker(UniqueReturnChecker(linter))

