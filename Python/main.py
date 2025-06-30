Python 3.13.5 (tags/v3.13.5:6cb20a2, Jun 11 2025, 16:15:46) [MSC v.1943 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
from lmc import *
from assembler import *
import argparse

"""
    Riccardo Striano
    Programmazione Avanzata e Parallela - Progetto Python
    Anno 2024-2025
"""

def parse_list_of_ints(value):
    try:
...         print(value.split(","))
...         for i in value.split(","):
...             y = int(i)
...             if y < 0 and y >= 1000:
...                 raise argparse.ArgumentTypeError(f"'{value}' is not a valid list of integers in the range [0-999]")
...         return [int(i) for i in value.split(",")]
...     except ValueError:
...         raise argparse.ArgumentTypeError(f"'{value}' is not a valid list of integers")
... 
... def main(path, verbose, input_q, slow, one_step):
...     instructions_path = path
...     Louis = myAssembler(instructions_path)
...     Logan = myLMC(memory=Louis.get_memory(),input_q=input_q)
...     Logan.work(verbose, slow, one_step)
...     print(f"Input Queue : {Logan.get_input()}")
...     print(f"Output Queue: {Logan.result()}")
... 
... if __name__ == "__main__":
... 
...     parser = argparse.ArgumentParser(description="Argparser for LMC")
...     parser.add_argument("-path", type=str, default='lmc_test/reverse.lmc', 
...                         help="Path of the Assembly code. (default: lmc_test/reverse.lmc)")
...     parser.add_argument("-verbose", type=bool, default=False, 
...                         help="Activate verbose mode. (default: False)")
...     parser.add_argument("-slow", type=bool, default=False, 
...                         help="Activate slow mode. (default: False)")
...     parser.add_argument("-one_step", type=bool, default=False, 
...                         help="Activate one_step mode. (default: False)")
...     parser.add_argument("-input_q", type=parse_list_of_ints, default = [1, 2, 3, 0], 
...                         help="Input queue for the LMC. (default: [1, 2, 3, 0])")
...     args = parser.parse_args()
...     
...     main(path=args.path, verbose=args.verbose, input_q=args.input_q, slow=args.slow, one_step=args.one_step)
... 
