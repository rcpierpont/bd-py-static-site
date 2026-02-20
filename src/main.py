from textnode import TextType,TextNode

def main():
    node = TextNode('hello', TextType.LINK, 'https://www.boot.dev')
    print(node)

main()