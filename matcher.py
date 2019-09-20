#! /usr/bin/env python3
from dataclasses import dataclass


@dataclass
class Matcher:
    """
    A matcher accepts a list of tag, attribute, value, process. When all of the first
    3 match, then the generator function is called on the matching tag.
    """
    name: str
    attribute: str
    value: str
    generator: object
    input_dir: str
    output_dir: str
    wrapper_counter: int

    def match(self, tag):
        if tag.name != self.name:
            return False

        # if tag.name == self.name and self.attribute is None:
        #     return True

        for k, v in tag.attrs.items():
            if k == self.attribute:
                if isinstance(v, list):
                    return self.value in v
                else:
                    return self.value == v
        return False

    def generate(self, tag, output, parent):
        """
        generate functions accept a tag, an output object (which is just the top-level
        BeautifulSoup object), and a parent (which is where the result should be
        inserted).
        """
        self.wrapper_counter += 1
        return self.generator(tag, output, parent, self.input_dir, self.output_dir, self.wrapper_counter)
