from __future__ import unicode_literals
from lib2to3.fixer_base import BaseFix
from .utils import find_indentation
from lib2to3.pgen2 import token
from lib2to3.pygram import python_symbols as symbols
from lib2to3.pytree import Node, Leaf


NL = Leaf(token.NEWLINE, '\n')

class FixCompoundStatements(BaseFix):
    """
    Compound statements (multiple statements on the same line) are
    generally discouraged.

    While sometimes it's okay to put an if/for/while with a small body
    on the same line, never do this for multi-clause statements. Also
    avoid folding such long lines!
    """

    def match(self, node):
        results = {}
        if (node.prev_sibling and isinstance(node.prev_sibling, Leaf) and node.
            prev_sibling.type == token.COLON and node.type != symbols.suite):
            # If it's inside a lambda definition, subscript, or sliceop, leave
            # it alone
            # symbols.trailer
            if node.parent.type in [symbols.lambdef, symbols.subscript,
                symbols.sliceop, symbols.dictsetmaker, symbols.trailer]:
                pass
            else:
                results["colon"] = True
        if (node.type == symbols.simple_stmt and Leaf(token.SEMI, ';') in node
            .children):
            results["semi"] = True
        return results

    def transform(self, node, results):
        if results.get("colon"):
            node = self.transform_colon(node)
        if results.get("semi"):
            node = self.transform_semi(node)

    def transform_colon(self, node):
        node_copy = node.clone()
        # Strip any whitespace that could have been there
        node_copy.prefix = node_copy.prefix.lstrip()
        old_depth = find_indentation(node)
        new_indent = '%s%s' % ((' ' * 4), old_depth)
        new_node = Node(symbols.suite, [Leaf(token.NEWLINE, '\n'), Leaf(token
            .INDENT, new_indent), node_copy, Leaf(token.DEDENT, '')])
        node.replace(new_node)
        node.changed()

        # Replace node with new_node in case semi
        return node_copy

    def transform_semi(self, node):
        for child in node.children:
            if child.type == token.SEMI:
                next_sibling = child.next_sibling
                # If the next sibling is a NL, this is a trailing semicolon;
                # simply remove it and the NL's prefix
                if next_sibling == NL:
                    child.remove()
                    continue

                # Strip any whitespace from the next sibling
                prefix = next_sibling.prefix
                stripped_prefix = prefix.lstrip()
                if prefix != stripped_prefix:
                    next_sibling.prefix = stripped_prefix
                    next_sibling.changed()
                # Replace the semi with a newline
                old_depth = find_indentation(child)

                child.replace([Leaf(token.NEWLINE, '\n'),
                               Leaf(token.INDENT, old_depth)])
                child.changed()
        return node
