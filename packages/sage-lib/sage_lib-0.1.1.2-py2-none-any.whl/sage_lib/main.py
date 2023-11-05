import argparse, os
from sage_lib import DFTPartition  # Make sure to import relevant classes

def generate_xyz_from_outcar(path, verbose=False):
    absolute_path = os.path.abspath(path)  # Convert the path to an absolute path
    DP = DFTPartition(absolute_path)
    DP.readVASPFolder(v=verbose)
    DP.export_configXYZ()
    
def generate_vacancy(path, verbose=False):
    absolute_path = os.path.abspath(path)  # Convert the path to an absolute path
    DP = DFTPartition(absolute_path)
    DP.readVASPFolder(v=verbose)
    DP.generateDFTVariants('Vacancy', [1])
    DP.exportVaspPartition()

def main():
    parser = argparse.ArgumentParser(description='Tool for theoretical calculations in quantum mechanics and molecular dynamics.')
    subparsers = parser.add_subparsers(dest='command', help='Available sub-commands')

    # Sub-command to generate vacancy directory
    parser_vacancy = subparsers.add_parser('vacancy', help='Generate vacancy.')
    parser_vacancy.add_argument('--path', type=str, required=True, help='Path to the VASP files directory')   
    parser_vacancy.add_argument('--verbose', action='store_true', help='Display additional information')
    
    # Sub-command to generate XYZ file from an OUTCAR directory
    parser_xyz = subparsers.add_parser('xyz', help='Generate an XYZ file from an OUTCAR directory.')
    parser_xyz.add_argument('--path', type=str, required=True, help='Path to the OUTCAR directory')
    parser_xyz.add_argument('--verbose', action='store_true', help='Display additional information')
    parser_xyz.add_argument('--subfolders', action='store_true', help='Read all subfolders')


    args = parser.parse_args()

    if args.command == 'xyz':
        generate_xyz_from_outcar(args.path, verbose=args.verbose)

    if args.command == 'vacancy':
        generate_vacancy(args.path, verbose=args.verbose)

if __name__ == '__main__':
    main()