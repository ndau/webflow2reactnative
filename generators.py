#! /usr/bin/env python3

import os
import tinycss
from tinycss.css21 import CSS21Parser

# React Native does not support all CSS keys
# below is a list of keys it does not support
rn_css_filter = ["webkit", "ms-"]


def create_styled_component(tag, component_name, component_type, css_dir, selector):
    parser = tinycss.make_parser('page3')
    class_names = tag['class']
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
    if rule.selector.as_css() == '.' + klass or rule.selector.as_css() == '#' + klass or rule.selector.as_css() == klass:
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

# the generator for a Button


button_wrapper_counter = 1


def gen_button(tag, output, parent, input_dir, output_dir):
    global button_wrapper_counter
    text = tag.text

    bw = output.new_tag(f"ButtonWrapper{button_wrapper_counter}")
    styled_components = create_styled_component(tag,
                                                f"ButtonWrapper{button_wrapper_counter}",
                                                "styled.TouchableOpacity",
                                                os.path.join(
                                                    input_dir, 'css'),
                                                text)

    styled_components += create_styled_component(tag,
                                                 f"ButtonText{button_wrapper_counter}",
                                                 "styled.Text",
                                                 os.path.join(
                                                     input_dir, 'css'),
                                                 text)

    bt = output.new_tag(f"ButtonText{button_wrapper_counter}")
    bt.append(text)
    bw.append(bt)
    parent.append(bw)

    button_wrapper_counter += 1

    return parent, styled_components


# the generator for a text input
def gen_textinput(tag, output, parent, input_dir, output_dir):
    tiw = output.new_tag("TextInputWrapper")

    styled_components = ''

    parent.append(tiw)
    return parent, styled_components
