#!/usr/bin/python3.11
# -*- coding: utf-8 -*-
"""
----------------------------------------------------
Title:      patch_creator.py
License:    agpl-3.0
Author:     Samuel Carlson
Created on: 2023-09-18
----------------------------------------------------

Description: Input filenames to merge.

----------------------------------------------------

Arguments: 
-i (--input_dir)      - Provide custom input dir containing pdfs to merge.
-o (--output_dir)     - Provide custom output dir to place merged pdfs.
-f (--output_file)    - Provide custom output filename to place merged pdfs.

----------------------------------------------------

Notes:
How the VENV was made:
virtualenv -p python3.11 venv/py3.11

How to run this script:
cd /mnt/f/Documents/Personal/Scripts/
source /mnt/f/Documents/Personal/Scripts/python_patch_creator/activate
python patch_creator.py --clone --destination /bin/tool-patch/10.1-a --source /bin/tool-base/10.1
----------------------------------------------------
"""
# Imports
from typing import Union    # Globally required, used for function type hints.
from pathlib import Path    # Globally required, used for type hints
import logging              # For logging of debug, info, warning, errors
import sys                  # Needed for logging
import code                 # Interactive debug
import argparse             # Needed for args

# Setup logging
log_fh = logging.FileHandler(filename="patch_creator.log")
stdout_handler = logging.StreamHandler(stream=sys.stdout)
handlers = [log_fh, stdout_handler]
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    #format='[%(asctime)s] %(levelname)s: %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S', 
    #datefmt='%d-%b-%y %H:%M:%S', 
    handlers=handlers
)


def make_symlinks(source_path : Path, dest_path: Path):
    """
    Only run for patch flow. Not for clone flow.
    Creates symlinks from the PATCH dir (the untarred tar.gz (.tgz)) into the 10.1-a dir.
    Only run this after 10.1-a is created.
    source_path should be the untarred dir in PATCH
    dest_path should be the 10.1-a dir (created by clone flow).
    If dir doesn't exist, create it.
    If symlink already exists, overwrite it.
    If symlink doesn't exist, create it.
    """
    
    
