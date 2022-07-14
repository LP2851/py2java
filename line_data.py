import re
from enum import Enum, auto

CODE_CONVERTER_COMMANDS = {
    "###STATIC",
    "###OVERRIDE",
    "###ABSTRACT"
}

class DataCodes(Enum):
    UNKNOWN = auto()

    CONVERTER_CODE_COMMENT = auto()
    
    COMMENT = auto()
    MUTLILINE_COMMENT_START = auto()
    MUTLILINE_COMMENT_END = auto() 

    IMPORT = auto()
    IMPORT_COMPLEX = auto()
    
    CLASS_DEF = auto()
    FUNC_DEF = auto()
    VAR_DEF = auto()
    VAR_REASSIGN = auto()
    FUNC_CALL = auto()

    FOR_LOOP = auto()
    WHITE_LOOP = auto()
    IF_STATEMENT = auto()
    ELIF_STATEMENT = auto()
    ELSE_STATEMENT = auto()

    PASS_KEYWORD = auto()

    ANNOTATION = auto()

    

class LineData: 

    def __init__(self, line: str) -> None:
        self.line = line
        self.__what_is_line: int = self.__discover_line_type()

    @staticmethod
    def __check_is_converter_code_comment(line: str) -> bool:
        return line.strip() in CODE_CONVERTER_COMMANDS
    
    @staticmethod
    def __check_is_comment(line: str) -> bool:
        return line.strip().startswith("#")
    
    @staticmethod
    def __check_is_multiline_comment(line: str) -> bool:
        return line.strip().startswith("'''") or line.strip().startswith('"""')
    
    @staticmethod
    def __check_is_import(line: str) -> bool:
        return line.strip().startswith("import ")

    def __check_is_complex_import(line: str) -> bool:
        # regex = ""
        # return re.match(regex, line.strip())
        return False

    @staticmethod
    def __check_is_class_def(line: str) -> bool:
        regex = "class [a-zA-Z0-9]+(\([a-zA-Z0-9]*\))?:"
        return re.match(regex, line.strip())

    @staticmethod
    def __check_is_pass_keyword(line: str) -> bool:
        return line.strip() == "pass"

    @staticmethod
    def __check_is_annotation(line: str) -> bool:
        regex = "@[a-zA-Z0-9]+"
        return re.match(regex, line.strip())

    

    __CHECK_FUNCTIONS = {
        __check_is_converter_code_comment: DataCodes.CONVERTER_CODE_COMMENT,
        __check_is_comment: DataCodes.COMMENT,
        __check_is_multiline_comment: DataCodes.MUTLILINE_COMMENT_START,
        __check_is_import: DataCodes.IMPORT,
        __check_is_complex_import: DataCodes.IMPORT_COMPLEX,
        __check_is_class_def: DataCodes.CLASS_DEF,    
        __check_is_pass_keyword: DataCodes.PASS_KEYWORD,    

        __check_is_annotation: DataCodes.ANNOTATION,
    }

    def get_num_tabs(self) -> int:
        return self.line.count("\n")
    
    def set_what_is_line(self, what_is_line: int= DataCodes.UNKNOWN) -> None:
        self.__what_is_line = what_is_line

    def get_what_is_line(self) -> DataCodes:
        return DataCodes(self.__what_is_line)

    def set_multiline_end(self) -> None:
        self.__what_is_line =  DataCodes.MUTLILINE_COMMENT_END

    def __discover_line_type(self) -> int:
        for func, val in self.__CHECK_FUNCTIONS.items():
            if func(self.line):
                return val
        return DataCodes.UNKNOWN

    def is_known_line_type(self) -> bool:
        return self.__what_is_line == DataCodes.UNKNOWN

    def is_line(self, line_type: int) -> bool:
        return self.__what_is_line == line_type