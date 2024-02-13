#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Balazs Kocso"
__version__ = "1.2"


class LZW():
    def __init__(self, abc):
        self.abc = abc

    def _longest_prefix_match(self, string, list):
        max_idx = 0
        max_value = 0
        for i in range(len(list)):
            prefix_len = 0
            for j in range(len(string)):
                if j < len(list[i]) and list[i][j] == string[j]:
                    prefix_len += 1
                else:
                    break
            if prefix_len > max_value:
                max_value = prefix_len
                max_idx = i
        return max_idx

    def encode(self, input_string):
        output = []
        act_string = str(input_string)

        # INIT
        dictionary = list(self.abc)

        # ENCODE
        while act_string != "":
            idx = self._longest_prefix_match(act_string, dictionary)

            act_string = act_string[len(dictionary[idx]):]
            if act_string != "":
                dictionary.append(dictionary[idx] + act_string[0])

            output.append(idx + 1)

            # print dictionary

        return output

    def decode(self, encoded_string):
        output = ""
        act_string = list(encoded_string)

        # INIT
        dictionary = list(self.abc)

        # DECODE
        first = True
        while len(act_string) != 0:
            act_element = act_string.pop(0) - 1

            if first:
                first = False
            else:
                dictionary[-1] = dictionary[-1] + dictionary[act_element][0]

            output += dictionary[act_element]
            dictionary.append(dictionary[act_element])

            # print dictionary

        return output


if __name__ == '__main__':
    string = 'abababababababababababababababab'
    # string = 'abababababababababababababababab'

    abc = list(sorted(set(list(string))))
    # abc = ['a', 'b', 'c', 'd', 'e']

    lzw = LZW(abc)
    encoded_string = lzw.encode(string)
    decoded_string = lzw.decode(encoded_string)

    print(abc)
    print(string)
    print(encoded_string)
    print(decoded_string)