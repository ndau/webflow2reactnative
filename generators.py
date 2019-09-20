#! /usr/bin/env python3

import os
import tinycss
from tinycss.css21 import CSS21Parser

# React Native does not support all CSS keys
# below is a list of keys it does not support
# or it does not work well in RN
rn_css_filter = ["webkit", "ms-", "inline-block",
                 "line-height", "cursor", "block", "clear", "order"]


def create_styled_component(tag, component_name, component_type, css_dir, selector):
    parser = tinycss.make_parser('page3')

    class_names = tag.get('class', '')
    styled_component = f'const {component_name} = {component_type}`\n'
    css = ''

    for subdir, dirs, files in os.walk(css_dir):
        for file in files:
            filepath = subdir + os.sep + file

            if filepath.endswith(".css"):
                with open(filepath) as f:
                    stylesheet = CSS21Parser().parse_stylesheet(f.read())
                    for rule in stylesheet.rules:
                        # let us reconstruct the css rule
                        for klass in class_names:
                            try:
                                the_css = search_for_selector(rule, klass)
                                if the_css is not None:
                                    css += the_css
                            except AttributeError:
                                for media_rule in rule.rules:
                                    for klass in class_names:
                                        the_css = search_for_selector(
                                            media_rule, klass)
                                        if the_css is not None:
                                            css += the_css
    return styled_component + css + '`\n'


def search_for_selector(rule, klass):
    selector = rule.selector.as_css()
    if selector == '.' + klass or selector == '#' + klass or selector == klass:
        css_str = ''
        for d in rule.declarations:
            prop_css_val = ' '.join(v.as_css() for v in d.value)

            found_in_filter = False
            for filter in rn_css_filter:
                if str(d.name).find(filter) >= 0 or prop_css_val.find(filter) >= 0:
                    found_in_filter = True

            if not found_in_filter:
                css_str += f"{d.name}:{prop_css_val};\n"

        return css_str


def gen_button(tag, output, parent, input_dir, output_dir, wrapper_counter):
    text = tag.text

    rn_tag_name = f"ButtonWrapper{wrapper_counter}"
    bw = output.new_tag(rn_tag_name)
    styled_components = create_styled_component(tag,
                                                rn_tag_name,
                                                "styled.TouchableOpacity",
                                                os.path.join(
                                                    input_dir, 'css'),
                                                text)

    styled_components += create_styled_component(tag,
                                                 rn_tag_name,
                                                 "styled.Text",
                                                 os.path.join(
                                                     input_dir, 'css'),
                                                 text)

    bt = output.new_tag(rn_tag_name)
    bt.append(text)
    bw.append(bt)
    parent.append(bw)

    return parent, styled_components


def gen_textinput(tag, output, parent, input_dir, output_dir, wrapper_counter):
    text = tag.text

    rn_tag_name = f"TextInputWrapper{wrapper_counter}"
    tiw = output.new_tag(rn_tag_name)
    styled_components = create_styled_component(tag,
                                                rn_tag_name,
                                                "styled.TextInput",
                                                os.path.join(
                                                    input_dir, 'css'),
                                                text)

    parent.append(tiw)
    return parent, styled_components


def gen_text(tag, output, parent, input_dir, output_dir, wrapper_counter):
    text = tag.text

    rn_tag_name = f"TextWrapper{wrapper_counter}"
    tiw = output.new_tag(rn_tag_name)
    tiw.string = text
    styled_components = create_styled_component(tag,
                                                rn_tag_name,
                                                "styled.Text",
                                                os.path.join(
                                                    input_dir, 'css'),
                                                text)

    parent.append(tiw)
    return parent, styled_components


def gen_view(tag, output, parent, input_dir, output_dir, wrapper_counter):
    text = tag.text

    rn_tag_name = f"Div{wrapper_counter}"
    tiw = output.new_tag(rn_tag_name)
    styled_components = create_styled_component(tag,
                                                rn_tag_name,
                                                "styled.View",
                                                os.path.join(
                                                    input_dir, 'css'),
                                                text)

    parent.append(tiw)
    return parent, styled_components
