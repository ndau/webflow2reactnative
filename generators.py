#! /usr/bin/env python3

import os
import tinycss

tags_to_exclude_text = [
    "h1",
]


def _gen_generic(tagname, componentname, tag, output, parent, wrapper_counter, sc):
    rn_tag_name = f"{tagname}{wrapper_counter}"
    child = output.new_tag(rn_tag_name)
    try:
        if tag['placeholder']:
            child['placeholder'] = tag['placeholder']
    except KeyError:
        pass

    sc.create_styled_component(tag, rn_tag_name, componentname)

    parent.append(child)
    return parent, child


def _gen_generic_text(tagname, componentname, tag, output, parent, wrapper_counter, sc):
    rn_tag_name = f"{tagname}{wrapper_counter}"
    child = output.new_tag(rn_tag_name)
    if tag.name not in tags_to_exclude_text:
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
    if not text:
        text = tag['value']
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
    child.append(text)
    parent.append(child)

    return parent, child
