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
    _import_module_maps = {} # aliased module mapping to original module (import)
    # e.g. import urllib.parse as ps; import sklearn as sk; 
    # { 'ps': 'urllib.parse', 'sk': 'sklearn' }
    _import_function_module_maps = {} # aliased function or function mapping to module (importfrom)
    # e.g. from random import randint, from urllib.parse import quote as qt;
    # { 'randint': 'random', 'qt': 'urllib.parse' }
    # still missing a qt -> quote mapping
    _import_function_maps = {}

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
        print('import')
        for name, alias in node.names:
            self._import_module_maps[alias or name] = name
    
    def visit_importfrom(self, node: nodes.ImportFrom) -> None:
        print('importfrom')
        print('aa>>', node.names)
        print('aa>>', node.modname)
        '''
        need to resolve the importFrom to the module name
        e.g. from random import randint
        >> randint function needs to scope to random module (assuming no override)
        e.g. from urllib.parse import quote
        >> quote function needs to scope to urllib.parse module (assuming no override)
        e.g. from urllib.parse import quote as qt
        >> qt needs to resolve to quote (import_map), then scoped to urllib.parse

        '''
        for name, alias in node.names:
            self._import_function_maps[alias or name] = name
            self._import_function_module_maps[name] = node.modname
        # whenever encounter randint call directly, lookup this to get the module name
        # then use the module name to get blacklist
        # TODO: unscope if a function def override? need to acct for class scoping!
        


    def visit_call(self, node: nodes.Call) -> None:
        """
        visit call
        """
        print('kk', self._import_module_maps)
        # print('>>', node.func) # need to break this into the module and the function
        # print('>>', type(node.func)) # ast.nodes.node_classes.Attribute/Name
        if isinstance(node.func, nodes.Attribute):
            func_name = node.func.attrname
            # figures out the root, unaliased import
            mod_name = self._import_module_maps.get(node.func.expr.name, node.func.expr.name)
            
            if func_name in self._blacklisted_functions.get(mod_name, []):
                self.add_message('W9801', node=node)
                print('FAIL', func_name, mod_name, '='*80)
            print('>>>>', func_name, mod_name, node.func.as_string())
            # THIS also has to take into account aliasing TODO

        elif isinstance(node.func, nodes.Name):
            # print('yy', node.func.name, node.func.as_string()) # func() calls
            func_name = self._import_function_maps.get(node.func.name, node.func.name)
            mod_name = self._import_function_module_maps.get(func_name)
            if func_name in self._blacklisted_functions.get(mod_name, []):
                self.add_message('W9801', node=node)
                print('FAIL', func_name, mod_name, '*'*80)
            print('>>>>', func_name, mod_name)
            '''
            we need to check the importFrom to match this, as well as check if 
            func has been overridden in-code (might need runtime); non-trivial
            TODO
            '''
            

            
        # print('>>', node.args)
        # print('>>', node.keywords)
        

def register(linter: "PyLinter") -> None:
    linter.register_checker(FunctionChecker(linter))
