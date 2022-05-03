from .unique_checker import UniqueReturnChecker
from .helloworld_checker import HelloWorldASTChecker
from .localpath_checker import LocalPathChecker
from .version_checker import VersionChecker
from .function_checker import FunctionChecker
from pylint.lint import PyLinter

def register(linter: "PyLinter") -> None:
    linter.register_checker(UniqueReturnChecker(linter))
    linter.register_checker(HelloWorldASTChecker(linter))
    linter.register_checker(LocalPathChecker(linter))
    linter.register_checker(VersionChecker(linter))
    linter.register_checker(FunctionChecker(linter))