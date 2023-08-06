'''
This module performs a few early syntax check on the input AST.
It checks the conformance of the input code to Pythran specific
constraints.
'''

import pythran.tables as tables
from pythran.intrinsic import Class

import ast


class PythranSyntaxError(SyntaxError):
    def __init__(self, msg, node=None):
        SyntaxError.__init__(self, msg)
        if node:
            self.lineno = node.lineno
            self.offset = node.col_offset


class SyntaxChecker(ast.NodeVisitor):
    '''
    Visit an AST and raise a PythranSyntaxError upon unsupported construct.

    Attributes
    ----------
    attributes : {str}
        Possible attributes from Pythonic modules/submodules.
    '''

    def __init__(self):
        """ Gather attributes from tables.modules content. """
        self.attributes = set()

        def save_attribute(module):
            """ Recursively save Pythonic keywords as possible attributes. """
            self.attributes.update(module.iterkeys())
            for signature in module.itervalues():
                if isinstance(signature, dict):
                    save_attribute(signature)
                elif isinstance(signature, Class):
                    save_attribute(signature.fields)

        for module in tables.modules.itervalues():
            save_attribute(module)

    def visit_Module(self, node):
        err = ("Top level statements can only be strings, functions, comments"
               " or imports")
        for n in node.body:
            if isinstance(n, ast.Expr) and isinstance(n.value, ast.Str):
                continue
            else:
                if not any(isinstance(n, getattr(ast, t))
                           for t in ('FunctionDef', 'Import', 'ImportFrom',)):
                    raise PythranSyntaxError(err, n)
        self.generic_visit(node)

    def visit_Interactive(self, node):
        raise PythranSyntaxError("Interactive session not supported", node)

    def visit_Expression(self, node):
        raise PythranSyntaxError("Interactive expressions not supported", node)

    def visit_Suite(self, node):
        raise PythranSyntaxError(
            "Suites are specific to Jython and not supported", node)

    def visit_ClassDef(self, node):
        raise PythranSyntaxError("Classes not supported")

    def visit_Print(self, node):
        self.generic_visit(node)
        if node.dest:
            raise PythranSyntaxError(
                "Printing to a specific stream not supported", node.dest)

    def visit_With(self, node):
        raise PythranSyntaxError("With statements not supported")

    def visit_Call(self, node):
        self.generic_visit(node)
        if node.starargs:
            raise PythranSyntaxError("Call with star arguments not supported",
                                     node)
        if node.kwargs:
            raise PythranSyntaxError("Call with kwargs not supported", node)

    def visit_FunctionDef(self, node):
        self.generic_visit(node)
        if node.args.vararg:
            raise PythranSyntaxError("Varargs not supported", node)
        if node.args.kwarg:
            raise PythranSyntaxError("Keyword arguments not supported",
                                     node)

    def visit_Raise(self, node):
        self.generic_visit(node)
        if node.tback:
            raise PythranSyntaxError(
                "Traceback in raise statements not supported",
                node)

    def visit_Attribute(self, node):
        self.generic_visit(node)
        if node.attr not in self.attributes:
            raise PythranSyntaxError(
                "Attribute '{0}' unknown".format(node.attr),
                node)

    def visit_Import(self, node):
        """ Check if imported module exists in tables.modules. """
        for alias in node.names:
            current_module = tables.modules
            # Recursive check for submodules
            for path in alias.name.split('.'):
                if path not in current_module:
                    raise PythranSyntaxError(
                        "Module '{0}' unknown.".format(alias.name),
                        node)
                else:
                    current_module = current_module[path]

    def visit_ImportFrom(self, node):
        """
            Check validity of imported functions.

            Check:
                - no level specific value are provided.
                - a module is provided
                - module/submodule exists in tables.modules
                - imported function exists in the given module/submodule
        """
        if node.level != 0:
            raise PythranSyntaxError("Specifying a level in an import", node)
        if not node.module:
            raise PythranSyntaxError("import from without module", node)
        module = node.module
        current_module = tables.modules
        # Check if module exists
        for path in module.split('.'):
            if path not in current_module:
                raise PythranSyntaxError(
                    "Module '{0}' unknown.".format(module),
                    node)
            else:
                current_module = current_module[path]

        # Check if imported functions exist
        for alias in node.names:
            if alias.name == '*':
                continue
            elif alias.name not in current_module:
                raise PythranSyntaxError(
                    "identifier '{0}' not found in module '{1}'".format(
                        alias.name,
                        module),
                    node)

    def visit_Exec(self, node):
        raise PythranSyntaxError("Exec statement not supported", node)

    def visit_Global(self, node):
        raise PythranSyntaxError("Global variables not supported", node)


def check_syntax(node):
    '''Does nothing but raising PythranSyntaxError when needed'''
    SyntaxChecker().visit(node)
