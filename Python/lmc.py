Python 3.13.5 (tags/v3.13.5:6cb20a2, Jun 11 2025, 16:15:46) [MSC v.1943 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
>>> """
...     Riccardo Striano SM3201366
...     Programmazione Avanzata e Parallela - Progetto Python
...     Anno 2024-2025
... """
... from excpts import *
... 
... class ProgramCounter:
... 
...     """
...         Class for the ProgramCounter. It implements the addition as addition module 1000 and the branch as multiplication. 
...         If asking for the reason of this, the answer will be something vague about how cool it looks.
...     """
... 
...     def __init__(self):
...         self.__counter = 0
...     
...     def __add__(self, n): # Addition
...         if not isinstance(n, int):
...             print(f"Excepted an integer. {type(n)} received instead.")
...             raise BadOperandException
...         self.__counter = (self.__counter + n) % 1000
...         return self
...     
...     def __mul__(self, n): # Branch
...         if not isinstance(n, int):
...             print(f"Excepted an integer. {type(n)} received instead.")
...             raise BadOperandException
...         self.__counter = (n % 1000)
...         return self    
... 
...     def __str__(self):
...         return str(self.__counter)   
...     
...     def __lt__(self, n):
        return self.__counter < n

    def __gt__(self, n):
        return self.__counter > n
    
class Memory():

    """
        Class for the memory. it has a memory size fixed to 100. It can be initialized with a list. It only contains integer in the range [0 - 999]. 
        It implements both get and set item as if it was a simple list but checking for all the possible excpetion. 
        The Memory class is implemented to interacts well with  ProgramCounter objects. 
        At the end we also implement the asList method to return, when necessary, the memory as list.
    """

    def __init__(self, items = None):
        self.__items = [0]*100
        if items != None:
            if not isinstance(items, list):
                print("Need a list to initialize a Queque.")
                raise BadOperandException
            if len(items) > 100:
                print("Memory must be up to 100 size")
                raise BadOperandException
            for l in items:
                if not isinstance(l, int):
                    print("Need a list of integer to initialize a Memory.")
                    raise BadOperandException
                if l < 0 or l > 999:
                    print("Need a list of integer  in the range [0 - 999] to initialize a Memory.")
                    raise BadOperandException
            for i in range (len (items)):
                self.__items[i] = items[i]
    

    def __getitem__(self, k):
        if not isinstance(k, (int, ProgramCounter)):
            print("Index must be an integer or a Program Counter.")
            raise BadOperandException
        if k < 0 or k > 99:
            print("Index out of range. [range 0 - 99]")
            raise BadOperandException
        if isinstance(k, ProgramCounter):
            return self.__items[k._ProgramCounter__counter]
        return self.__items[k]

    def __setitem__(self, k, n):
        if not isinstance(n, int):
            print("Value must be an integer.")
            raise BadOperandException      
        if n < 0 or n > 999:      
            print("Value is either too small or too big [range 0 - 999].")
            raise BadOperandException   
        if not isinstance(k, (int, ProgramCounter)):
            print("Index must be an integer or a Program Counter.")
            raise BadOperandException
        if k < 0 or k > 99:
            print("Index out of range. [range 0 - 99]")
            raise BadOperandException  
        if isinstance(k, ProgramCounter):
            self.__items[k._ProgramCounter__counter] = n
        else:
            self.__items[k] = n

    def asList(self):
        return self.__items
    
class Queue():

    """
        Generic class for a Queue of integer in the range [0 - 999].
        It implements the usual append and pop methods. It also implements the append as an addition.
    """

    def __init__(self, items = None):
        self.__items = []
        if not items == None:
            if not isinstance(items, list):
                print("Need a list to initialize a Queque.")
                raise BadOperandException
            for l in items:
                if not isinstance(l, int):
                    print("Need a list of integer to initialize a Queque.")
                    raise BadOperandException
                if l < 0 or l > 999:
                    print("Need a list of integer  in the range [0 - 999] to initialize a Queque.")
                    raise BadOperandException
            self.__items = items
    
    def append(self, n):
        if not isinstance(n, int):
            print("Value must be an integer.")
            raise BadOperandException 
        if n < 0 or n > 999:
            print("Value must be an integer in the range [0 - 999]")
            raise BadOperandException  
        self.__items.append(n)

    def pop(self):
        if len(self.__items) == 0:
            print("Cannot pop from an empty queue.")
            raise BadOperandException
        return self.__items.pop(0)
    
    def __add__(self, n):
        self.append(n)
        return self
    
    def __str__(self):
        return str(self.__items)

class myLMC():

    """
        Class for the LMC.
        It has a Memory, an accumulator, a ProgramCounter, an input Queue, an output Queue, a flag and a working check.
        The use of them are well explained in the pdf. Working check is used for the computation.
        We access to the input Queue and the output Queue with get_input and result. 
    """

    def __init__(self, memory, input_q = None): # input as list !!
        self.__memory = Memory(memory)
        self.__accumulator = 0
        self.__program_counter = ProgramCounter()
        self.__input_queue = Queue(input_q)
        self.__output_queue = Queue()
        self.__flag = 0 
        self.__working = True

    def __add__(self, k):
        """
            Perform an addition of the accumulator module 1000. 
            It also set the flag to true if an overflow occurred.
        """
        self.__accumulator = self.__accumulator + self.__memory[k]
        self.__flag = self.__accumulator > 999
        self.__accumulator = self.__accumulator%1000
    
    def __sub__(self, k):
        """
            Perform a subtraction of the accumulator module 1000. 
            It also set the flag to true if an underflow occurred.
        """
        self.__accumulator = self.__accumulator - self.__memory[k]
        self.__flag = self.__accumulator < 0
        self.__accumulator = self.__accumulator%1000

    def __store(self, k):
        """
            Store the accumulator value at the memory cell of the given index. 
        """
        self.__memory[k] = self.__accumulator
    
    def __load(self, k):
        """
            Load the value at the memory cell of the given index into the accumulator. 
        """
        self.__accumulator = self.__memory[k]
    
    def __branch(self, k):
        """
            Branch of the program counter. 
        """
        self.__program_counter*=k # Branch
        self.__program_counter+=(-1) # i will increment it later so we decrement it now
    
    def __branch_ifzero(self, k):
        """
            Branch if zero of the program counter. 
        """
        if not self.__flag and self.__accumulator == 0:
            self.__branch(k)

    def __branch_ifpositive(self, k):
        """
            Branch if positive of the program counter. 
        """
        if not self.__flag:
            self.__branch(k)
    
    def __input(self):
        """
            Input action : load the head of the input queue into the accumulator. 
        """
        self.__accumulator = self.__input_queue.pop()
    
    def __output(self):
        """
            Output action : append at the head of the output queue the value of the accumulator. 
        """
        self.__output_queue += self.__accumulator
    
    def __halt(self, k):
        """
            Halt. Stop the working flow.
        """
        self.__working = False
    
    def work(self, verbose = False, slow = False, one_step = False):
        """

            Core method of the Little Man Computer. It performs the simulation 
            of the LMC Architecture. 

            Parameters : 
                verbose (Bool): if True print the status of the lmc while working
                slow (Bool) : if True set a 0.5 second deelay per cycle     
        """
        import time
        while self.__working:
            if slow:
                time.sleep(0.5)
            if one_step:
                keep = input()
            instruction = self.__memory[self.__program_counter]
            radix = instruction//100
            index = instruction%100
            
            if verbose :
                print(f"Doing instruction {instruction}. Accumulator rn at {self.__accumulator}. Program counter rn at {self.__program_counter}.")
            
            if instruction == 901:
                self.__input()
            elif instruction == 902:
                self.__output()
            else:
                if radix == 0:
                    self.__halt(index)
                elif radix == 1:
                    self.__add__(index)
                elif radix == 2:
                    self.__sub__(index)
                elif radix == 3:
                    self.__store(index)
                elif radix == 5:
                    self.__load(index)
                elif radix == 6:
                    self.__branch(index)
                elif radix == 7:
                    self.__branch_ifzero(index)
                elif radix == 8:
                    self.__branch_ifpositive(index)
                else:
                    raise IllegalInstructionException
            self.__program_counter += 1
            if verbose :
                print(f" |-Instruction {instruction} is done. Accumulator rn at {self.__accumulator}. Program counter rn at {self.__program_counter}.")
        
    
    def result(self):
        return self.__output_queue

    def get_input(self):
        return self.__input_queue
    
if __name__ == "__main__":

    Kevin = myLMC(memory = [901, 310, 901, 110, 902, 0], input_q = [2, 3])
    Kevin.work(verbose=True)
