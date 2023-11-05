import wonderparse as _wp

_values = {
    'A':1.8,
    'C':2.5,
    'D':-3.5,
    'E':-3.5,
    'F':2.8,
    'G':-0.4,
    'H':-3.2,
    'I':4.5,
    'K':-3.9,
    'L':3.8,
    'M':1.9,
    'N':-3.5,
    'P':-1.6,
    'Q':-3.5,
    'R':-4.5,
    'S':-0.8,
    'T':-0.7,
    'V':4.2,
    'W':-0.9,
    'X':None,
    'Y':-1.3,
    '-':None,
}

def calculate(seq:"The amino acid sequence."):
    """Calculate the GRAVY score."""
    answers = [_values[k] for k in seq]
    answers = [v for v in answers if v is not None]
    if len(answers):
        return sum(answers) / len(answers)
    else:
        return float('nan')

def main(args=None):
    ans = _wp.easymode.simple_run(
        args=args,
        program_object=calculate,
        prog="gravy",
        endgame='return',
    )
    print(format(ans, ".5f"))
    
if __name__ == '__main__':
    main() 
