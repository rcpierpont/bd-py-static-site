import os,shutil,sys
from fileutils import copy_files_recursive,generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"

def main():
    basepath = '/' if len(sys.argv) == 1 else sys.argv[1]
    
    print('basepath: ' + basepath)
    
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)
    print("Generating pages...")
    generate_pages_recursive(basepath, dir_path_content, template_path, dir_path_public)


main()