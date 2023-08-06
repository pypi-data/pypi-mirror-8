import unittest
from compat.itertools import zip_longest
from pathlib import Path
from vint.ast.plugin.scope_plugin import ScopePlugin, ScopeType, DeclarationScope
from vint.ast.parsing import Parser

FIXTURE_BASE_PATH = Path('test', 'fixture', 'ast')

Fixtures = {
    'DECLARING_FUNC':
        Path(FIXTURE_BASE_PATH, 'fixture_to_scope_plugin_declaring_func.vim'),
    'DECLARING_FUNC_IN_FUNC':
        Path(FIXTURE_BASE_PATH, 'fixture_to_scope_plugin_declaring_func_in_func.vim'),
    'DECLARING_VAR':
        Path(FIXTURE_BASE_PATH, 'fixture_to_scope_plugin_declaring_var.vim'),
    'DECLARING_VAR_IN_FUNC':
        Path(FIXTURE_BASE_PATH, 'fixture_to_scope_plugin_declaring_var_in_func.vim'),
    'FUNC_PARAM':
        Path(FIXTURE_BASE_PATH, 'fixture_to_scope_plugin_func_param.vim'),
    'LOOP_VAR':
        Path(FIXTURE_BASE_PATH, 'fixture_to_scope_plugin_loop_var.vim'),
    'DICT_KEY':
        Path(FIXTURE_BASE_PATH, 'fixture_to_scope_plugin_declaring_with_dict_key.vim'),
}


