#! /usr/bin/env python3

import os
import tinycss

# React Native does not support all CSS keys
# below is a list of keys it does not support
# or it does not work well in RN
rn_css_excludes = [
    "webkit",
    "ms-",
    "inline-block",
    "line-height",
    "cursor",
    "block",
    "clear",
    "order",
]


def _gen_generic(tagname, componentname, tag, output, parent, wrapper_counter, sc):
    rn_tag_name = f"{tagname}{wrapper_counter}"
    child = output.new_tag(rn_tag_name)
    sc.create_styled_component(tag, rn_tag_name, componentname)

    parent.append(child)
    return parent, child


def _gen_generic_text(tagname, componentname, tag, output, parent, wrapper_counter, sc):
    rn_tag_name = f"{tagname}{wrapper_counter}"
    child = output.new_tag(rn_tag_name)
    child.string = tag.text
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
    child.append(text)
    parent.append(child)

    return parent, child


