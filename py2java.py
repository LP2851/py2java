import sys
import os.path
from code_generator import CodeGenerator
import generate_java

def is_valid_file(filename: str) -> bool:
    if not filename.endswith(".py"):
        return False
    if not os.path.exists(filename):
        return False
    return True

def validate_python_files(filenames: list[str]) -> list[str]:
    valid_files = []
    for file in filenames:
        if is_valid_file(file):
            valid_files.append(file)
            print(f"[FILE VALID] :: {file}")
            continue
        print(f"[FILE INVALID] :: '{file}' is invalid and was ignored.")
    return valid_files

def get_file_data(file: str) -> list[str]:
    out = ""
    with open(file, "r") as f:
        out = f.readlines()
    return out

def main(files_to_convert: list[str]) -> None:
    files_to_convert = validate_python_files(files_to_convert)

    # generate_java.JavaGenerator.run("Main")
    code_gen = CodeGenerator()
    code_gen.input_code(get_file_data(files_to_convert[0]))
    code_gen.generate_output()


if __name__ == "__main__":
    files_to_convert = sys.argv[1:]
    main(files_to_convert)

