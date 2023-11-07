import re


def compile_regexes(include_patterns, exclude_patterns):
    compiled_include = [re.compile(regex) for regex in include_patterns or []]
    compiled_exclude = [re.compile(regex) for regex in exclude_patterns or []]

    return compiled_include, compiled_exclude


def search_regexes(regexes_list, search_text):
    for regex in regexes_list:
        if regex.search(search_text) is not None:
            return True
