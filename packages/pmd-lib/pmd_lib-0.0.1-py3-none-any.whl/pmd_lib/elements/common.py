from typing import List, Union
from ..core import Node


class Text(Node):
    def __init__(self, text: str, break_at_points: bool = True, **kwargs) -> None:
        super().__init__(ending_linebreak=1, **kwargs)
        self.break_at_points = break_at_points
        self.nodes.append(text)

    def compile(self):
        md_string = super().compile()
        if self.break_at_points:
            md_string = md_string.replace('. ', '.\n')
        return md_string


class Headline(Node):
    def __init__(self, title: str, level: int = 1) -> None:
        super().__init__(enforce_inline=True, beginning_linebreak=1, ending_linebreak=2)
        level = max(1, min(level, 6))  # Ensure level is between 1 and 6
        self.nodes = ['#' * level, ' ', title]


class Paragraph(Node):
    def __init__(self, nodes: Union[List[Node], None] = None) -> None:
        super().__init__(nodes=nodes, ending_linebreak=2)


class Wrap(Node):
    def __init__(self, content: Union[str, Node], wrap_symbol: str, strip_space=True, **kwargs) -> None:
        if isinstance(content, list):
            nodes = content
        else:
            nodes = [content]
        super().__init__(nodes=nodes, **kwargs)

        self.wrap_symbol = wrap_symbol
        self.strip_space = strip_space

    def compile(self):
        compiled_content = super().compile()
        if self.strip_space:
            compiled_content = compiled_content.strip(' ')
        wrapped_content = f"{self.wrap_symbol}{compiled_content}{self.wrap_symbol}"
        if self.enforce_inline:
            return wrapped_content
        else:
            return wrapped_content + '\n'


class Italics(Wrap):
    def __init__(self, content: Union[str, Node], **kwargs) -> None:
        super().__init__(Wrap(content, wrap_symbol='*', enforce_inline=True), wrap_symbol=' ', enforce_inline=True,
                         **kwargs)


class Bold(Wrap):
    def __init__(self, content: Union[str, Node], **kwargs) -> None:
        super().__init__(Wrap(content, wrap_symbol='**', enforce_inline=True), wrap_symbol=' ', enforce_inline=True,
                         **kwargs)


class Strikethrough(Wrap):
    def __init__(self, content: Union[str, Node], **kwargs) -> None:
        super().__init__(Wrap(content, wrap_symbol='~~', enforce_inline=True), wrap_symbol=' ', enforce_inline=True,
                         **kwargs)


class Blockquote(Node):
    def __init__(self, content: Union[str, Node], **kwargs) -> None:
        super().__init__(enforce_inline=False, **kwargs)
        if isinstance(content, Node):
            self.nodes.append(content)
        elif isinstance(content, str):
            # Ensuring there is a blank line before and after the blockquote
            self.nodes.append(Text(content))
            # self.nodes.append('\n'.join(['> ' + line for line in content.splitlines()]))
        else:
            raise TypeError('Blockquote content must be a string or a Node.')

    def compile(self):
        content_string = super().compile()
        md_string = ''
        for line in content_string.splitlines():
            md_string += f'> {line}\n'
        return '\n' + md_string + '\n'


class ListItem(Node):
    def __init__(self, content: Union[str, Node], ordered: bool = False, task: bool = False, is_checked: bool = False,
                 index: int = 0) -> None:
        super().__init__()
        self.content = content
        self.ordered = ordered
        self.task = task
        self.is_checked = is_checked
        self.index = index

    def compile(self):
        # Compile the content here if it's a Node
        compiled_content = self.content.compile() if isinstance(self.content, Node) else self.content
        compiled_content = compiled_content.replace('\n', '')
        if self.task:
            checkbox = "[x]" if self.is_checked else "[ ]"
            prefix = f"- {checkbox} "
        elif self.ordered:
            prefix = f"{self.index + 1}. "
        else:
            prefix = "- "
        return f"{prefix}{compiled_content}\n"


class MarkdownList(Node):
    def __init__(self, items: List[Union[str, Node]], ordered: bool = False, task: bool = False, **kwargs) -> None:
        super().__init__(**kwargs, beginning_linebreak=1, ending_linebreak=1)
        self.ordered = ordered
        self.task = task  # New attribute to indicate a task list
        for index, item in enumerate(items):
            if isinstance(item, tuple) and self.task:
                # If task list, expect a tuple (content, is_checked)
                content, is_checked = item
                list_item = ListItem(content=content, ordered=ordered, task=task, is_checked=is_checked, index=index)
            else:
                # If not a task list, the item is just the content
                list_item = ListItem(content=item, ordered=ordered, task=task, index=index)
            self.nodes.append(list_item)


class Code(Wrap):
    def __init__(self, content: str, **kwargs) -> None:
        # Inline code in standard Markdown is wrapped in backticks
        super().__init__(content=content, wrap_symbol='`', enforce_inline=True, **kwargs)


