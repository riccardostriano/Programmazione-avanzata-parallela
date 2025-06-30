Python 3.13.5 (tags/v3.13.5:6cb20a2, Jun 11 2025, 16:15:46) [MSC v.1943 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
>>> """
...     Riccardo Striano SM3201366
...     Programmazione Avanzata e Parallela - Progetto Python
...     Anno 2024-2025
... """
... 
... from excpts import *
... from lmc import Memory
... 
... class OperationsTranslator():
...     """
...         Specific translator class to perform the translation between an assembly instruction and 
...         its radix value in machine code. It works only for LMC architecture. It implements the
...         get item handling exception.
...     """
...     def __init__(self):
...         self.__operations = {'ADD' : 100, 'SUB' : 200, 'STA' : 300, 'LDA' : 500, 'BRA' : 600, 'BRZ' : 700, 'BRP' : 800, 'INP' : 901, 'OUT' : 902, 'HLT':0, 'DAT' : 0}
...     
...     def __getitem__(self, key):
...         if key not in self.__operations.keys():
...             print("Not a valid key.")
...             raise BadOperandException
...         return self.__operations[key]
...         
... class myAssembler():
...     """
...         Specific class for the Assembler of the assembly described in the pdf.
...         It represents the instructions as list and asks for the path of the file containing them.
...         It preprocess the instructions removing comments and blank line.
...         Bad Operations are handled by the class under the IllegalOperationException.
...         It prepocess the labels.
        Once created automatically assemble the machine code.
        All the methods just described are private.
        To get access to the machine code generate must call the get_memory.
    """
    def __init__(self, instructions_path):
        self.__operations = ['ADD', 'SUB', 'STA', 'LDA', 'BRA', 'BRZ', 'BRP', 'INP', 'OUT', 'HLT', 'DAT']
        self.__instructions = self.__instruction_from_file(instructions_path)
        if len(self.__instructions) > 100:
            print("There are too many instructions")
            raise BadOperandException
        self.__preprocess_instructions()
        self.__labels = {}
        self.__preprocess_labels()
        self.__memory = Memory()
        self.__assemble()
        
    def __instruction_from_file(self, path):
        """
            Load the instructions from a given file. Removes blank lines and comment-only lines.
            
            Parameters:
                path (str) : path of the instructions_file.
            
            Returns:
                (list) Instructions as list
        """
        file = open(path, 'r')
        instructions = file.read().split("\n")
        actual_instructions = []
        for instr in instructions:
            if instr.split() == []:
                continue
            if instr.split()[0] == "//":
                continue
            actual_instructions.append(instr)
        return actual_instructions

    def __preprocess_instructions(self):
        """
            Given the instructions list remove all the comments.
        """
        for i, instruction in enumerate(self.__instructions):
            comment_index = instruction.find("//")
            if comment_index != -1:
                self.__instructions[i] = self.__instructions[i][:comment_index]
            self.__instructions[i] = self.__instructions[i].upper()

    def __preprocess_labels(self):
        """
            Given the instructions list find the index for every label.
        """
        for i, instruction in enumerate(self.__instructions):
            components = instruction.split()
            if len(components) == 3:
                self.__labels[components[0]] = i
            if len(components) == 2 and components[1] in self.__operations:
                self.__labels[components[0]] = i
    
    def __assemble(self):
        """
            Core method of the class. It takes the operations and assembles the machine code.
            It follows straight forward what is explained in the pdf.
        """
        for i, instruction in enumerate(self.__instructions):
            components = instruction.split()
            op, idx = '', '' # the operation is divided in operation and index 
            label_op = False # check if a label is present or not as operation index
            if len(components) == 3: # LABEL OPERATION INDEX/LABEL
                op = components[1]
                idx = components[2]
            if len(components) == 2 and components[1] in self.__operations: # LABEL OPERATION
                op = components[1]
                idx = '0'
            if len(components) == 2 and components[0] in self.__operations: # OPERATION INDEX/LABEL
                op = components[0]
                idx = components[1]
            if len(components) == 1: # OPERATION
                op = components[0]
                idx = '0'
            if len(components) == 0: # ---
                break
            if idx in self.__labels.keys(): # TO UNDERSTAND IF IDX IS A REAL INDEX OR A LABEL
                label_op = True
            elif not idx.isnumeric():
                print("Label not defined.")
                raise IllegalOperationException
            translator = OperationsTranslator()
            op_value = translator[op] 
            idx_value = self.__labels[idx] if label_op else int(idx) # IT DEPENDS ON THE LABEL_OP 
            self.__memory[i] = op_value + int(idx_value) # the actual memory : the radix value of the operation plus the index value
    
    def get_memory(self):
        return self.__memory.asList()

if __name__ == "__main__":

