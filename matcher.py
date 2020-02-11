#! /usr/bin/env python3
#  ----- ---- --- -- -
#  Copyright 2020 The Axiom Foundation. All Rights Reserved.
# 
#  Licensed under the Apache License 2.0 (the "License").  You may not use
#  this file except in compliance with the License.  You can obtain a copy
#  in the file LICENSE in the source distribution or at
#  https://www.apache.org/licenses/LICENSE-2.0.txt
#  - -- --- ---- -----

import typing
from dataclasses import dataclass


@dataclass
class Matcher:
    """
    A matcher accepts a list of tag, attribute, value, generator. When all of the first
    3 match, then the generator function is called on the matching tag.
    """

    name: str
    attribute: str
    value: str
    generator: object
    selector: object

    wrapper_counter: typing.ClassVar[int] = 0

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
        Matcher.wrapper_counter += 1
        return self.generator(tag, output, parent,
                              Matcher.wrapper_counter, self.selector)
