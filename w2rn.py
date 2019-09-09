#! /usr/bin/env python3

import sys
import os
import generators
from bs4 import BeautifulSoup
from matcher import Matcher

input_dir = sys.argv[1]
output_dir = sys.argv[2]

# This is a list of all the matcher objects. Be aware that if multiple
# Matchers match the same tag, only the first one that matches gets called.
matchers = [
    Matcher("a", "class", "w-button",
            generators.gen_button, input_dir, output_dir),
    Matcher("input", "class", "text-field",
            generators.gen_textinput, input_dir, output_dir),
]


def process(tag, matchers, output, parent):
    for m in matchers:
        if m.match(tag):
            return m.generate(tag, output, parent)
    return parent


def processInputDir(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        if filename.endswith(".html"):
            with open(os.path.join(input_dir, filename), "r") as infile:
                inp = BeautifulSoup(infile, "lxml")

            outp = BeautifulSoup("", "lxml")
            div = outp.new_tag("Div1")

            # find_all walks the tree in order and emits a list of all tags in the system,
            # so we don't need to process things recursively.
            for ch in inp.body.find_all(True):
                div = process(ch, matchers, outp, div)

            outp.append(div)

            views_dir = os.path.join(output_dir, 'src', 'ui', 'views')
            os.makedirs(views_dir, exist_ok=True)
            react_native_filename = filename.capitalize().rpartition('.html')[
                0] + 'View'

            with open(os.path.join(views_dir, react_native_filename + '.js'), "w") as outfile:
                print("import React from 'react'", file=outfile)
                print("import styled from 'styled-components'\n", file=outfile)
                print(generators.use_styled_components(), file=outfile)
                print("class " + react_native_filename +
                      " extends React.Component {", file=outfile)
                print("  render() {", file=outfile)
                print("    return (", file=outfile)
                print("      " + outp.prettify(formatter='html'), file=outfile)
                print("    )", file=outfile)
                print("  }", file=outfile)
                print("}\n", file=outfile)
                print("export default " + react_native_filename, file=outfile)
        else:
            continue


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 w2rn.py <input-dir> <output-dir>")
        exit(1)

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    processInputDir(input_dir, output_dir)
