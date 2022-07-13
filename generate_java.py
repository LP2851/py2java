
class JavaGenerator2:
    def __init__(self, code: list[str], is_file_path: bool=False, class_name: str=None) -> None:
        self.__tab_index = 0
        self.__class_name = class_name

        self.code_py = code if not is_file_path else JavaGenerator2.get_code_from_file(code)

    @staticmethod
    def get_code_from_file(file: str) -> list[str]:
        code = []
        with open(file, "r") as f:
            code = f.readlines()
        return code

    def generate(self):
        for line in self.code_py:
            # if is class 
            pass
    

class JavaGenerator:
    def __init__(self, class_name: str) -> None:
        self.__tab_index = 0
        self._class_name = class_name
        self.__java = ""
    
    @staticmethod
    def run(class_name: str, code=None):
        generator = JavaGenerator(class_name)
        generator.__generate_class()
        print(generator.__java)

    def output_file(self) -> None:
        with open(f"{self._class_name}.java", "w") as f:
            f.write(self.__java)
        

    def __add_line(self, code: str="") -> None:
        if len(code) != 0:
            if code[-1] == "{":
                code = self.__generate_tabs() + code
                self.__tab_index += 1
            elif code[-1] == "}":
                self.__tab_index -= 1
                code = self.__generate_tabs() + code
            elif code[-1] != ";":
                code = self.__generate_tabs() + code + ";"
            else:
                code = self.__generate_tabs() + code
        
        code += "\n"
        self.__java += code

    def __add_func_close(self) -> None:
        self.__add_line("}")
        
    def __generate_class(self) -> None:
        self.__generate_class_start()
        self.generate_main_method("")
        self.__add_func_close()

    def __generate_class_start(self):
        self.__add_line(f"public class {self._class_name} " + "{")

    def generate_main_method(self, code) -> str:
        self.__add_line()
        self.__add_line("public static void main(String[] args) {")

        # code here
        self.__add_line(JavaGenerator.generate_simple_print_statement("Hello World"))
    
        self.__add_func_close()

    @staticmethod
    def generate_simple_print_statement(print_string: str) -> str:
        return f'System.out.println("{print_string}");'

    def __generate_tabs(self) -> str:
        return "\t" * self.__tab_index
    