from dotenv import load_dotenv
from datasets import load_dataset
import random

load_dotenv()
ds = load_dataset("bigcode/the-stack", data_dir="data/xml", split="train", streaming=True)
ds_meta = ds.select_columns(["size"])

i = 0

for row in ds_meta:
    if i % 50 == 0:
        print(f"Checked {i} files...")

    if row["size"] >= 2 * 1024 * 1024:
        sample = next(iter(ds.skip(i)))
        filename = f"./samples/sample_{random.randint(1000000, 9999999)}.xml"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(sample["content"])
        print(f"Saved to {filename} successfully!")
    i += 1