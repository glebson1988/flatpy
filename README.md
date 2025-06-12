# FlatPy - Static Site Generator

A simple and efficient static site generator in Python that converts markdown files into a complete website.

## About the Project

FlatPy is a static site generator that transforms your markdown files into a beautiful website. The project reads markdown content from the `content/` folder, applies HTML templates, and generates a ready-to-use static website in the `docs/` folder.

Key features:
- 📝 **Markdown support** - full markdown syntax for content
- 🎨 **HTML templates** - customizable templates for page styling
- 🗂️ **Directory structure** - automatic navigation creation from folder structure
- 📱 **Static resources** - copying CSS, images, and other files
- 🔄 **Recursive generation** - support for nested directories and blogs
- 🌐 **GitHub Pages ready** - configurable basepath for deployment

## Project Structure

```
├── src/                        # Source code of the generator
│   ├── main.py                 # Main file - site generation
│   ├── nodes/                  # Data models
│   │   ├── textnode.py         # TextNode and TextType
│   │   ├── htmlnode.py         # HTMLNode, LeafNode, ParentNode
│   │   └── blocknode.py        # BlockType for block elements
│   ├── parsers/                # Markdown parsers
│   │   ├── converter.py        # HTML conversion
│   │   ├── text_parser.py      # Inline element parsing
│   │   └── block_parser.py     # Block element parsing
│   └── tests/                  # Tests
├── content/                    # Markdown content of the site
│   ├── index.md               # Home page
│   ├── blog/                  # Blog
│   └── contact/               # Contact information
├── static/                     # Static files
│   ├── index.css              # CSS styles
│   └── images/                # Images
├── docs/                       # Generated site (output for GitHub Pages)
├── template.html              # HTML template for pages
├── main.sh                    # Local development script
└── build.sh                   # Production build script
```

## Supported Markdown Elements

### Inline elements:
- **Bold text**: `**text**`
- *Italic*: `*text*`
- `Code`: `` `code` ``
- Links: `[text](url)`
- Images: `![alt](url)`

### Block elements:
- Headings: `# H1`, `## H2`, `### H3`, etc.
- Code blocks: ``` ``` ```
- Quotes: `> quote`
- Lists: `- item` and `1. item`
- Paragraphs

## Usage

### Local Development:
```bash
# Run for local development (default basepath "/")
./main.sh

# Or directly via Python
python3 -m src.main
```

### Production Build for GitHub Pages:
```bash
# Build for GitHub Pages deployment
./build.sh

# This runs: python3 -m src.main "/flatpy/"
```

### Custom Basepath:
```bash
# Build with custom basepath
python3 -m src.main "/custom-path/"
```

### Content structure:
Place your markdown files in the `content/` folder:
```
content/
├── index.md           # Home page
├── about.md          # About page
└── blog/             # Blog
    ├── post1.md      # First post
    └── post2.md      # Second post
```

### HTML template:
Edit `template.html` to change the design:
```html
<!doctype html>
<html>
  <head>
    <title>{{ Title }}</title>
    <link href="/index.css" rel="stylesheet" />
  </head>
  <body>
    <article>{{ Content }}</article>
  </body>
</html>
```

### Static files:
Place CSS, images, and other static files in the `static/` folder. They will be copied to `docs/` during generation.

## GitHub Pages Deployment

This project is configured for easy deployment to GitHub Pages:

1. **Build the site**:
   ```bash
   ./build.sh
   ```

2. **Commit and push**:
   ```bash
   git add .
   git commit -m "Deploy site"
   git push origin main
   ```

3. **Configure GitHub Pages**:
   - Go to your repository settings
   - Navigate to Pages section
   - Set source to "Deploy from a branch"
   - Select "main" branch and "/docs" folder
   - Save settings

4. **Access your site**:
   Your site will be available at: `https://USERNAME.github.io/REPO_NAME/`

The `build.sh` script automatically configures all paths for GitHub Pages deployment, ensuring CSS, images, and internal links work correctly with the `/flatpy/` basepath.

## Development Commands

```bash
# Code formatting
make format

# Code style checking
make lint

# Run tests
make test

# Full check (formatting + linting + tests)
make check

# Help
make help
```

## Code Usage Example

```python
from src.parsers import markdown_to_html_node, extract_title

# Convert markdown to HTML
markdown_text = """
# Heading

This is **bold** text with *italic*.

- List item 1
- List item 2
"""

html_node = markdown_to_html_node(markdown_text)
html_output = html_node.to_html()

# Extract title
title = extract_title(markdown_text)
```

## Code Quality Tools

The project uses modern tools to maintain code quality:

- **Black** — automatic code formatting
- **isort** — import sorting
- **flake8** — code style checking
- **unittest** — testing

All tools are configured to work together and are available through convenient Makefile commands.

## Architecture Features

1. **Clean architecture**: code organized by functionality with clear separation of concerns
2. **Modularity**: easily understandable and modifiable code
3. **Extensibility**: can easily add new markdown elements or output formats
4. **Well tested**: comprehensive test suite covers all functionality
5. **Code quality**: automatic formatting and style checking
6. **Deployment ready**: built-in support for GitHub Pages and other static hosts

## Result

After running the generator, a ready-to-use static website will appear in the `docs/` folder, which can be deployed on any web server or static site hosting (GitHub Pages, Netlify, Vercel, etc.).
