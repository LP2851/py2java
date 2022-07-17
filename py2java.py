import sys
import os.path
from os import makedirs
from code_generator import CodeGenerator
import generate_java
from settings import Settings


def is_valid_file(file_path: str) -> bool:
    """
    Validates that the passed file is a Python file and exists.
    :param file_path: The file path that needs to validated. 
    :return: If the passed file is valid
    :rtype: bool
    """
    if not file_path.endswith(".py"):
        return False
    if not os.path.exists(file_path):
        return False
    return True

def validate_python_files(file_paths: list[str]) -> list[str]:
    """
    Takes a list of file paths inputted by the users and returns all of the valid Python file paths. 
    :param file_paths: A list of file paths inputted by the user
    :return: List of all valid file paths from the ones that were passed. 
    :rtype: list[str]  
    """
    valid_files = []
    for file in file_paths:
        if is_valid_file(file):
            valid_files.append(file)
            print(f"[FILE VALID] :: {file}")
            continue
        print(f"[FILE INVALID] :: '{file}' is invalid and was ignored.")
    return valid_files

def get_file_data(file: str) -> list[str]:
    """
    Gets all of the data from the file.
    :param file: The path to the file to be openned and read. 
    :return: The file's content. 
    :rtype: list[str] 
    """
    out = ""
    with open(file, "r") as f:
        out = f.readlines()
    return out

def save_to_file(code: str, class_name: str, source_file: str) -> None:
    """
    Saves the generated code to a new file. 
    :param code: The generated code
    :param class_name: Name of the class (for the name of the file). 
    :source_file: The name of the file the code was generated from. 
    """
    # If the directory doesnt exist then it is created. 
    if not os.path.exists(Settings.OUTPUT_FOLDER_NAME):
        makedirs(Settings.OUTPUT_FOLDER_NAME)
    # Writing the code
    with open(f"{Settings.OUTPUT_FOLDER_NAME}{class_name}.java", "w") as f:
        final_code = "/// Created Using: py2java By LP2851\n"
        if Settings.CREATE_SOURCE_COMMENT:
            final_code += f"/// Source File: {source_file}\n"
        final_code += code
        f.write(final_code)


def main(files_to_convert: list[str]) -> None:
    """
    Generates code for all valid files and then creates the needed files based on the code. 
    :param files_to_convert: The list of string paths for files to be converted (sys.argv[1:]).
    """
    files_to_convert = validate_python_files(files_to_convert)

    # generate_java.JavaGenerator.run("Main")
    code_gen = CodeGenerator()
    code_gen.input_code(get_file_data(files_to_convert[0]))
    out = code_gen.get_output() # list[tuple[code, class_name]]

    # logic for moving between classes/files
    for (code, class_name) in out:
        save_to_file(code, class_name, files_to_convert[0])



if __name__ == "__main__":
    files_to_convert = sys.argv[1:]
    main(files_to_convert)

