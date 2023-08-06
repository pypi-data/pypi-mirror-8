from __future__ import unicode_literals
from lib2to3.fixer_base import BaseFix
from .utils import find_indentation
from lib2to3.pgen2 import token
from lib2to3.pytree import Node, Leaf
from lib2to3.pygram import python_symbols as symbols


class FixImportsOnSeparateLines(BaseFix):
    '''
    Imports should usually be on separate lines.
    '''

    def match(self, node):
        if (node.type == symbols.simple_stmt and
            node.children[0].type == symbols.import_name and
            node.children[0].children[1].type == symbols.dotted_as_names):
            return node.children[0].children[1].children
        return False

    def transform(self, node, results):
        child_imports = [leaf.value for leaf in results if leaf.type == token.
            NAME]
        current_indentation = find_indentation(node)
        new_nodes = []
        for index, module_name in enumerate(child_imports):
            new_prefix = current_indentation
            if not index:
                # Keep the prefix, if this is the first import name
                new_prefix = node.prefix
            new_nodes.append(Node(symbols.simple_stmt, [Node(symbols.
                import_name, [Leaf(token.NAME, 'import', prefix=new_prefix),
                Leaf(token.NAME, module_name, prefix=" ")]), Leaf(token.
                NEWLINE, '\n')]))

        node.replace(new_nodes)
        node.changed()
