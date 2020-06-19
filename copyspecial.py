#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Copyspecial Assignment"""

# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# give credits
__author__ = "Iris Hoffmeyer, https://stackoverflow.com/a/47185863"

import re
import os
import sys
import shutil
import subprocess
import argparse


def get_special_paths(dirname):
    """Given a dirname, returns a list of all its special files."""
    special_files = []
    with os.scandir(dirname) as files:
        regex = re.compile(r"__(\w*)__")
        for f in files:
            special_file = regex.search(f.name)
            if f.is_file() and special_file is not None:
                special_files.append(os.path.abspath(f.path))
    return special_files


def copy_to(path_list, dest_dir):
    """Given a list of file paths, copy each file to dest_dir path"""
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    for f in path_list:
        shutil.copy(f, dest_dir)
    return


def zip_to(path_list, dest_zip):
    """Given a list of file paths, creates a zip file using the name provided
    in dest_zip"""
    args = ['zip', '-j', dest_zip]
    args.extend(path_list)
    args_string = ' '.join(args)
    print(f"Command I'm going to do:  \n{args_string}\n")
    try:
        subprocess.run(args, check=True, capture_output=True)
    except subprocess.CalledProcessError as err:
        print(err.output.decode())
        sys.exit(err.returncode)
    return


def main(args):
    """Main driver code for copyspecial."""
    # This snippet will help you get started with the argparse module.
    parser = argparse.ArgumentParser()
    parser.add_argument('--todir', help='dest dir for special files')
    parser.add_argument('--tozip', help='dest zipfile for special files')
    # TODO: add one more argument definition to parse the 'from_dir' argument
    parser.add_argument('from_dir', help='from dir for special files')
    ns = parser.parse_args(args)

    # TODO: you must write your own code to get the command line args.
    # Read the docs and examples for the argparse module about how to do this.
    if ns.from_dir is not None and ns.todir is None and ns.tozip is None:
        print('\n'.join(get_special_paths(ns.from_dir)))
    elif ns.from_dir is not None and ns.todir is not None and ns.tozip is None:
        copy_to(get_special_paths(ns.from_dir), ns.todir)
    elif ns.from_dir is not None and ns.todir is None and ns.tozip is not None:
        zip_to(get_special_paths(ns.from_dir), ns.tozip)
    else:
        parser.print_help()

    # Parsing command line arguments is a must-have skill.
    # This is input data validation. If something is wrong (or missing) with
    # any required args, the general rule is to print a usage message and
    # exit(1).

    # Your code here: Invoke (call) your functions


if __name__ == "__main__":
    main(sys.argv[1:])
