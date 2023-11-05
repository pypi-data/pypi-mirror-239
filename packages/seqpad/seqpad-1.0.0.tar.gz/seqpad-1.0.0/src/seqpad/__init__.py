import wonderparse as _wp


def seqpad(seq:"nucleotide sequence"):
    while len(seq) % 3 != 0:
        seq += 'N'
    return seq

def main(args=None):
    _wp.easymode.simple_run(
        args=args,
        program_object=seqpad,
        prog='seqpad',
    )
    
if __name__ == '__main__':
    main() 
