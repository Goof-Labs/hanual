class CompileManager:
    def __init__(self, tree) -> None:
        self._tree = tree

    def compile_priority(self):
        """
        CompilePriority is for nodes such as functions. This is because
        functions should be compiled at the start of the file and not
        the middle. The example shows how the tree wold be genorated
        without this.

        Instructions
        Instructions
        Instructions
        
        FUNCTION_1_ENTERY
        
        Function_instructions
        Function_instructions
        Function_instructions

        RET

        Instructions
        Instructions
        Instructions

        This is a clear problem, so instead of compiling functions in place
        we make a function [this function] that wil get all functions
        definitions and then compile then. Then everything else can be
        compiled.
        """

