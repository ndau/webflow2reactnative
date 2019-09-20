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


def all_css_files(css_dir):
    """ generator for all css files in css_dir """
    for subdir, dirs, files in os.walk(css_dir):
        for file in files:
            filepath = subdir + os.sep + file

            if filepath.endswith(".css"):
                yield filepath


def create_styled_component(tag, component_name, component_type, css_dir, selector):
    parser = tinycss.make_parser()

    class_names = tag.get("class", "")
    css_rules = []

    for filepath in all_css_files(css_dir):
        with open(filepath) as f:
            stylesheet = parser.parse_stylesheet(f.read())
            for rule in stylesheet.rules:
                # let us reconstruct the css rule
                for klass in class_names:
                    try:
                        css_rules.extend(search_for_selector(rule, klass))
                    except AttributeError:
                        for media_rule in rule.rules:
                            for klass in class_names:
                                css_rules.extend(search_for_selector(media_rule, klass))

    css = "\n  ".join([r for r in css_rules])
    styled_component = f"const {component_name} = {component_type}`\n  {css}`\n\n"
    return styled_component


def search_for_selector(rule, klass):
    """
    looks for css in the rule related to klass and extracts the elements
    that are not explicitly excluded. Might return an empty list.
    """
    selector = rule.selector.as_css()
    css_rules = []
    if selector not in ["." + klass, "#" + klass, klass]:
        return css_rules

    for d in rule.declarations:
        prop_css_val = "".join(v.as_css() for v in d.value)

        excluded = False
        for exclude in rn_css_excludes:
            if exclude in d.name or exclude in prop_css_val:
                excluded = True

        if not excluded:
            css_rules.append(f"{d.name}: {prop_css_val};")

    return css_rules


def gen_button(tag, output, parent, input_dir, output_dir, wrapper_counter):
    text = tag.text

    rn_tag_name = f"ButtonWrapper{wrapper_counter}"
    bw = output.new_tag(rn_tag_name)
    styled_components = create_styled_component(
        tag,
        rn_tag_name,
        "styled.TouchableOpacity",
        os.path.join(input_dir, "css"),
        text,
    )

    styled_components += create_styled_component(
        tag, rn_tag_name, "styled.Text", os.path.join(input_dir, "css"), text
    )

    bt = output.new_tag(rn_tag_name)
    bt.append(text)
    bw.append(bt)
    parent.append(bw)

    return parent, styled_components


def gen_textinput(tag, output, parent, input_dir, output_dir, wrapper_counter):
    text = tag.text

    rn_tag_name = f"TextInputWrapper{wrapper_counter}"
    tiw = output.new_tag(rn_tag_name)
    styled_components = create_styled_component(
        tag, rn_tag_name, "styled.TextInput", os.path.join(input_dir, "css"), text
    )

    parent.append(tiw)
    return parent, styled_components


def gen_text(tag, output, parent, input_dir, output_dir, wrapper_counter):
    text = tag.text

    rn_tag_name = f"TextWrapper{wrapper_counter}"
    tiw = output.new_tag(rn_tag_name)
    tiw.string = text
    styled_components = create_styled_component(
        tag, rn_tag_name, "styled.Text", os.path.join(input_dir, "css"), text
    )

    parent.append(tiw)
    return parent, styled_components


def gen_view(tag, output, parent, input_dir, output_dir, wrapper_counter):
    text = tag.text

    rn_tag_name = f"Div{wrapper_counter}"
    tiw = output.new_tag(rn_tag_name)
    styled_components = create_styled_component(
        tag, rn_tag_name, "styled.View", os.path.join(input_dir, "css"), text
    )

    parent.append(tiw)
    return parent, styled_components
