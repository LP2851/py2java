import sys
import os.path
from os import makedirs
from code_generator import CodeGenerator
import generate_java
from settings import Settings

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

def save_to_file(code:str, class_name:str,) -> None:
    if not os.path.exists(Settings.OUTPUT_FOLDER_NAME):
        makedirs(Settings.OUTPUT_FOLDER_NAME)
    with open(f"{Settings.OUTPUT_FOLDER_NAME}{class_name}.java", "w") as f:
        f.write(code)


def main(files_to_convert: list[str]) -> None:
    files_to_convert = validate_python_files(files_to_convert)

    # generate_java.JavaGenerator.run("Main")
    code_gen = CodeGenerator()
    code_gen.input_code(get_file_data(files_to_convert[0]))
    out = code_gen.get_output() # list[tuple[code, class_name]]

    # logic for moving between classes/files
    code, class_name = out[0] 
    save_to_file(code, class_name)


if __name__ == "__main__":
    files_to_convert = sys.argv[1:]
    main(files_to_convert)

