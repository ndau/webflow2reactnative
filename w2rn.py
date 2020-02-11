#! /usr/bin/env python3

#  ----- ---- --- -- -
#  Copyright 2020 The Axiom Foundation. All Rights Reserved.
# 
#  Licensed under the Apache License 2.0 (the "License").  You may not use
#  this file except in compliance with the License.  You can obtain a copy
#  in the file LICENSE in the source distribution or at
#  https://www.apache.org/licenses/LICENSE-2.0.txt
#  - -- --- ---- -----

import sys
import os
import generators
from bs4 import BeautifulSoup
from matcher import Matcher
from string import Template
from pathlib import Path
from helpers import steprint, parse_args, ensure_output_dir, load_lng_file

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
        Matcher("div", "class", "div-block-price", generators.gen_view, sc),
        Matcher("div", "class", "div-block-pricing", generators.gen_view, sc),
        Matcher("div", "class", "div-block-price-metrics",
                generators.gen_view, sc),
        Matcher("div", "class", "border",
                generators.gen_view, sc),
        Matcher("div", "class", "div-block-add-account",
                generators.gen_view, sc),
        Matcher("div", "class", "div-block-overview-heading",
                generators.gen_view, sc),
        Matcher("div", "class", "div-block-account-summary",
                generators.gen_view, sc),
        Matcher("div", "class", "div-block-account-title",
                generators.gen_view, sc),
        Matcher("div", "class", "div-block-account-amount",
                generators.gen_view, sc),
        Matcher("body", "class", "outercontainertop", generators.gen_view, sc),
        Matcher("h1", "class", "heading", generators.gen_text, sc),
        Matcher("h1", "class", "heading-large-ndau", generators.gen_text, sc),
        Matcher("h1", "class", "heading-account", generators.gen_text, sc),

        Matcher("strong", "class", "bold-text", generators.gen_text, sc),
        Matcher("strong", "class", "bold-text-2", generators.gen_text, sc),
        Matcher("div", "class", "text-block-2", generators.gen_text, sc),
        Matcher("div", "class", "text-block-4", generators.gen_text, sc),
        Matcher("div", "class", "text-block-total-ndau",
                generators.gen_text, sc),
        Matcher("div", "class", "text-block-price-total",
                generators.gen_text, sc),
        Matcher("div", "class", "text-block-us-amount",
                generators.gen_text, sc),
        Matcher("div", "class", "text-block-negative",
                generators.gen_text, sc),
        Matcher("div", "class", "text-block-account", generators.gen_text, sc),
        Matcher("div", "class", "text-block-fa-orange",
                generators.gen_text, sc),
        Matcher("div", "class", "text-block-positive",
                generators.gen_text, sc),
        Matcher("div", "class", "text-block-dollar", generators.gen_text, sc),
        Matcher("div", "class", "text-block-account-title",
                generators.gen_text, sc),
        Matcher("section", "class", "containerbottom",
                generators.gen_view, sc),
    ]
    steprint("Processing...", end='')
    processInputDir(input_dir, output_dir, sc, matchers)
    steprint("Done")
