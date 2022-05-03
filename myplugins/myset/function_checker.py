from astroid import nodes
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
from pylint.lint import PyLinter

class FunctionChecker(BaseChecker):
    """
    check blacklisted functions
    """
    __implements__ = IAstroidChecker
    _blacklisted_functions = {
        'random': [
            'randint', 'choice'
        ],
        'urllib.parse': [
            'quote'
        ]
    }
    _import_maps = {}

    name = 'function-checker'
    priority = -1
    msgs = {
        'W9801': (
            'Function check.',
            'function-checker',
            'Avoid using certain functions.',
        ),
    }

    def visit_import(self, node: nodes.Import) -> None:
        """
        visit import
        """
        for name, alias in node.names:
            self._import_maps[alias or name] = name
    
    def visit_importfrom(self, node: nodes.ImportFrom) -> None:
        pass

    def visit_call(self, node: nodes.Call) -> None:
        """
        visit call
        """
        print('kk', self._import_maps)
        # print('>>', node.func) # need to break this into the module and the function
        print('>>', type(node.func)) # ast.nodes.node_classes.Attribute/Name
        if isinstance(node.func, nodes.Attribute):
            func_name = node.func.attrname
            # figures out the root, unaliased import
            mod_name = self._import_maps.get(node.func.expr.name, node.func.expr.name)
            print('xx', func_name, mod_name, node.func.as_string())

            if func_name in self._blacklisted_functions.get(mod_name, []):
                self.add_message('W9801', node=node)
            # THIS also has to take into account aliasing

        elif isinstance(node.func, nodes.Name):
            print('yy', node.func.name, node.func.as_string()) # func() calls
            func_name = node.func.name
            '''
            we need to check the importFrom to match this, as well as check if 
            func has been overridden in-code (might need runtime); non-trivial
            TODO
            '''
            
        # print('>>', node.args)
        # print('>>', node.keywords)
        

def register(linter: "PyLinter") -> None:
    linter.register_checker(FunctionChecker(linter))
