#! /usr/bin/env python3

import os
import tinycss
from tinycss.css21 import CSS21Parser

# ---- generators ---
styled_components = ''

# React Native does not support all CSS keys
# below is a list of keys it does not support
rn_css_filter = ["webkit", "ms-"]


def use_styled_components():
    """
    function to search for a CSS selector in all css files
    """
    global styled_components
    sc = styled_components
    styled_components = ''
    return sc


def create_styled_component(tag, component_name, component_type, css_dir, selector):
    parser = tinycss.make_parser('page3')
    class_names = tag['class']
    styled_component = 'const ' + component_name + ' = ' + component_type + '`\n'
    css = ''

    for subdir, dirs, files in os.walk(css_dir):
        for file in files:
            filepath = subdir + os.sep + file

            if filepath.endswith(".css"):
                f = open(filepath)
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
            prop_css_val = ''
            for v in d.value:
                prop_css_val = prop_css_val+' '+v.as_css()

            found_in_filter = False
            for filter in rn_css_filter:
                if str(d.name).find(filter) >= 0 or prop_css_val.find(filter) >= 0:
                    found_in_filter = True

            if not found_in_filter:
                css_str = css_str + \
                    str(d.name)+":"+prop_css_val+";\n"

        return css_str

# the generator for a Button


def gen_button(tag, output, parent, input_dir, output_dir):
    global styled_components
    text = tag.text

    bw = output.new_tag("ButtonWrapper")
    styled_components = create_styled_component(tag,
                                                "ButtonWrapper",
                                                "styled.TouchableOpacity",
                                                os.path.join(input_dir, 'css'),
                                                text)

    styled_components += create_styled_component(tag,
                                                 "ButtonText",
                                                 "styled.Text",
                                                 os.path.join(
                                                     input_dir, 'css'),
                                                 text)

    bt = output.new_tag("ButtonText")
    bt.append(text)
    bw.append(bt)
    parent.append(bw)

    return parent


# the generator for a text input
def gen_textinput(tag, output, parent, input_dir, output_dir):
    tiw = output.new_tag("TextInputWrapper")
    parent.append(tiw)
    return parent
