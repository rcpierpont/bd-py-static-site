import re

IMAGE_REGEX = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
LINK_REGEX = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
TITLE_REGEX = r"^#{1}\s{1}.+"

def extract_markdown_images(text):
    return re.findall(IMAGE_REGEX, text)

def extract_markdown_links(text):
    return re.findall(LINK_REGEX, text)

def extract_title(text):
    matches = re.findall(TITLE_REGEX, text, flags=re.MULTILINE) 
    return matches[0][2:]