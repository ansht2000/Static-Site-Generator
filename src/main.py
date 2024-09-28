import os
import shutil
from converters import generate_page

dir_path_static = "./static"
dir_path_public = "./public"

def copy_content(src_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
    for filename in os.listdir(src_dir_path):
        from_path = os.path.join(src_dir_path, filename)
        to_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {to_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, to_path)
        else:
            copy_content(from_path, to_path)

def main():
    if not os.path.exists(dir_path_static):
        raise ValueError("Static content could not be loaded: no static directory")
    if not os.path.exists(dir_path_public):
        os.mkdir(dir_path_public)
    print("Deleting public directory...")
    if len(os.listdir(dir_path_public)) != 0:
        shutil.rmtree(dir_path_public)
        os.mkdir(dir_path_public)
    print("Copying static files to public directory...")
    copy_content(dir_path_static, dir_path_public)
    generate_page("./content/index.md", "template.html", "./public/index.html")

main()