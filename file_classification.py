from pathlib import Path
import ollama
from itertools import islice

folder = Path("samples/classification/source")
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"

files = list(folder.iterdir())
files.sort()
for file in files:
    print(f"{RED}Current File: {file}{RESET}")

    with open(file, "r", encoding="utf-8") as f:
        first_30_lines = "".join(islice(f, 30))

    response = ollama.chat(
        model="gemma4:e2b",
        messages=[
            {
                "role": "system",
                "content": """
                    You are a helpful categorisation assistant. You will be provide with the beginnen of an XML
                    Document and you should decide between the following three categories: 
                    - Self Descriptive: A file with content that is understandable without external knowledge. An
                    Example of this would be a file that contains a root tag named "users" and child tags named
                    "user" with attributes like "name", "email", and "age".

                    - Schema Driven: A file that features element tags and attributes that are not understandable
                    without external knowledge. This external knowledge could be a schema or rules defined by an
                    organization. An example of this would be an EDIFACT file that was converted to XML and thus
                    included tags like "UNH", "BGM", and "DTM" with attributes like "C506" and "C507". The file 
                    uses vocabulary that is not understandable without external knowledge that defines this new 
                    vocabulary.

                    - Schema Describing: A file that does not hold data but instead describes the structure of other
                    files that are intended to hold data. An example of this would be an XSD file that contains tags
                    like "xs:element" and "xs:complexType" with attributes like "name", "type", and "minOccurs". 
                    The meaning of these tags and attributes is understandable without external knowledge, but the 
                    file does not hold data itself.

                    Although files like UI definitions or configuration files follow rules defined by an external
                    actor, they are not considered schema driven since they typically use human language. This means
                    that a schema driven file can be differentiated from self descriptive file if it uses IDs instead of
                    meaningful words. A self descriptive file for example would use terms like "component", "task", 
                    "servers" and "clients" while a schema driven file would use IDs for each of these terms. These IDs
                    would then be explained in an external document. 
                    
                    Classify the XML fragment into exactly one category! If the evidence is insufficient and you are 
                    unsure, respond with "evidence_insufficient" and do not invent external standards! ONLY respond 
                    with one of these four words: "self_descriptive", "schema_driven", "schema_describing", or 
                    "evidence_insufficient".
                    """
            },
            {
                "role": "user",
                "content": f"""
                    Here is you XML fragment to classify:
                    {first_30_lines}

                    Note the established rules and analyze this snippet step by step. Respond only with the most fitting
                    category from the four options provided. Do not provide any additional commentary or explanation!
                    """,
            },
        ],
        think=True,
        options={"temperature": 0.1, "num_ctx": 16384},
    )

    print(f"{GREEN}Input: {first_30_lines}{RESET}")

    if "thinking" in response["message"]:
        print(f"{BLUE}Thinking: {response["message"]["thinking"]}{RESET}")
    else:
        print(f"{BLUE}No thinking information available.{RESET}")

    predicted_category = response["message"]["content"].strip().lower()
    print(f"{YELLOW}Category: {predicted_category}{RESET}")

    if predicted_category == "self_descriptive":
        file.replace("samples/classification/self_descriptive/"+file.name)
    elif predicted_category == "schema_driven":
        file.replace("samples/classification/schema_driven/"+file.name)
    elif predicted_category == "schema_describing":
        file.replace("samples/classification/schema_describing/"+file.name)
    elif predicted_category == "evidence_insufficient":
        file.replace("samples/classification/evidence_insufficient/"+file.name)
