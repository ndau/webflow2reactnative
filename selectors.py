#! /usr/bin/env python3

import os
import tinycss

from dataclasses import dataclass, field

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

@dataclass
class Component:
    """
    A component holds a single component's worth of CSS by name
    """

    name: str
    typ: str
    css_rules: object

    def generate(self):
        rules = [f"{k}: {self.css_rules[k]};" for k in self.css_rules]
        css = "\n  ".join(rules)
        return f"const {self.name} = {self.typ}`\n  {css}`\n\n"


@dataclass
class SelectorCollector:
    """
    A SelectorCollector is used to process css styles
    """

    css_dir: str
    components: object = field(default_factory = dict)
    wrapper_counter: int = 0


    def _all_css_files(self):
        """ generator helper for the names of all css files in self.css_dir """
        for subdir, dirs, files in os.walk(self.css_dir):
            for file in files:
                filepath = subdir + os.sep + file

                if filepath.endswith(".css"):
                    yield filepath


    def _lookup_rules(self, rule, klass):
        """
        looks for css in the rule related to klass and extracts the elements
        that are not explicitly excluded. Might return an empty list.
        """
        selector = rule.selector.as_css()
        css_rules = {}
        if selector not in ["." + klass, "#" + klass, klass]:
            return css_rules

        for d in rule.declarations:
            prop_css_val = "".join(v.as_css() for v in d.value)

            excluded = False
            for exclude in rn_css_excludes:
                if exclude in d.name or exclude in prop_css_val:
                    excluded = True

            if not excluded:
                css_rules[d.name] = prop_css_val

        return css_rules

    def create_styled_component(self, tag, component_name, component_type):
        parser = tinycss.make_parser()

        class_names = tag.get("class", "")
        components = {}
        css_rules = {}

        for filepath in self._all_css_files():
            with open(filepath) as f:
                stylesheet = parser.parse_stylesheet(f.read())
                for rule in stylesheet.rules:
                    # let us reconstruct the css rule
                    for klass in class_names:
                        try:
                            css_rules.update(self._lookup_rules(rule, klass))
                        except AttributeError:
                            for media_rule in rule.rules:
                                for klass in class_names:
                                    css_rules.update(self._lookup_rules(media_rule, klass))

        self.components[component_name] = Component(component_name, component_type, css_rules)


    def generate(self):
        output = ""
        for name in self.components:
            output += self.components[name].generate()
        return output
