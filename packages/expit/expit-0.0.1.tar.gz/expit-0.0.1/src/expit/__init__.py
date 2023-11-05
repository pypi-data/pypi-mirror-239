import math as _math

import wonderparse as _wp


def function(x:float):
    return 1 / (1 + _math.exp(-x))

def main(args=None):
    _wp.easymode.simple_run(
        args=args,
        program_object=function,
        prog='expit',
    )
    
if __name__ == '__main__':
    main() 
