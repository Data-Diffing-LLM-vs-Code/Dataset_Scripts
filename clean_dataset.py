from pathlib import Path

source_folder = Path("samples/cleaning/source")
removing_folder = "samples/cleaning/removing/"
accepted_folder = "samples/cleaning/accepted/"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"

files = list(source_folder.iterdir())
files.sort()
for file in files:
    print(f"{RED}Current File: {file}{RESET}")

    if file.stat().st_size < 1000:
        file.replace(removing_folder+"too_small/"+file.name)
        continue

    if not file.read_text(encoding="utf-8").isascii():
        file.replace(removing_folder+"not_ascii/"+file.name)
        continue

    file.replace(accepted_folder+file.name)