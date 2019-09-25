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


def gen_button(tag, output, parent, wrapper_counter, sc):
    text = tag.text

    rn_tag_name = f"ButtonWrapper{wrapper_counter}"
    bw = output.new_tag(rn_tag_name)

    sc.create_styled_component(tag, rn_tag_name, "styled.TouchableOpacity")

    sc.create_styled_component(tag, rn_tag_name, "styled.Text")

    bt = output.new_tag(rn_tag_name)
    bt.append(text)
    bw.append(bt)
    parent.append(bw)

    return parent


def gen_textinput(tag, output, parent, wrapper_counter, sc):
    text = tag.text

    rn_tag_name = f"TextInputWrapper{wrapper_counter}"
    tiw = output.new_tag(rn_tag_name)
    sc.create_styled_component(tag, rn_tag_name, "styled.TextInput")

    parent.append(tiw)
    return parent


def gen_text(tag, output, parent, wrapper_counter, sc):
    text = tag.text

    rn_tag_name = f"TextWrapper{wrapper_counter}"
    tiw = output.new_tag(rn_tag_name)
    tiw.string = text
    sc.create_styled_component(tag, rn_tag_name, "styled.Text")

    parent.append(tiw)
    return parent


def gen_view(tag, output, parent, wrapper_counter, sc):
    text = tag.text

    rn_tag_name = f"Div{wrapper_counter}"
    tiw = output.new_tag(rn_tag_name)
    sc.create_styled_component(tag, rn_tag_name, "styled.View")

    parent.append(tiw)
    return parent
