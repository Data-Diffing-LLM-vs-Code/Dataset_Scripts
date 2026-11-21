from datasets import load_dataset
from dotenv import load_dotenv

load_dotenv()

ds = load_dataset("bigcode/the-stack", data_dir="data/xml", split="train", streaming=True)

i = 1000

for row in ds:
    if i == 2000:
        break

    if row["size"] >= 3072:
        filename = f"./samples/downloads/{i}.xml"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(row["content"])
        print(f"Saved to {filename} successfully!")
        i += 1