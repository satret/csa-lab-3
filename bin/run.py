import argparse
import io
import json

from machine.simulation import simulation


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog='asm translator')
    parser.add_argument('binary_file', type=argparse.FileType('r'), help='.out file')
    parser.add_argument('input_file', type=argparse.FileType('r'), help='.txt file')
    return parser.parse_args()


def main(binary_file: io.TextIOWrapper, input_file: io.TextIOWrapper):
    print('machine started')
    program = json.loads(binary_file.read())
    print(program)
    inp = list(input_file.read())
    print(simulation(program, inp, 32, 1e4))


if __name__ == '__main__':
    args = parse_args()
    main(args.binary_file, args.input_file)