class CodeBlock(Wrap):
    def __init__(self, code: Union[str, List] = [], **kwargs) -> None:
        super().__init__(content=code, wrap_symbol='```',
                         beginning_linebreak=1, ending_linebreak=1, node_separator='\n', **kwargs)


class Referencable(Node):
    def __init__(self, alt_text: str, url: str = '', reference: str = '', is_image: bool = False, **kwargs):
        super().__init__(**kwargs)
        self.alt_text = alt_text
        self.url = url
        self.reference = reference
        self.is_image = is_image

    def compile(self):
        # Select the appropriate prefix ('!' for images, empty for links)
        prefix = '!' if self.is_image else ''
        # Construct reference or URL part
        link_part = f'[{self.reference}]' if self.reference else f'({self.url})'
        return f"{prefix}[{self.alt_text}]{link_part}\n"


class Link(Referencable):
    def __init__(self, alt_text: str, path: str = '', reference: str = '', **kwargs):
        super().__init__(alt_text, path, reference, is_image=False, **kwargs)


class Image(Referencable):
    def __init__(self, alt_text: str, path: str = '', reference: str = '', **kwargs):
        super().__init__(alt_text, path, reference, is_image=True, **kwargs)


class Reference(Node):
    def __init__(self, reference: str, path: str, **kwargs):
        super().__init__(**kwargs)
        self.reference = reference
        self.path = path

    def compile(self):
        super().compile()
        return f"\n[{self.reference}]: {self.path}\n"


class ReferenceManager(Node):
    def __init__(self) -> None:
        super().__init__()
        self.references = {}
        self.counter = 0

    def get_id(self, url: str, title: str = "") -> str:
        # Automatically generate a reference key based on a counter to ensure uniqueness
        ref_key = f"ref{self.counter}"
        self.counter += 1

        # Add the URL and title if provided to the references dictionary
        self.references[ref_key] = (url, title) if title else url

        # Return the generated reference key
        return ref_key

    def new_link(self, text: str, url: str, title: str = "", inline=True) -> str:
        # Use get_id to create a reference key for the link
        ref_key = self.get_id(url, title)
        # Return the formatted link using the reference key
        return f"[{text}][{ref_key}]" + ('' if inline else '\n')

    def new_image(self, alt_text: str, path: str, title: str = "") -> str:
        # Use get_id to create a reference key for the image
        ref_key = self.get_id(path, title)
        # Return the formatted image using the reference key
        return f"![{alt_text}][{ref_key}]\n"

    def compile(self) -> str:
        # Compile all references into the Markdown reference format
        compiled_references = "\n"
        for ref_key, ref_info in self.references.items():
            if isinstance(ref_info, tuple):
                # If a title is provided, format it as a reference with a title (used for images)
                url, title = ref_info
                compiled_references += f"[{ref_key}]: {url} \"{title}\"\n"
            else:
                # If no title, format it as a simple link reference
                compiled_references += f"[{ref_key}]: {ref_info}\n"
        return compiled_references


class Line(Node):

    def __init__(self):
        pass

    def compile(self):
        return '\n---\n'


class Table(Node):

    def __init__(self, header=None, rows=None, alignment=None):
        super().__init__()
        self.header = [] if header is None else header
        self.nodes = [] if rows is None else rows
        self.alignment = [] if alignment is None else alignment

    def _check_dimensions(self):
        pass

    def compile(self):
        def row_string(entries, column_sizes):
            return '{:<{}}'.join(['|' for i in range(len(entries) + 1)]).format(
                *[item for pair in zip(entries, column_sizes) for item in pair])

        alignment_map = {'<': (1, 0), '^': (1, 1), '>': (0, 1)}
        self.header = [element.compile() if isinstance(element, Node) else str(element) for element in self.header]
        self.nodes = [[element.compile() if isinstance(element, Node) else str(element) for element in row]
                      for row in self.nodes]
        table = []
        table.append(self.header)
        table = table + self.nodes
        column_sizes = [max(len(item)+1 for item in row) for row in zip(*table)]
        md_string = '\n'
        if len(self.header) > 0:
            md_string += row_string(self.header, column_sizes)
            md_string += '\n'
            if len(self.alignment) > 0:
                seperators = [(':' * alignment_map[self.alignment[i]][0] +
                               '-' * (column_sizes[i] - sum(alignment_map[self.alignment[i]])) +
                               ':' * alignment_map[self.alignment[i]][1]) for i in range(len(column_sizes))]
            else:
                seperators = [(':' + '-' * (column_sizes[i] - 2) + ':') for i in range(len(column_sizes))]
            md_string += row_string(seperators, column_sizes)
            md_string += '\n'
            for row in self.nodes:
                md_string += row_string(row, column_sizes)
                md_string += '\n'
        return md_string + '\n'

    def __add__(self, other: Union['Node', str, List]) -> 'Node':
        if isinstance(other, Node) or isinstance(other, str) or isinstance(other, List):
            self.nodes.append(other)
        else:
            raise TypeError('Expected node to inherit Node, or be of type str.')
        return self