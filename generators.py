#! /usr/bin/env python3

#  ----- ---- --- -- -
#  Copyright 2020 The Axiom Foundation. All Rights Reserved.
# 
#  Licensed under the Apache License 2.0 (the "License").  You may not use
#  this file except in compliance with the License.  You can obtain a copy
#  in the file LICENSE in the source distribution or at
#  https://www.apache.org/licenses/LICENSE-2.0.txt
#  - -- --- ---- -----

import os
import tinycss
import html

tags_to_exclude_text = [
    "h1",
]

# Gloabl translation_keys list used by str_cook, which is used by all generators
# This gets set when
tns_keys = []


def str_cook(s):
    '''
    Preprocesses the string to
    1) unescape any html entities (artifact from webflow output)
    2) add i18n calls for recognized keys
    '''
    s = html.unescape(s)
    if s.strip() in tns_keys:
        s = f"i18n.t('{s}')"
    return s


def _gen_generic(tagname, componentname, tag, output, parent, wrapper_counter, sc):
    rn_tag_name = f"{tagname}{wrapper_counter}"
    child = output.new_tag(rn_tag_name)
    # As this is a change I make before I leave I wanted to
    # jsut comment. We need to think about if we want placeholder
    # text to come from weblfow.
    # try:
    #     if tag['placeholder']:
    #         child['placeholder'] = tag['placeholder']
    # except KeyError:
    #     pass

    sc.create_styled_component(tag, rn_tag_name, componentname)
    parent.append(child)
    return parent, child


def _gen_generic_text(tagname, componentname, tag, output, parent, wrapper_counter, sc):
    rn_tag_name = f"{tagname}{wrapper_counter}"
    child = output.new_tag(rn_tag_name)
    # if tag.name not in tags_to_exclude_text and 'Welcome' not in tagname:
    child.string = str_cook(tag.text)
    sc.create_styled_component(tag, rn_tag_name, componentname)
    parent.append(child)
    return parent, child


def gen_textinput(tag, output, parent, wrapper_counter, sc):
    return _gen_generic("TextInputWrapper", "styled.TextInput",
                        tag, output, parent, wrapper_counter, sc)


def gen_view(tag, output, parent, wrapper_counter, sc):
    return _gen_generic("Div", "styled.View",
                        tag, output, parent, wrapper_counter, sc)


def gen_text(tag, output, parent, wrapper_counter, sc):
    return _gen_generic_text("TextWrapper", "styled.Text",
                             tag, output, parent, wrapper_counter, sc)


def gen_button(tag, output, parent, wrapper_counter, sc):
    rn_tag_name = f"ButtonWrapper{wrapper_counter}"

    sc.create_styled_component(tag, rn_tag_name, "styled.TouchableOpacity")
    sc.create_styled_component(tag, rn_tag_name, "styled.Text")

    child = output.new_tag(rn_tag_name)
    text = tag.text
    if not text:
        text = tag['value']

    text = str_cook(text)
    child.append(text)
    parent.append(child)

    return parent, child


def gen_link(tag, output, parent, wrapper_counter, sc):
    rn_tag_name = f"LinkWrapper{wrapper_counter}"

    sc.create_styled_component(tag, rn_tag_name, "styled.TouchableOpacity")
    sc.create_styled_component(tag, rn_tag_name, "styled.Text")

    child = output.new_tag(rn_tag_name)
    text = tag.text
    if not text:
        text = tag['value']
    text = str_cook(text)
    child.append(text)
    parent.append(child)

    return parent, child