class TestScopePlugin(unittest.TestCase):
    def assertScopeTree(self, actual_scope, expected_scope):
        """ Asserts the specified scope tree equals to the expected.
        NOTE: expected_scope should not have "parent_scope".
        """
        self.assertIsInstance(actual_scope, dict)
        self.assertIsInstance(expected_scope, dict)

        self.assertIs(actual_scope['type'], expected_scope['type'])
        self.assertEqual(actual_scope['variables'], expected_scope['variables'])

        actual_child_scopes = actual_scope['child_scopes']
        expected_child_scopes = expected_scope['child_scopes']

        self.assertEqual(set(actual_child_scopes.keys()),
                         set(expected_child_scopes.keys()))

        for child_scope_name in expected_child_scopes.keys():
            for actual_child_scope, expected_child_scope in zip_longest(
                    actual_child_scopes[child_scope_name],
                    expected_child_scopes[child_scope_name]):

                self.assertScopeTree(actual_child_scope, expected_child_scope)

                # Check parent_scope is correct.
                self.assertIs(actual_child_scope['parent_scope'], actual_scope)


    def assertProcessing(self, file_path, expected_scope_tree):
        parser = Parser()
        ast = parser.parse_file(file_path)

        plugin = ScopePlugin()
        plugin.process(ast)

        self.assertScopeTree(ast.vint_scope_tree, expected_scope_tree)


    def test_process_with_declaring_var(self):
        expected_scope_tree = {
            'type': ScopeType.TOPLEVEL,
            'variables': {
                'g:explicit_global_var': [{
                    'declaration_scope': DeclarationScope.GLOBAL,
                    'is_declared_with_implicit_scope': False,
                }],
                'b:buffer_local_var': [{
                    'declaration_scope': DeclarationScope.BUFFER_LOCAL,
                    'is_declared_with_implicit_scope': False,
                }],
                'w:window_local_var': [{
                    'declaration_scope': DeclarationScope.WINDOW_LOCAL,
                    'is_declared_with_implicit_scope': False,
                }],
                't:tab_local_var': [{
                    'declaration_scope': DeclarationScope.TAB_LOCAL,
                    'is_declared_with_implicit_scope': False,
                }],
                's:script_local_var': [{
                    'declaration_scope': DeclarationScope.SCRIPT_LOCAL,
                    'is_declared_with_implicit_scope': False,
                }],
                'implicit_global_var': [{
                    'declaration_scope': DeclarationScope.GLOBAL,
                    'is_declared_with_implicit_scope': True,
                }],
                '$ENV_VAR': [{
                    'declaration_scope': DeclarationScope.GLOBAL,
                    'is_declared_with_implicit_scope': False,
                }],
                '@"': [{
                    'declaration_scope': DeclarationScope.GLOBAL,
                    'is_declared_with_implicit_scope': False,
                }],
                '&opt_var': [{
                    'declaration_scope': DeclarationScope.GLOBAL,
                    'is_declared_with_implicit_scope': False,
                }],
            },
            'child_scopes': {},
        }

        self.maxDiff = 4096
        self.assertProcessing(Fixtures['DECLARING_VAR'], expected_scope_tree)


    def test_process_with_declaring_func(self):
        expected_scope_tree = {
            'type': ScopeType.TOPLEVEL,
            'variables': {
                'g:ExplicitGlobalFunc': [{
                    'declaration_scope': DeclarationScope.GLOBAL,
                    'is_declared_with_implicit_scope': False,
                }],
                'b:BufferLocalFunc': [{
                    'declaration_scope': DeclarationScope.BUFFER_LOCAL,
                    'is_declared_with_implicit_scope': False,
                }],
                'w:WindowLocalFunc': [{
                    'declaration_scope': DeclarationScope.WINDOW_LOCAL,
                    'is_declared_with_implicit_scope': False,
                }],
                't:TabLocalFunc': [{
                    'declaration_scope': DeclarationScope.TAB_LOCAL,
                    'is_declared_with_implicit_scope': False,
                }],
                's:ScriptLocalFunc': [{
                    'declaration_scope': DeclarationScope.SCRIPT_LOCAL,
                    'is_declared_with_implicit_scope': False,
                }],
                'ImplicitGlobalFunc': [{
                    'declaration_scope': DeclarationScope.GLOBAL,
                    'is_declared_with_implicit_scope': True,
                }],
            },
            'child_scopes': {
                'g:ExplicitGlobalFunc': [{
                    'type': ScopeType.FUNCTION,
                    'variables': {},
                    'child_scopes': {},
                }],
                'b:BufferLocalFunc': [{
                    'type': ScopeType.FUNCTION,
                    'variables': {},
                    'child_scopes': {},
                }],
                'w:WindowLocalFunc': [{
                    'type': ScopeType.FUNCTION,
                    'variables': {},
                    'child_scopes': {},
                }],
                't:TabLocalFunc': [{
                    'type': ScopeType.FUNCTION,
                    'variables': {},
                    'child_scopes': {},
                }],
                's:ScriptLocalFunc': [{
                    'type': ScopeType.FUNCTION,
                    'variables': {},
                    'child_scopes': {},
                }],
                'ImplicitGlobalFunc': [{
                    'type': ScopeType.FUNCTION,
                    'variables': {},
                    'child_scopes': {},
                }],
            },
        }

        self.maxDiff = 6144
        self.assertProcessing(Fixtures['DECLARING_FUNC'], expected_scope_tree)


    def test_process_with_declaring_var_in_func(self):
        expected_scope_tree = {
            'type': ScopeType.TOPLEVEL,
            'variables': {
                'FuncContext': [{
                    'declaration_scope': DeclarationScope.GLOBAL,
                    'is_declared_with_implicit_scope': True,
                }],
            },
            'child_scopes': {
                'FuncContext': [{
                    'type': ScopeType.FUNCTION,
                    'variables': {
                        'l:explicit_func_local_var': [{
                            'declaration_scope': DeclarationScope.FUNCTION_LOCAL,
                            'is_declared_with_implicit_scope': False,
                        }],
                        'implicit_func_local_var': [{
                            'declaration_scope': DeclarationScope.FUNCTION_LOCAL,
                            'is_declared_with_implicit_scope': True,
                        }],
                    },
                    'child_scopes': {},
                }]
            },
        }

        self.maxDiff = 4096
        self.assertProcessing(Fixtures['DECLARING_VAR_IN_FUNC'], expected_scope_tree)


    def test_process_with_declaring_func_in_func(self):
        expected_scope_tree = {
            'type': ScopeType.TOPLEVEL,
            'variables': {
                'FuncContext': [{
                    'declaration_scope': DeclarationScope.GLOBAL,
                    'is_declared_with_implicit_scope': True,
                }],
            },
            'child_scopes': {
                'FuncContext': [{
                    'type': ScopeType.FUNCTION,
                    'variables': {
                        'l:ExplicitFuncLocalFunc': [{
                            'declaration_scope': DeclarationScope.FUNCTION_LOCAL,
                            'is_declared_with_implicit_scope': False,
                        }],
                        'ImplicitFuncLocalFunc': [{
                            'declaration_scope': DeclarationScope.FUNCTION_LOCAL,
                            'is_declared_with_implicit_scope': True,
                        }],
                    },
                    'child_scopes': {
                        'l:ExplicitFuncLocalFunc': [{
                            'type': ScopeType.FUNCTION,
                            'variables': {},
                            'child_scopes': {},
                        }],
                        'ImplicitFuncLocalFunc': [{
                            'type': ScopeType.FUNCTION,
                            'variables': {},
                            'child_scopes': {},
                        }],
                    },
                }],
            },
        }

        self.maxDiff = 4096
        self.assertProcessing(Fixtures['DECLARING_FUNC_IN_FUNC'], expected_scope_tree)


    def test_process_with_func_param(self):
        expected_scope_tree = {
            'type': ScopeType.TOPLEVEL,
            'variables': {
                'g:FunctionWithNoParams': [{
                    'declaration_scope': DeclarationScope.GLOBAL,
                    'is_declared_with_implicit_scope': False,
                }],
                'g:FunctionWithOneParam': [{
                    'declaration_scope': DeclarationScope.GLOBAL,
                    'is_declared_with_implicit_scope': False,
                }],
                'g:FunctionWithTwoParams': [{
                    'declaration_scope': DeclarationScope.GLOBAL,
                    'is_declared_with_implicit_scope': False,
                }],
                'g:FunctionWithVarParams': [{
                    'declaration_scope': DeclarationScope.GLOBAL,
                    'is_declared_with_implicit_scope': False,
                }],
                'g:FunctionWithParamsAndVarParams': [{
                    'declaration_scope': DeclarationScope.GLOBAL,
                    'is_declared_with_implicit_scope': False,
                }],
                'g:FunctionWithRange': [{
                    'declaration_scope': DeclarationScope.GLOBAL,
                    'is_declared_with_implicit_scope': False,
                }],
            },
            'child_scopes': {
                'g:FunctionWithNoParams': [{
                    'type': ScopeType.FUNCTION,
                    'variables': {},
                    'child_scopes': {},
                }],
                'g:FunctionWithOneParam': [{
                    'type': ScopeType.FUNCTION,
                    'variables': {
                        'a:param1': [{
                            'declaration_scope': DeclarationScope.PARAMETER,
                            'is_declared_with_implicit_scope': False,
                        }],
                    },
                    'child_scopes': {},
                }],
                'g:FunctionWithTwoParams': [{
                    'type': ScopeType.FUNCTION,
                    'variables': {
                        'a:param1': [{
                            'declaration_scope': DeclarationScope.PARAMETER,
                            'is_declared_with_implicit_scope': False,
                        }],
                        'a:param2': [{
                            'declaration_scope': DeclarationScope.PARAMETER,
                            'is_declared_with_implicit_scope': False,
                        }],
                    },
                    'child_scopes': {},
                }],
                'g:FunctionWithVarParams': [{
                    'type': ScopeType.FUNCTION,
                    'variables': {
                        # No tracable parameters
                        # :help a:0
                    },
                    'child_scopes': {},
                }],
                'g:FunctionWithParamsAndVarParams': [{
                    'type': ScopeType.FUNCTION,
                    'variables': {
                        'a:param1': [{
                            'declaration_scope': DeclarationScope.PARAMETER,
                            'is_declared_with_implicit_scope': False,
                        }],
                    },
                    'child_scopes': {},
                }],
                'g:FunctionWithRange': [{
                    'type': ScopeType.FUNCTION,
                    'variables': {
                        'a:firstline': [{
                            'declaration_scope': DeclarationScope.PARAMETER,
                            'is_declared_with_implicit_scope': False,
                        }],
                        'a:lastline': [{
                            'declaration_scope': DeclarationScope.PARAMETER,
                            'is_declared_with_implicit_scope': False,
                        }],
                        'a:param1': [{
                            'declaration_scope': DeclarationScope.PARAMETER,
                            'is_declared_with_implicit_scope': False,
                        }],
                    },
                    'child_scopes': {},
                }],
            },
        }

        self.maxDiff = 4096
        self.assertProcessing(Fixtures['FUNC_PARAM'], expected_scope_tree)


    def test_process_with_loop_var(self):
        expected_scope_tree = {
            'type': ScopeType.TOPLEVEL,
            'variables': {
                'implicit_global_loop_var': [{
                    'declaration_scope': DeclarationScope.GLOBAL,
                    'is_declared_with_implicit_scope': True,
                }],
            },
            'child_scopes': {},
        }

        self.maxDiff = 1024
        self.assertProcessing(Fixtures['LOOP_VAR'], expected_scope_tree)


    def test_process_with_declaring_with_dict_key(self):
        expected_scope_tree = {
            'type': ScopeType.TOPLEVEL,
            'variables': {
                'g:dict["Function1"]': [{
                    'declaration_scope': DeclarationScope.GLOBAL,
                    'is_declared_with_implicit_scope': False,
                }],
                'g:dict["Function2"]': [{
                    'declaration_scope': DeclarationScope.GLOBAL,
                    'is_declared_with_implicit_scope': False,
                }],
                'g:dict["key1"]': [{
                    'declaration_scope': DeclarationScope.GLOBAL,
                    'is_declared_with_implicit_scope': False,
                }],
                'g:dict["key2"]': [{
                    'declaration_scope': DeclarationScope.GLOBAL,
                    'is_declared_with_implicit_scope': False,
                }],
            },
            'child_scopes': {
                'g:dict["Function1"]': [{
                    'type': ScopeType.FUNCTION,
                    'variables': {},
                    'child_scopes': {},
                }],
                'g:dict["Function2"]': [{
                    'type': ScopeType.FUNCTION,
                    'variables': {},
                    'child_scopes': {},
                }],
            },
        }

        self.maxDiff = 1024
        self.assertProcessing(Fixtures['DICT_KEY'], expected_scope_tree)


if __name__ == '__main__':
    unittest.main()
