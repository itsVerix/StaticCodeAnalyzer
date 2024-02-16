import re
from helper_functions import *


def valid_indentation(line):
    if line[0] != ' ':
        return True
    if spaces_cnt(line) % 4 != 0 and spaces_cnt(line) != 0:
        return False
    return True


def unnecessary_semicolon(line):
    # Remove string literals from consideration to avoid false positives
    line_without_strings = ""
    in_string = False
    string_char = ''
    for char in line:
        if char in ('"', "'") and not in_string:
            in_string = True
            string_char = char
        elif char == string_char and in_string:
            in_string = False
            string_char = ''
        if not in_string:
            line_without_strings += char

    # Now check for semicolons outside of strings
    index = line_without_strings.find('#')
    if index != -1:
        # Ignore everything after the comment symbol
        line_without_strings = line_without_strings[:index]

    if ';' in line_without_strings:
        # Simplified check: If there's a semicolon not in a string or comment, consider it unnecessary
        return True
    return False


def valid_inline_comment(line):
    index = line.find('#')
    if index == -1 or index == 0:
        return True
    if line[index-1] != ' ' or line[index-2] != ' ':
        return False
    return True


def find_todo(line):
    index = line.find('#')
    if index == -1:
        return False
    if line[index+1:].lower().find('todo') != -1:
        return True
    return False


def too_many_spaces(line):
    if re.match(r'\s*(def|class)', line) is None:
        return False, None

    regex = r'\s*(def|class)\s{1}\w'
    if re.match(regex, line) is None:
        return True, re.search(r'\s*(def|class)\s{2,}', line).group()
    return False, None


def not_camel_case_class(line):
    if line.find('class') == -1:
        return False, None

    regex = r'\s*class\s+([A-Z][a-z]+)+[:(]'
    if re.match(regex, line) is None:
        return True, re.search(r'\s(\w+)[:(]', line).group(1)
    return False, None


def not_snake_case_func(line):
    if line.find('def') == -1:
        return False, None

    regex = r'^\s*def\s+([a-z_][a-z_0-9]*)\s*\((.*?)\)\s*:'
    if re.match(regex, line) is None:
        return True, re.search(r'\s(\w+)\(', line).group(1)
    return False, None
