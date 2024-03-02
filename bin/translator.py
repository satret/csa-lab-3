import argparse
from json import dumps
import io

from machine.translator import parse_code


def main(input_file: io.TextIOWrapper, output_file: io.TextIOWrapper):
    code_text = input_file.readlines()
    parsed_data, parsed_code = parse_code(code_text)
    output_file.write(dumps({
        'data': parsed_data,
        'code': parsed_code
    }, indent=4))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog='asm translator')
    parser.add_argument('input_file', type=argparse.FileType('r'), help='.asm file')
    parser.add_argument('output_file', type=argparse.FileType('w'), help='.out file')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(args.input_file, args.output_file)
