#! /usr/bin/env python3

# A matcher accepts a list of tag, attribute, value, process. When all of the first
# 3 match, then the generator function is called on the matching tag.


class Matcher(object):
    def __init__(self, name, attribute, value, generator, input_dir, output_dir):
        self.name = name
        self.attribute = attribute
        self.value = value
        self.generator = generator
        self.input_dir = input_dir
        self.output_dir = output_dir

    def match(self, tag):
        if tag.name != self.name:
            return False
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
        return self.generator(tag, output, parent, self.input_dir, self.output_dir)
