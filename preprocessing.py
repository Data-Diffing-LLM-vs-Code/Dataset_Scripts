from lxml import etree
import re
from pathlib import Path

folder = Path("samples/preprocessing/source")
converted_folder = Path("samples/preprocessing/converted")

files=list(folder.iterdir())
files.sort()
for file in files:
    print(file)

    new_file_name = converted_folder / f"{file.stem}.xml"

    try:
        with open (file, "r") as f:
            xml=f.read()
            xml=xml.replace(r"\n"," ").replace(r"\t"," ").replace("\r"," ").replace("\n"," ")
            xml=re.sub(r"\s+"," ",xml)

        root = etree.fromstring(xml.encode("UTF-8"), etree.XMLParser(remove_blank_text=True))
        etree.indent(root, space="    ")
        tree = root.getroottree()

        print(new_file_name)
        with open(new_file_name, "wb") as f:
            tree.write_c14n(
                f,
                with_comments=False,
                exclusive=False,
            )

        file.unlink()
    except Exception as e:
        print(f"Error processing file {file}: {e}")
        new_file_name.unlink(missing_ok=True)