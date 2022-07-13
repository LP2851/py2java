class Settings:
    '''
    Class for all of the settings values that will be turned into arguments later on.
    
    Additional New Lines Settings:
        NEWLINES_BEFORE_COMMENT_BLOCK:          Adds a newline before each comment block
        NEWLINES_BEFORE_CLASSES_AND_FUNCTIONS:  Adds a newline before each class definition/function definition line

    Output Settings:
        VERBOSE:                                Makes the program show stuff as it happens 
        OUTPUT_FOLDER_NAME                      The location the .java files will be outputted to

    Extra Comments in Files:
        CREATE_SOURCE_COMMENT:                  Adds a comment at the top of each document saying where the code came from
    '''

    # Additional New Lines Settings:
    NEWLINES_BEFORE_COMMENT_BLOCK = True
    NEWLINES_BEFORE_CLASSES_AND_FUNCTIONS = True

    # Output Settings:
    VERBOSE = True
    OUTPUT_FOLDER_NAME = "./out/" 

    # Extra Comments in Files:
    CREATE_SOURCE_COMMENT = True