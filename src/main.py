import os, sys
from shutil import copy, rmtree
from textnode import TextNode
from generatehtml import generate_website

dir_path_static = './static'
dir_path_public = './docs'
template_file = 'template.html'
dir_content = './content'



def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    clean_up_dir(dir_path_public)   
    copy_static_to_public(dir_path_static, dir_path_public)
    generate_website(dir_content, template_file, dir_path_public, basepath)

def copy_static_to_public(sorce_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    contents = os.listdir(sorce_dir_path)

    for item in contents:
        c_path = os.path.join(sorce_dir_path, item)
        p_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(c_path):
            print(f"Copying file: {item}, to {dest_dir_path}")
            copy(c_path, p_path)
        else:
            # Assume this is a directory
            copy_static_to_public(c_path, p_path)

def clean_up_dir(directory):
    if os.path.exists(f"./{directory}"):
        rmtree(f"./{directory}")
        os.mkdir(f"./{directory}")


if __name__ == "__main__":
    main()
