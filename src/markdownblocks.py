from htmlnode import ParentNode,LeafNode
from textnode import TextType,TextNode,text_node_to_html
from blocktype import BlockType,block_to_block_type,block_to_paragraph_lines,block_to_code_lines,block_to_list_lines
from splitnodes import text_to_text_nodes


def split_heading_tag_and_text(md):
    k = 0
    while md[k] == '#' and md[k+1] == '#':
        k+=1
    return (f'h{k+1}', md[k+2:])

def markdown_to_blocks(markdown):
    blocks = []
    blocks_raw = markdown.split('\n\n')
    for block in blocks_raw:
        block_stripped = block.strip()
        if block_stripped != '':
            blocks.append(block_stripped)
    return blocks

def split_paragraph_to_nodes(lines):
    child_text_nodes = []
    for line in lines:
        line_nodes = text_to_text_nodes(line)
        child_text_nodes.extend(line_nodes)
    child_html_nodes = []
    for node in child_text_nodes:
        child_html_nodes.append(text_node_to_html(node))
    return child_html_nodes

def markdown_to_html_node(markdown):
    div_child_nodes = []
    md_blocks = markdown_to_blocks(markdown)
    for block in md_blocks:
        block_type = block_to_block_type(block)
        
        if block_type == BlockType.PARAGRAPH:
            lines = block_to_paragraph_lines(block)
            child_html_nodes = split_paragraph_to_nodes(lines)
            div_child_nodes.append(ParentNode('p', child_html_nodes))
        elif block_type == BlockType.CODE:
            lines = block_to_code_lines(block)
            inner_node = LeafNode('code', f"{''.join(lines)}")
            div_child_nodes.append(ParentNode('pre', [inner_node]))
        elif block_type == BlockType.HEADING:
            tag,text = split_heading_tag_and_text(block)
            child_html_nodes = split_paragraph_to_nodes([text])
            div_child_nodes.append(ParentNode(tag, child_html_nodes))
        elif block_type == BlockType.UNORDERED_LIST:
            list_item_lines = [line.replace('- ','') for line in block_to_list_lines(block)]
            list_item_nodes = []
            for line in list_item_lines:
                line_nodes_html = split_paragraph_to_nodes([line])
                line_item_node = ParentNode('li', line_nodes_html)
                list_item_nodes.append(line_item_node)
            div_child_nodes.append(ParentNode('ul', list_item_nodes))
        elif block_type == BlockType.ORDERED_LIST:
            list_item_lines = block_to_list_lines(block)
            list_item_nodes = []
            for i in range(len(list_item_lines)):
                prefix = f'{i+1}. '
                line = list_item_lines[i].replace(prefix, '')
                line_nodes_html = split_paragraph_to_nodes([line])
                line_item_node = ParentNode('li', line_nodes_html)
                list_item_nodes.append(line_item_node)
            div_child_nodes.append(ParentNode('ol', list_item_nodes))
        elif block_type == BlockType.QUOTE:
            quote_lines = [line.replace('> ','') for line in block_to_paragraph_lines(block)]
            child_html_nodes = split_paragraph_to_nodes(quote_lines)
            div_child_nodes.append(ParentNode('blockquote', child_html_nodes))

    return ParentNode('div', div_child_nodes)