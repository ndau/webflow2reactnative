#! /usr/bin/env python3

import sys
import os
import generators
from bs4 import BeautifulSoup
from matcher import Matcher
from string import Template
from pathlib import Path
import argparse  # for parsing arguments
import esprima  # for parsing js files

from selector_collector import SelectorCollector


def process(tag, matchers, output, parent):
    for m in matchers:
        if m.match(tag):
            return m.generate(tag, output, parent)

    return parent, parent


def handle_tag(tag, matchers, output, outparent):
    """
    tag is the tag to check
    outparent is the node to attach any generated object to
    """

    sys.stderr.write(".")  # show progress
    sys.stderr.flush()
    # outchild is the parent if we don't overwrite it
    outchild = outparent
    for ch in tag.find_all(recursive=False):
        outparent, outchild = process(
            ch, matchers, output, outparent)
        outchild = handle_tag(ch, matchers, output, outchild)

    return outparent, outchild


def processInputDir(input_dir, output_dir, sc, matchers):

    for path in Path(input_dir).glob("*.html"):
        sys.stderr.write(f"\n{path}")  # show progress
        with open(path, "r") as infile:
            inp = BeautifulSoup(infile, "lxml")

        outp = BeautifulSoup("", "lxml")

        # find_all walks the tree in order and emits a list of all tags in the system,
        # so we don't need to process things recursively.
        div = outp.new_tag("Body")
        div, junk = handle_tag(inp.body, matchers, outp, div)
        # for ch in inp.body.find_all(True):
        #     div = process(ch, matchers, outp, div)

        outp.append(div)

        writeReactNativeFile(output_dir, path.name, sc, outp)
    steprint()  # print new line


def get_template():
    """ get a template relative to the directory with file containing __main__ """
    template = ""
    if "__file__" in vars():
        template = os.path.join(
            os.path.dirname(os.path.realpath("__file__")),
            "templates",
            "rn_view.template",
        )
    else:
        template = os.path.join("templates", "rn_view.template")

    with open(template, encoding="utf8") as f:
        template = f.read()
    return template


def writeReactNativeFile(output_dir, filename, sc, outp):
    views_dir = os.path.join(output_dir, "src", "ui", "views")
    os.makedirs(views_dir, exist_ok=True)
    react_native_filename = filename.rpartition(".html")[0]

    template = Template(get_template())
    content = template.substitute(
        styled_components=sc.generate(outp), jsx=outp.prettify(formatter="minimal")
    )

    with open(os.path.join(views_dir, react_native_filename + ".js"), "w") as outfile:
        print(content, file=outfile)


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


def load_lng_file(filepath):
    """
    Loads a js module, looks for the export default statement, parses the keys from the object supplied.
    Note: this does not evaluate any javascript, it only parses it. That means only strings will work.
    """
    tns_keys = []
    lng_file_string = open(lng_file).read()
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


if __name__ == "__main__":

    args = parse_args(sys.argv[1:])
    input_dir = args['input_dir']
    output_dir = args['output_dir']
    lng_file = args['lng_file']

    ensure_output_dir(output_dir)

    # Change the gloabl translation key list for the generators
    generators.tns_keys = load_lng_file(lng_file)

    sc = SelectorCollector(os.path.join(input_dir, "css"))

    # This is a list of all the matcher objects. Be aware that if multiple
    # Matchers match the same tag, only the first one that matches gets called
    matchers = [
        Matcher("a", "class", "w-button", generators.gen_button, sc),
        Matcher("a", "class", "link", generators.gen_button, sc),
        Matcher("input", "class", "w-button", generators.gen_button, sc),
        Matcher("form", "class", "form", generators.gen_view, sc),
        Matcher("div", "class", "w-container", generators.gen_view, sc),
        Matcher("div", "class", "w-form", generators.gen_view, sc),
        Matcher("div", "class", "buttoncontainer", generators.gen_view, sc),
        Matcher("input", "class", "w-input", generators.gen_textinput, sc),
        Matcher("div", "class", "upperdiv", generators.gen_view, sc),
        Matcher("div", "class", "lowerdiv", generators.gen_view, sc),
        Matcher("div", "class", "div-block-5", generators.gen_view, sc),
        Matcher("div", "class", "div-block-3", generators.gen_view, sc),
        Matcher("body", "class", "outercontainertop", generators.gen_view, sc),
        Matcher("h1", "class", "heading", generators.gen_text, sc),
        Matcher("strong", "class", "bold-text", generators.gen_text, sc),
        Matcher("strong", "class", "bold-text-2", generators.gen_text, sc),
        Matcher("div", "class", "text-block-2", generators.gen_text, sc),
        Matcher("div", "class", "text-block-4", generators.gen_text, sc),
        Matcher("section", "class", "containerbottom",
                generators.gen_view, sc),
    ]
    steprint("Processing...", end='')
    processInputDir(input_dir, output_dir, sc, matchers)
    steprint("Done")
