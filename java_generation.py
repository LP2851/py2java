from line_data import DataCodes, LineData, CODE_CONVERTER_COMMANDS
from settings import Settings
import re

class CodeBlock:
    PUBLIC = 0
    PROTECTED = 1
    PRIVATE = 2

    def add_line(self, line: LineData) -> bool:
        pass

    def generate_code(self) -> list[str]:
        pass

    def is_complete(self) -> bool:
        return True

class JavaPassBlock(CodeBlock):
    def __init__(self) -> None:
        pass

    def add_line(self, line: LineData) -> bool:
        return True

    def generate_code(self) -> list[str]:
        return [""]

class JavaImportBlock(CodeBlock):

    __BASE_TYPES = {
        dict: "java.util.HashMap",
        list: "java.util.ArrayList",
        set: "java.util.HashSet",
    }

    def __init__(self) -> None:
        self.code_lines: list[LineData] = list()
        self.__other_imports = set()

    def add_import_for_type(self, _type: type) -> None:
        self.__other_imports.add(_type)

    def add_line(self, line: LineData) -> bool:
        self.code_lines.append(line)
        return True

    def generate_code(self) -> list[str]:
        return ["// WIP: IMPORTS CODE"]


class JavaCommentBlock(CodeBlock):
    COMMENT = "// "
    COMMENT_MULTI = "///"

    def __init__(self, comment:str=None, tabs:int=0) -> None:
        self.__comment: list[str | LineData] = [] if comment is None else [comment]
        self.__tabs = tabs
        # BEWARE comment list can contain both strings and LineData objects

    def add_line(self, line: LineData) -> bool:
        self.__comment.append(line)
        return True

    def is_complete(self) -> bool:
        if len(self.__comment) == 1:
            return type(self.__comment[0]) is str
        
        if type(self.__comment[-1]) is LineData:
            return self.__comment[-1].get_what_is_line() is DataCodes.MUTLILINE_COMMENT_END
        return False 
            

    def generate_code(self) -> list[str]:
        if len(self.__comment) == 1:
            c = self.__comment[0]
            if type(c) is LineData: 
                c = c.line
            tabs = c.count("\t") + self.__tabs
            c = c.strip().removeprefix("#")
            return ["\t" * tabs + f"{self.COMMENT} {c}"]

        out = []
        if Settings.NEWLINES_BEFORE_COMMENT_BLOCK:
            out.append("")
        for c in self.__comment:
            comment = c
            if type(c) is LineData: 
                if c.get_what_is_line() in [DataCodes.MUTLILINE_COMMENT_START, DataCodes.MUTLILINE_COMMENT_END]:
                    continue
                comment = comment.line
            tabs = comment.count("\t") + self.__tabs
            comment = comment.strip().removeprefix("#")
            out.append("\t" * tabs + f"{self.COMMENT_MULTI} {comment}")
        return out


class JavaClassBlock(CodeBlock):
    __Class_Regex = "class [a-zA-Z0-9]+(\([a-zA-Z0-9]*\))?:"

    def __init__(self, importer) -> None:
        self.code_lines: list[LineData] = list()
        self.blocks: list[CodeBlock] = list()
        self.__tab_count = -1
        self.__importer = importer

        self.__current_block: CodeBlock = None

        self.__is_static = False
        self.__is_abstract = False
        self.__visability = 0
        
        self.__is_complete = False

        self.class_name = ""
        self.__class_parent = ""
        

    @staticmethod
    def __get_class_details(code: str) -> tuple[str, str | None]:
        class_name_and_beyond = code.split(" ")[1]
        class_name_and_beyond = class_name_and_beyond.replace(":", "").replace(")", "").replace("(", " ")
        class_name_and_inherit = class_name_and_beyond.split(" ")
        if len(class_name_and_inherit) == 2:
            [class_name, inherit] = class_name_and_inherit
            return class_name, inherit
        return class_name_and_inherit[0], None

    def add_line(self, line: LineData) -> bool:
        is_start_line = False
        if self.__tab_count == -1:
            self.__tab_count = line.get_num_tabs()
            is_start_line = True
            if self.__tab_count == 0:
                self.__importer = JavaImportBlock()
                
        if not is_start_line:
            if not line.get_num_tabs() >= self.__tab_count:
                self.is_complete = True
                return False

        
        if self.__is_complete:
            if line.get_what_is_line() not in [DataCodes.COMMENT, DataCodes.MUTLILINE_COMMENT_START, DataCodes.MUTLILINE_COMMENT_END]:
                return False

        # CHECKS FOR COMMENT COMMANDS

        # HANDS OFF TO CURRENT BLOCK IF IN USE
        if self.__current_block:
            if not self.__current_block.is_complete():
                return self.__current_block.add_line(line)
        
        # CHECK IS PASS
        if line.get_what_is_line() is DataCodes.PASS_KEYWORD:
            self.blocks.append(JavaPassBlock())
            self.code_lines.append(line)
            return True

        # CHECK IS CLASS DEF
        if line.get_what_is_line() is DataCodes.CLASS_DEF:
            if self.class_name != "":
                return False
            self.class_name, self.__class_parent = self.__get_class_details(line.line.strip())
            self.code_lines.append(line)
            return True
        # CHECK IS FUNC DEF
        # CHECK IS VARIABLE DEF
        # CHECK IS UNKNOWN
        # CHECK IS COMMENT/BLOCK
        if line.get_what_is_line() is DataCodes.COMMENT:
            self.blocks.append(JavaCommentBlock(line.line, self.__tab_count+1))
            self.code_lines.append(line)
            return True

        if line.get_what_is_line() is DataCodes.MUTLILINE_COMMENT_START:
            self.__current_block = JavaCommentBlock(tabs=self.__tab_count+1)
            self.blocks.append(self.__current_block)
            self.__current_block.add_line(line)
            return True
        

        print("#################### Something is wrong ")
        return False

    def __generate_class_def(self) -> str:
        out = "\t" * self.__tab_count
        match self.__visability:
            case CodeBlock.PUBLIC:
                out += "public "
            case CodeBlock.PROTECTED:
                out += "protected "
            case CodeBlock.PRIVATE:
                out += "private "
        if self.__is_abstract:
            out += "abstract "
        
        if self.__is_static:
            out += "static "
        
        out += "class " + self.class_name + " "

        if self.__class_parent:
            out += "extends " + self.__class_parent + " "
        
        return out + "{"


    def generate_code(self) -> list[str]:
        out = []
        if self.__tab_count == 0:
            out += self.__importer.generate_code()

        if Settings.NEWLINES_BEFORE_CLASSES_AND_FUNCTIONS:
            out.append("")
        out += [self.__generate_class_def()]

        for block in self.blocks:
            block_output = block.generate_code()
            out += block_output

        out += ["\t" * self.__tab_count + "}"]
        return out
        
        
