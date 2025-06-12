import os
import shutil

from src.nodes import TextNode, TextType
from src.parsers import extract_title, markdown_to_html_node


def copy_file(source_path, dest_path):
    with open(source_path, "rb") as source_file:
        with open(dest_path, "wb") as dest_file:
            while True:
                chunk = source_file.read(8192)
                if not chunk:
                    break
                dest_file.write(chunk)


def copy_static_to_public(source_dir="static", dest_dir="public"):
    print(f"Starting copy from {source_dir} to {dest_dir}")

    if os.path.exists(dest_dir):
        print(f"Removing existing directory: {dest_dir}")
        shutil.rmtree(dest_dir)

    print(f"Creating directory: {dest_dir}")
    os.mkdir(dest_dir)

    if not os.path.exists(source_dir):
        print(f"Warning: source directory {source_dir} not found")
        return

    copy_directory_contents(source_dir, dest_dir)
    print("Copy completed!")


def copy_directory_contents(source_dir, dest_dir):
    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isfile(source_path):
            print(f"Copying file: {source_path} -> {dest_path}")
            copy_file(source_path, dest_path)
        else:
            print(f"Creating directory: {dest_path}")
            os.mkdir(dest_path)
            copy_directory_contents(source_path, dest_path)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read markdown file
    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    # Read template file
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    # Extract title
    title = extract_title(markdown_content)

    # Replace placeholders in template
    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)

    # Create destination directory if it doesn't exist
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Write final HTML to destination
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(final_html)


def main():
    # Delete everything in public directory
    if os.path.exists("public"):
        shutil.rmtree("public")

    # Copy static files to public
    copy_static_to_public()

    # Generate page from content/index.md
    generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()
