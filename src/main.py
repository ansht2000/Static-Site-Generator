import os
import shutil
from converters import generate_pages_recursive, copy_content

dir_path_static = "./static"
dir_path_public = "./public"

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
    print("Generating content...")
    generate_pages_recursive("./content", "template.html", "./public")

main()