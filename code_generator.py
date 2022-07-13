from __future__ import annotations
from line_data import LineData, CODE_CONVERTER_COMMANDS, DataCodes
from java_generation import JavaGenerator
from settings import Settings

DEBUG = True

class CodeGenerator:

    PYTHON_COMMENT_CODE_SIGNIFIER = "###"

    def __init__(self, from_language: str = "py3.10", to_language: str = "java") -> None:
        self._to_language = to_language
        self._from_language = from_language
        self.__input: str | None = None
        self.__code_lines = None
        self.__lines_tab_count = None
        self.__outputs: list[tuple[str, str]] | None = None

        self.__in_multiline_comment = False

        self.__line_data = None

    def input_code(self, code: list[str]) -> None:
        self.__input = code
        # code_lines = code.splitlines()
        self.__code_lines = []
        self.__lines_tab_count = [] 

        for line in code:
            if line.strip() == "":
                continue
            num_tabs = line.count("\t")
            self.__lines_tab_count.append(num_tabs)
            # self.__code_lines.append(line.replace("\t", ""))
            self.__code_lines.append(line.replace("\n", ""))
    
    def __pre_process_code(self) -> None:
        self.__line_data = []
        in_multiline_comment = False

        for line in self.__code_lines:
            line_data = LineData(line)
            if line_data.is_line(DataCodes.MUTLILINE_COMMENT_START):
                if in_multiline_comment:
                    line_data.set_multiline_end()
                    in_multiline_comment = False
                else:
                    in_multiline_comment = True
            self.__line_data.append(line_data)

            if DEBUG:
                print(f"{line_data.get_what_is_line().name} '{line_data.line}'")

    def __process_code(self) -> JavaGenerator:
        gen = None
        match self._to_language:
            case "java":
                gen = JavaGenerator(self.__line_data)
        return gen 

    def generate_output(self) -> None:
        if not self.__input:
            return

        self.__pre_process_code()
        gen = self.__process_code()
        code = gen.get_generated_code()

        # self.__output = "\n".join(code)
        self.__outputs = []

        '''
        code = [
            (
                [, , , ], # code lines
                class_name
            ), # EACH TUPLE IS A CLASS FILE

        ]
        '''
        
        for classes in range(len(code)):
            out = ""
            for c in code[classes][0]: 
                out += c + "\n"
            self.__outputs.append((out, code[classes][1]))

        if Settings.VERBOSE:
            for output in self.__outputs:
                print()
                print("FILE: " + output[1]+".java")
                print(output[0])
        

    def get_output(self) -> list[tuple[str, str]]:
        if not self.__input:
            return None
        if self.__outputs:
            return self.__outputs
        self.generate_output()
        return self.__outputs

    @staticmethod
    def recode(input: str, from_language: str = "py3.10", to_language: str = "java") -> None:
        gen = CodeGenerator(from_language=from_language, to_language=to_language)
        gen.input_code(input)
        return gen.output