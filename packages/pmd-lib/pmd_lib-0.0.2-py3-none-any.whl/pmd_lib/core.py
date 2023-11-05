import warnings
from typing import List, Union
from elements import *


class Node:
    def __init__(self, enforce_inline: bool = False,
                 beginning_linebreak: int = 0, ending_linebreak: int = 0,
                 nodes: Union[List['Node'], None] = None, node_separator: str = '') -> None:
        self.nodes = [] if nodes is None else nodes
        self.enforce_inline = enforce_inline
        self.ending_linebreak = ending_linebreak
        self.beginning_linebreak = beginning_linebreak
        self.node_separator = node_separator

    def compile(self):
        md_string = ''
        n_nodes = len(self.nodes)
        for i, node in enumerate(self.nodes):
            if isinstance(node, str):
                node_string = node
            else:
                node_string = node.compile()
            if self.enforce_inline and '\n' in node_string:
                warnings.warn('Node was set to enforce inline, but received a multi-line string during compilation.'
                              'Linebreaks will be removed to continue.')
                node_string = node_string.replace('\n', ' ')
            md_string += node_string + (self.node_separator if i < n_nodes - 1 else '')
        if self.ending_linebreak > 0:
            md_string += '\n' * self.ending_linebreak
        if self.beginning_linebreak > 0:
            md_string = '\n' * self.beginning_linebreak + md_string
        return md_string

    def __add__(self, other: Union['Node', str]) -> 'Node':
        if isinstance(other, Node) or isinstance(other, str):
            self.nodes.append(other)
        else:
            raise TypeError('Expected node to inherit Node, or be of type str.')
        return self

    def __radd__(self, other: str) -> 'Node':
        if isinstance(other, str):
            return (Node(enforce_inline=self.enforce_inline) + other) + self
        else:
            raise TypeError('Expected other to be of type str. Got {} instead'.format(str(type(other))))


class Document(Node):
    def __init__(self, nodes: Union[List[Node], None] = None) -> None:
        super().__init__(nodes=nodes)

    def save(self, filename):
        with open(filename, 'w') as f:
            f.write(self.compile())



