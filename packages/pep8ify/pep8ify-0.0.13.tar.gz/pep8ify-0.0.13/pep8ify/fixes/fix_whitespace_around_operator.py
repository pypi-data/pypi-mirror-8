from __future__ import unicode_literals
from lib2to3.fixer_base import BaseFix
from lib2to3.pgen2 import token
from lib2to3.pygram import python_symbols as symbols
from lib2to3.pytree import Leaf

from .utils import OPERATORS, UNARY_OPERATORS

ARG_SYMBOLS = [symbols.arglist, symbols.varargslist, symbols.typedargslist]
KEYWORKD_ARG_SYMBOLS = [symbols.argument, symbols.arglist, symbols.
    typedargslist]


class FixWhitespaceAroundOperator(BaseFix):
    '''
    Avoid extraneous whitespace in the following situations:

    - More than one space around an assignment (or other) operator to
      align it with another.
    '''

    def match(self, node):
        if isinstance(node, Leaf) and node.value in OPERATORS:
            return True
        return False

    def transform(self, node, results):
        # Allow unary operators: -123, -x, +1.
        if (node.value in UNARY_OPERATORS and node.parent.type == symbols.
            factor):
            self.rstrip(node)
        # Allow argument unpacking: foo(*args, **kwargs).
        elif(node.value in ['*', '**'] and node.parent.type in ARG_SYMBOLS
            and (not node.prev_sibling or node.prev_sibling.type == token.
            COMMA)):
            self.rstrip(node)
        # Allow keyword assignment: foobar(foo=bar)
        elif node.value == '=' and node.parent.type in KEYWORKD_ARG_SYMBOLS:
            self.no_spaces(node)
        # Finally check if the spacing actually needs fixing
        elif(node.prefix != " " or node.get_suffix() != " "):
            self.spaces(node)

    def rstrip(self, node):
        next_sibling = node.next_sibling
        next_sibling_new_prefix = next_sibling.prefix.lstrip(' \t')
        if next_sibling.prefix != next_sibling_new_prefix:
            next_sibling.prefix = next_sibling_new_prefix
            next_sibling.changed()

    def no_spaces(self, node):
        if node.prefix != "":
            node.prefix = ""
            node.changed()

        next_sibling = node.next_sibling
        next_sibling_new_prefix = next_sibling.prefix.lstrip(' \t')
        if next_sibling.prefix != next_sibling_new_prefix:
            next_sibling.prefix = next_sibling_new_prefix
            next_sibling.changed()

    def spaces(self, node):
        if not node.prefix.count('\n'):
            # If there are newlines in the prefix, this is a continued line,
            # don't strip anything
            new_prefix = " %s" % node.prefix.lstrip(' \t')
            if node.prefix != new_prefix:
                node.prefix = new_prefix
                node.changed()

        next_sibling = node.next_sibling
        if not next_sibling:
            return
        if next_sibling.prefix.count('\n'):
            next_sibling_new_prefix = next_sibling.prefix.lstrip(' \t')
            if next_sibling_new_prefix[0:1] == '\\':
                # Insert a space before a backslash ending line
                next_sibling_new_prefix = " %s" % next_sibling_new_prefix
        else:
            next_sibling_new_prefix = " %s" % next_sibling.prefix.lstrip(
                ' \t')
        if next_sibling.prefix != next_sibling_new_prefix:
            next_sibling.prefix = next_sibling_new_prefix
            next_sibling.changed()
