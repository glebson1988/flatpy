# FlatPy - Markdown to HTML Converter

A project for converting markdown to HTML with a well-organized code structure.

## About the Project

FlatPy is a comprehensive markdown to HTML converter that parses markdown text and converts it into structured HTML output. The project is designed with clean architecture principles, separating concerns into logical modules for easy maintenance and extensibility.

The converter handles both inline and block-level markdown elements, providing a complete solution for markdown processing. It uses a node-based approach where markdown text is first parsed into intermediate TextNode and HTMLNode representations before being converted to final HTML output.

## Project Structure

```
src/
├── __init__.py                 # Package initialization
├── main.py                     # Application entry point
├── nodes/                      # Data models
│   ├── __init__.py
│   ├── textnode.py            # TextNode and TextType
│   ├── htmlnode.py            # HTMLNode, LeafNode, ParentNode
│   └── blocknode.py           # BlockType
├── parsers/                    # Parsing logic
│   ├── __init__.py
│   ├── converter.py           # Node conversion and markdown_to_html_node
│   ├── text_parser.py         # Inline element parsing
│   └── block_parser.py        # Block element parsing
└── tests/                      # Tests
    ├── __init__.py
    ├── test_textnode.py       # TextNode tests
    ├── test_htmlnode.py       # HTML node tests
    ├── test_converter.py      # Converter tests (includes markdown_to_html_node)
    ├── test_text_parser.py    # Inline parser tests
    └── test_block_parser.py   # Block parser tests
```

## Functionality

The project supports parsing the following markdown elements:

### Inline elements:
- **Bold text**: \*\*text\*\*
- *Italic text*: \_text\_
- `Code`: \`code\`
- Links: \[text\]\(url\)
- Images: \!\[alt\]\(url\)

### Block elements:
- Headings: \# H1, \#\# H2, etc.
- Code blocks: \`\`\` \`\`\`
- Quotes: \> quote
- Lists: \- item and 1\. item
- Paragraphs

## Usage

### Converting Markdown to HTML:
```python
from src.parsers import markdown_to_html_node

markdown_text = """
# Heading

This is **bold** text with _italic_.

- List item 1
- List item 2
"""

html_node = markdown_to_html_node(markdown_text)
html_output = html_node.to_html()
print(html_output)
```

### Running tests:
```bash
make test
# or
./test.sh
```

### Code quality tools:
```bash
# Code formatting
make format

# Style checking
make lint

# Full check (formatting + linting + tests)
make check

# Help
make help
```

### Running the application:
```bash
python3 -m src.main
```

### Importing functions:
```python
from src.parsers import text_to_textnodes, markdown_to_blocks, markdown_to_html_node
from src.nodes import TextNode, TextType
```

## Code Quality

The project uses modern tools to maintain code quality:

- **Black** - automatic code formatting
- **isort** - import sorting
- **flake8** - linter for code style checking
- **unittest** - testing

All tools are configured to work together and are available through convenient Makefile commands.

## Key Features

1. **Clean architecture**: code organized by functionality with clear separation of concerns
2. **Easy maintenance**: modular design makes the codebase easy to understand and modify
3. **Extensible**: can easily add new markdown elements or output formats
4. **Well tested**: comprehensive test suite with 86+ tests covering all functionality
5. **Code quality**: automatic formatting and code style checking
