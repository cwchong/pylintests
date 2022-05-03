from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
from pylint.lint import PyLinter

class VersionChecker(BaseChecker):
    '''
    Checks for min version used
    1. no emitting of errors, just log
    2. emit warning if min version is not met
        need a way to compare string versions (how does pip check?):
            packaging.version.parse
    '''
    __implements__ = IAstroidChecker
    _libraries = [
        ('dali', '0.1.0'),
        ('maia', '0.1.0'),
        ('sklearn', '1.1.0'), # this should flag
        ('mlflow', '1.14.1.4'),
    ]

    name = 'version-checker'
    priority = -1
    msgs = {
        'W9901': (
            'Version check.',
            'version-checker',
            'Avoid using old versions.',
        ),
    }

    def visit_import(self, node):
        print('visited import', node.names)
        # introspect version statically? possible?
        # cos even if run pkg_resources.get_distribution('construct').version
        # this is the version on current pylint run env, not the target
        # venv for the job
        # thus can only check prescence/absence of module in code
        # but still useful in order to map the module name for use
        # in checking function call (unless visit_func can tell us the module name)

    def visit_importfrom(self, node):
        print('visited importfrom', node.names)


def register(linter: "PyLinter") -> None:
    linter.register_checker(VersionChecker(linter))