def hierarchy_creator(source_path : Path, dest_path: Path):
    """
    Only run for clone flow. Not for patch flow.
    Creates real directories, symlinks to all files in those dirs in preparation for overwrite by PATCH flow.
    If file is of type dir, create dir at destination
    If file is of type file, ensure parent exists at destination, if so, create symlink at dest, else create parent then symlink file
    Repeat similar steps but for patch flow, overwriting existing symlinks (and possibly creating new symlinks to non-existent dirs in original install from PATCH dir)
    """
    Path.is_dir
    Path.is_file
    Path.is_symlink
    # To get all paths in a list, in order, recursively
    filepath_list = sorted(source_path.rglob("*")
    # To get the relative path do:
    # relative_path = source_path_test.relative_to(source_path)
    for filepath in filepath_list:
        if filepath.is_dir:
            filepath.mkdir(parents=True, exist_ok=True)
        elif filepath.is_file or filepath.is_symlink:
            # Get the relative path
            relative_path = filepath.relative_to(source_path)
            new_symlink_path = Path(dest_path, relative_path)
            # TODO: Not tested
            # I think this needs to be dest_path+relative_path
            if not new_symlink_path.parent.exists():
                new_symlink_path.mkdir(parents=True, exist_ok=True)
            # Do this after we are sure that the dir exists.
            new_symlink_path.symlink_to(filepath)
            

def get_posix_path(user_filepath : Union[str,Path]) -> Path:
    """
    Function to convert user provided 'path' to POSIX Path type
    """
    try:
        posix_path = Path(user_filepath)
    except Exception as err:
        logging.error(f"The path provided ({user_filepath}) could not be made into a POSIX Path, please check path and try again.")
        raise SystemExit("Both flows were enabled, which cannot happen. Please choose either clone or patch.")
    return posix_path
    
    
def verify_path(filepath : Path):
    """
    Verify the path exists.
    If path doesn't exist, ensure parent exists.
    If parent doesn't exist then prompt if user wants to make path.
    Else, if parent does exist, make path automatically
    """
    if not filepath.exists():
        logging.debug(f"{filepath} doesn't exist.")
        # If the parent doesn't exist, and also we can't create /bin/tool-base dirs so ignore any path with that.
        if not filepath.parent.exists() and Path("/bin/tool-base") not in filepath:
            logging.debug(f"{filepath} parent dir doesn't exist, either.")
            create_dir = input(f"Provided path {filepath} doesn't exist, and neither does the parent dir, would you like this script to mkdir -p {filepath}? (y/n)").lower().strip() == "y"
                if create_dir = "y":
                    filepath.mkdir(parents=True, exist_ok=True)
                else:
                    error_msg = f"Please update filepath for source and/or destination. Current path {filepath} is not usable so exiting script."
                    logging.error(f"{error_msg}")
                    raise SystemExit(f"{error_msg}")

    
def patch_creator(user_flow_clone : bool, user_flow_patch : bool, user_source_path : Union[Path, str], user_dest_path[Path, str]):
    """
    Function to handle user options and create the patch.
    """
    # 1. test to ensure only one true x
    # 2. test to ensure paths exist 
    # 3. if path doesn't exist, ensure parent exists, if parent doesn't exist then prompt if user wants to make path, if parent does exist, make path
    # 4. discover all files in source, keep in list
    # if file is of type dir, create dir at destination
    # if file is of type file, ensure parent exists at destination, if so, create symlink at dest, else create parent then symlink file
    # Repeat similar steps but for patch flow, overwriting existing symlinks (and possibly creating new symlinks to non-existent dirs in original install from PATCH dir)
    source_path = get_posix_path(user_source_path)
    dest_path   = get_posix_path(user_dest_path)
        
    verify_path(source_path)
    verify_path(dest_path)
    
    if user_flow_clone and user_flow_patch:
        raise SystemExit("Both flows were enabled, which cannot happen. Please choose either clone or patch.")
    # For making 10.1-a from existing 10.1 install.
    elif user_flow_clone:
        hierarchy_creator(source_path, dest_path)
    # For the patch flow - IE creating links from the PATCH dir (the untarred tar.gz (.tgz)) into the 10.1-a dir.
    elif user_flow_patch:
        make_symlinks(source_path, dest_path)
    else:
        raise SystemExit("Neither flow was enabled, quitting. Please choose either clone or patch.")
    
def get_basepath_info() -> tuple[str, str]:
    """
    __file__ doesn't exist if this script is called from interactive session. Work around that with except clause.
    """
    try:
        filepath = Path(__file__).resolve()
        basepath = filepath.parent
    # Best effort, if no __file__ then assume pwd
    except NameError:
        basepath = Path.cwd()
        filepath = Path(basepath, "patch_creator.py")
    return (basepath, filepath)
    
    
def main():
    """
    Main to setup args and call patch_creator function
    """
    parser = argparse.ArgumentParser(description="Used to pass in custom args to pdfmerge script.")
    optional_args = parser.add_argument_group("Optional Arguments")
    required_args = parser.add_argument_group("Required Arguments")
    mutex_args    = parser.add_mutually_exclusive_group(required=True)
    
    mutex_args.add_argument("-c", "--clone",
                            action=store_true,
                            help="Use clone option to specify that you want to create a clone of IT's tool-base install using symlinks.")
    mutex_args.add_argument("-p", "--patch",
                            action=store_true,
                            help="Use patch option to specify that you want to update existing clone dir with vendor patch (overlay) symlinks.")
    required_args.add_argument("-s", "--source", 
                            required=True,
                            action="store",
                            help="Source directory to link to.")
    required_args.add_argument("-d", "--destination", 
                            required=True,
                            action="store",
                            help="Destination directory to link to.")
    optional_args.add_argument("--debug", 
                               required=False, 
                               action=store_true,
                               help="Run script in debug mode.")
    args = parser.parse_args()
    
    debug_mode      = args.debug
    logging.info(f"{debug_mode = }")
    if debug_mode:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.info("Debug prints are enabled.")
    else:
        logging.getLogger().setLevel(logging.INFO)
        logging.info("Debug prints are disabled.")
        
    # Assign possible arg appropriately, uses default if arg not used.
    user_flow_clone     = args.clone
    user_flow_patch     = args.patch
    user_source_path    = args.source
    user_dest_path      = args.destination

    patch_creator(user_flow_clone, user_flow_patch, user_source_path, user_dest_path)


if __name__ == "__main__":
    main()