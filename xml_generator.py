import random
import xml.etree.ElementTree as ET

WORDS = ['Lorem', 'ipsum', 'dolor', 'sit', 'amet', 'consetetur', 'sadipscing', 'elitr', 'sed', 'diam', 'nonumy', 'eirmod', 'tempor', 'invidunt', 'ut', 'labore', 'et', 'dolore', 'magna', 'aliquyam', 'erat', 'sed', 'diam', 'voluptua', 'At', 'vero', 'eos', 'et', 'accusam', 'et', 'justo', 'duo', 'dolores', 'et', 'ea', 'rebum', 'Stet', 'clita', 'kasd', 'gubergren', 'no', 'sea', 'takimata', 'sanctus', 'est']

def generate_words(min_words, max_words):
    length = random.randint(min_words, max_words)
    return " ".join(random.choices(WORDS, k=length))


def generate_xml(filename, target_mib):
    target_bytes = target_mib * 1024 * 1024
    root = ET.Element("dataset")

    record_id = 1
    while True:
        record = ET.SubElement(root, "record", id=str(record_id))

        ET.SubElement(record, "identifier").text = f"{random.choice(WORDS)}-{random.randint(1000, 9999)}"
        ET.SubElement(record, "category").text = f"{random.choice(WORDS)}"
        ET.SubElement(record, "summary").text = generate_words(4, 8)
        ET.SubElement(record, "description").text = generate_words(10, 20)
        ET.SubElement(record, "status").text = f"{random.choice(WORDS)}"

        sub_node = ET.SubElement(record, "details")
        ET.SubElement(sub_node, "meta").text = generate_words(2, 4)
        nested = ET.SubElement(sub_node, "nested")
        ET.SubElement(nested, "data").text = generate_words(5, 10)

        if record_id % 50 == 0:
            xml_bytes = ET.tostring(root, encoding="utf-8")
            length_bytes = len(xml_bytes)
            print("Current length in bytes: ", length_bytes)

            if length_bytes >= target_bytes:
                break

        record_id += 1

    ET.indent(root, space="  ", level=0)
    ET.ElementTree(root).write(filename, encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    generate_xml("./samples/sample.xml", 2)
