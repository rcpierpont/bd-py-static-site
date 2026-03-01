import re
from enum import Enum
from blockregex import is_heading,is_code,is_quote,is_ul,is_ol

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    if is_heading(block):
        return BlockType.HEADING
    elif is_code(block):
        return BlockType.CODE
    elif is_quote(block):
        return BlockType.QUOTE
    elif is_ul(block):
        return BlockType.UNORDERED_LIST
    elif is_ol(block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
    
def block_to_paragraph_lines(block):
    p_lines = []
    lines = block.split('\n')
    for i in range(len(lines)-1):
        p_lines.append(lines[i] + ' ')
    p_lines.append(lines[-1])
    return p_lines

def block_to_code_lines(block):
    c_lines = []
    lines = block.split('\n')
    for line in lines:
        if line == '```':
            continue
        c_lines.append(line + '\n')
    return c_lines

def block_to_list_lines(block):
    return block.split('\n')