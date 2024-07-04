#!/usr/bin/env python3

import os
import re
import sys

RE_INVALID_CHAR = re.compile('[^A-FU0-9+_]')
RE_MISSING_UNDERSCORE = re.compile('(?<!_)U')
RE_MISSING_LETTER_U = re.compile('_(?!U)')
RE_MISSING_SIGN_PLUS = re.compile('U(?!\\+)')

def any_problems_here():
    found_invalid_filenames = False
    for filename in os.listdir():
        if not filename.lower().endswith('.png'):
            print(f'Non-png file {filename} does not belong in the emoji directory')
            found_invalid_filenames = True
            continue
        base_filename = filename[:-len('.png')]
        if RE_INVALID_CHAR.search(base_filename):
            print(f'Filename {filename} contains invalid characters in its filename. Only uppercase letters'
                  ' A-F and U, numbers, +, and _ should be used.')
            found_invalid_filenames = True
        if 'U+0' in base_filename:
            print(f'Filename {filename} contains codepoint(s) with leading zeros. Leading zeros should be'
                  ' removed from codepoint(s).')
            found_invalid_filenames = True
        if '+U' in base_filename:
            print(f'Filename {filename} is incorrectly named. "_" should be used as a separator between'
                  ' codepoints, not "+".')
            found_invalid_filenames = True
        if RE_MISSING_UNDERSCORE.search(base_filename):
            print(f'Filename {filename} is missing an underscore "_" between codepoints.')
            found_invalid_filenames = True
        if RE_MISSING_LETTER_U.search(base_filename):
            print(f'Filename {filename} is either missing a "U" to indicate the start of a codepoint,'
                  ' or has a spurious underscore ("_").')
            found_invalid_filenames = True
        if RE_MISSING_SIGN_PLUS.search(base_filename):
            print(f'Filename {filename} is either missing a "+" after a "U", or has a spurious "U".')
            found_invalid_filenames = True
        if 'U+FE0F' in base_filename:
            print(f'Filename {filename} should not include any emoji presentation selectors. U+FE0F codepoints'
                  ' should be removed from the filename.')
            found_invalid_filenames = True

        try:
            code_points = [int(code_point[len('U+'):], 16) for code_point in base_filename.split('_')]
            if any(code_point > 0x10ffff for code_point in code_points):
                print(f'Filename {filename} contains a code point exceeding U+10FFFF')
                found_invalid_filenames = True
        except ValueError:
            print(f'Filename {filename} contains invalid Unicode code points.')
            found_invalid_filenames = True

    return found_invalid_filenames

if __name__ == '__main__':
    try:
     script_dir = os.path.dirname(os.path.abspath(__file__))
     os.chdir(os.path.join(script_dir, "../Base/res/emoji/"))
 except OSError as e:
     print(f"Error changing directory: {e}")
     sys.exit(1)

    if any_problems_here():
        sys.exit(1)
