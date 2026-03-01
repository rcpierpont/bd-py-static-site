import re

HEADING_REGEX = r"(#{1,6})\s(.+)"
CODE_BLOCK_REGEX = r"(`{3}\n)[.\w\d\s\{\}\(\);\?:\\]*(`{3})"

def is_heading(block):
    if re.match(HEADING_REGEX, block):
        return True
    return False

def is_code(block):
    lines = block.split('\n')
    if len(lines) > 1 and lines[0].startswith('```') and lines[-1].endswith('```'):
        return True
    return False

def is_quote(block):
    block_lines = block.split('\n')
    is_quote = True
    for line in block_lines:
        if line[0] == '>':
            continue
        is_quote = False
    return is_quote

def is_ul(block):
    block_lines = block.split('\n')
    is_ul = True
    for line in block_lines:
        if line.startswith('- '):
            continue
        is_ul = False
    return is_ul

def is_ol(block):
    block_lines = block.split('\n')
    is_ol = True
    for k in range(len(block_lines)):
        if block_lines[k].startswith(f'{k+1}. '):
            continue
        is_ol = False
    return is_ol