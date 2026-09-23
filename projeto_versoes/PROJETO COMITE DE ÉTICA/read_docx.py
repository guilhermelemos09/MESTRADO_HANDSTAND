import zipfile
import xml.etree.ElementTree as ET
import sys
import os

def read_docx(path):
    try:
        with zipfile.ZipFile(path, 'r') as docx:
            xml_content = docx.read('word/document.xml')
            tree = ET.XML(xml_content)
            namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            paragraphs = []
            for p in tree.findall('.//w:p', namespaces):
                texts = [node.text for node in p.findall('.//w:t', namespaces) if node.text]
                if texts:
                    paragraphs.append(''.join(texts))
            return '\n'.join(paragraphs)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    for arg in sys.argv[1:]:
        if not os.path.exists(arg):
            print(f"File not found: {arg}")
            continue
        print(f"--- {os.path.basename(arg)} ---")
        out_name = arg + ".txt"
        with open(out_name, "w", encoding="utf-8") as f:
            f.write(read_docx(arg))
        print(f"Written to {out_name}")