'''
# class JavaClassCodeBlock(CodeSegment):

#     __Class_Regex = "class [a-zA-Z0-9]+(\([a-zA-Z0-9]*\))?:"

#     def __init__(self, code: list[str]) -> None:
#         super().__init__(self)
#         self.code = code
#         self.class_name = ""
#         self.class_inherits = None
#         self.__privacy = 0
#         self.__is_static = False

#         self.segments: list[CodeSegment] = []

#         self.__out: list[str] | None = None

#     def decode(self) -> None:
#         for line in self.code:
#             # If has py2java comment "###STATIC" then becomes static
#             if re.match(line.strip(), self.__STATIC_CUSTOM_Regex):
#                 self.__is_static = True
#                 continue
#             # If is class line 
#             if re.match(line.strip(), self.__Class_Regex):
#                 self.decode_class_line(line)
#                 continue
            

#     def get_output(self) -> list[str]:
#         if self.__out:
#             return self.__out
        
#         self.construct_output()
#         return self.__out

#     def construct_output(self) -> None:
#         self.__out = []


#     def decode_class_line(self, line) -> None:
#         self.class_name, self.class_inherits = self.__get_class_details(line)

            
#     @staticmethod
#     def __get_class_details(code: str) -> tuple[str, str | None]:
#         class_name_and_beyond = code.split(" ")[1]
#         class_name_and_beyond = class_name_and_beyond.replace(":", "").replace(")", "").replace("(", " ")
#         class_name_and_inherit = class_name_and_beyond.split(" ")
#         if len(class_name_and_inherit) == 2:
#             [class_name, inherit] = class_name_and_inherit
#             return class_name, inherit
#         return class_name, None
'''

class JavaGenerator:

    COMMENT_PREFIX = "// "
    TODO_PREFIX = "TODO: "

    def __init__(self, line_data: list[LineData], auto_run_processing:bool=True) -> None:
        self.__code: list[LineData] = line_data
        self.__import_block = JavaImportBlock()
        self.__code_segments = list()

        if auto_run_processing:
            self.process_code()

    def process_code(self) -> None:
        current_block: CodeBlock = None
        unclaimed_modifers: list[LineData] = list()
        for line in self.__code:
            what_is_line = line.get_what_is_line()
            
            
            if what_is_line == DataCodes.IMPORT:
                self.__import_block.add_line(line)
                continue
            if current_block:
                if current_block.add_line(line): 
                    continue
            current_block = None
            # UNKNOWN
            if what_is_line is DataCodes.UNKNOWN:
                segment = JavaCommentBlock(self.TODO_PREFIX + line.line)
                self.__code_segments.append(segment)
                continue

            # CLASS
            if what_is_line is DataCodes.CLASS_DEF:
                current_block = JavaClassBlock(self.__import_block)
                self.__code_segments.append(current_block)
                if not current_block.add_line(line):
                    print("SOMETHING WENT HORRIBLY WRONG")
                    print(line.line)
                    return
                continue
            # FUNCTION
            # VARIABLE
            # MODIFIER
            # COMMENT/BLOCK
            
         
    def get_generated_code(self) -> list[tuple[str, str]]:
        # out = self.__import_block.generate_code()
        out = []
        current_block = None
        missing_blocks = set()
        first_class = None
        for block in self.__code_segments:
            if type(block) is JavaClassBlock:
                current_block = block
                if not first_class:
                    first_class = current_block
                out.append((block.generate_code(), current_block.class_name))
                continue
            if not current_block:
                missing_blocks.add(len(out))
                out.append((block.generate_code(), None))
                continue
            out.append((block.generate_code(), current_block.class_name))

        
        for block in missing_blocks:
            code, _ = out[block]
            out[block] = (code, first_class)

        
        return out
