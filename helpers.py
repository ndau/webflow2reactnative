#  ----- ---- --- -- -
#  Copyright 2020 The Axiom Foundation. All Rights Reserved.
# 
#  Licensed under the Apache License 2.0 (the "License").  You may not use
#  this file except in compliance with the License.  You can obtain a copy
#  in the file LICENSE in the source distribution or at
#  https://www.apache.org/licenses/LICENSE-2.0.txt
#  - -- --- ---- -----

import os
import sys
import argparse  # for parsing arguments
import esprima  # for parsing js files


def steprint(*args, **kwargs):
    """Prints to stderr."""
    print(*args, file=sys.stderr, **kwargs)


def print_error(msg):
    """Prints a warning message to stderr"""
    steprint(f"\033[31mERROR\033[0m: {msg}")


def parse_args(args):

    parser = argparse.ArgumentParser(
        description='Transforms Webflow output to react native components.')
    parser.add_argument('input_dir', help='input directory')
    parser.add_argument(
        'output_dir', help='output directory (will overwrite any previous contents)')
    parser.add_argument('--lng-file', help='location of translation file')

    args = vars(parser.parse_args())
    input_dir = args['input_dir']
    lng_file = args['lng_file']
    if lng_file is not None and not os.path.exists(lng_file):
        print_error(f'Specified language file not found: {lng_file}')
        exit(1)

    # check args
    if not os.path.exists(input_dir):
        print_error(f'Input directory {input_dir} does not exist.')
        exit(1)

    if not os.path.isdir(input_dir):
        print_error(f'Input directory {input_dir} is not a directory.')
        exit(1)

    return args


def load_lng_file(lng_file_path):
    """
    Loads a js module, looks for the export default statement, parses the keys from the object supplied.
    Note: this does not evaluate any javascript, it only parses it. That means only strings will work.
    """
    tns_keys = []
    lng_file_string = open(lng_file_path).read()
    tree = esprima.parseModule(lng_file_string)
    try:
        for parent in tree.body:
            if parent.type is "ExportDefaultDeclaration":
                for node in parent.declaration.properties:
                    key = node.key.value
                    if key is None and node.key.name is not None:
                        key = node.key.name
                    tns_keys.append(key)
    except:
        print_error(f"Could not parse lng_file: {sys.exc_info()[0]}. \n ")
        exit(1)

    return tns_keys


def ensure_output_dir(output_dir):
    """
    Ensures the existence of the output directory
    """
    if os.path.exists(output_dir) and not os.path.isdir(output_dir):
        print_error(
            f"output directory {output_dir} exist and is not a directory.")
        exit(1)
    if not os.path.exists(output_dir):
        steprint(f"Output directory: {output_dir} does not exist. Creating...")
        try:
            os.mkdir(output_dir)
        except OSError:
            print_error(f"Creation of the directory {output_dir} failed")
        else:
            steprint(f"Created {output_dir} ")
