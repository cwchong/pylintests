from myplugins.myset import helloworld_checker
from pylint.testutils import CheckerTestCase, MessageTest
from astroid import extract_node


class TestHelloWorldChecker(CheckerTestCase):
    CHECKER_CLASS = helloworld_checker.HelloWorldASTChecker

    # TODO: parameterized test: https://github.com/PyCQA/pylint/blob/main/tests/checkers/unittest_non_ascii_name.py
    def test_finds_home_str(self):
        assign_node = extract_node("""
        a = "Hello, world!"
        """) # AssignNode
        const_node = assign_node.value

        with self.assertAddsMessages(
            MessageTest(
                msg_id="C9001",
                node=const_node,
                # below seems to be autopopulated in normal raising, but not in test
                line=const_node.lineno,
                col_offset=const_node.col_offset,
                end_line=const_node.end_lineno,
                end_col_offset=const_node.end_col_offset,
            ),
        ):
            self.checker.visit_const(const_node)

    # def test_ignores_unique_ints(self):
    #     func_node, return_node_a, return_node_b = astroid.extract_node("""
    #     def test(): #@
    #         if True:
    #             return 1 #@
    #         return 5 #@
    #     """)

    #     with self.assertNoMessages():
    #         self.checker.visit_functiondef(func_node)
    #         self.checker.visit_return(return_node_a)
    #         self.checker.visit_return(return_node_b)