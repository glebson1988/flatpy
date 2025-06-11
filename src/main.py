import os
import shutil

from src.nodes import TextNode, TextType


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


def main():
    copy_static_to_public()

    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)


if __name__ == "__main__":
    main()
