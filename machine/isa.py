from dataclasses import dataclass
from enum import Enum
from typing import Optional


class OperandType(str, Enum):
    DIRECT_ADDRESS = 'direct_address'  # прямая адресация
    INDIRECT_ADDRESS = 'indirect_address'  # косвенная адресация
    CONSTANT = 'constant'

    LABEL_TO_REPLACE = 'label_to_replace'


@dataclass
class Operand:
    type: OperandType
    value: int


class Opcode(str, Enum):
    IN = 'in'
    OUT = 'out'
    HLT = 'hlt'

    ST = 'st'
    LD = 'ld'
    ADD = 'add'
    DIV = 'div'
    MOD = 'mod'

    CMP = 'cmp'
    JMP = 'jmp'
    JE = 'je'


@dataclass
class Instruction:
    name: Opcode
    operands_count: int
    is_data_operand: Optional[bool]


INSTRUCTIONS = {
    'in': Instruction(Opcode.IN, 0, None),
    'out': Instruction(Opcode.OUT, 0, None),
    'hlt': Instruction(Opcode.HLT, 0, None),

    'st': Instruction(Opcode.ST, 1, True),
    'ld': Instruction(Opcode.LD, 1, True),
    'add': Instruction(Opcode.ADD, 1, True),
    'div': Instruction(Opcode.DIV, 1, True),
    'mod': Instruction(Opcode.MOD, 1, True),

    'cmp': Instruction(Opcode.CMP, 1, True),

    'jmp': Instruction(Opcode.JMP, 1, False),
    'je': Instruction(Opcode.JE, 1, False),
}
