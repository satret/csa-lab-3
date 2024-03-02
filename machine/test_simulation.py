import pytest

from machine.isa import Opcode, OperandType
from machine.simulation import DataPath, ControlUnit
from machine.translator import RealInstruction, RealOperand


def simulate_until_finish(data, code, memsize, inp):
    dp = DataPath(memsize, data, inp)
    cu = ControlUnit(code, dp)

    try:
        while True:
            cu.decode_and_execute_instr()
    except StopIteration:
        return cu


@pytest.mark.parametrize("data, code, expected_acc", [
    (
            [6, 5],
            [
                RealInstruction(Opcode.LD, RealOperand(OperandType.CONSTANT, 3)),
                RealInstruction(Opcode.ADD, RealOperand(OperandType.CONSTANT, 5)),
                RealInstruction(Opcode.HLT, None)
            ],
            8,
    ),
    (
            [999, 777, 4, 888, 222],
            [
                RealInstruction(Opcode.LD, RealOperand(OperandType.DIRECT_ADDRESS, 4)),
                RealInstruction(Opcode.HLT, None)
            ],
            222,
    ),
    (
            [999, 777, 4, 888, 333],
            [
                RealInstruction(Opcode.LD, RealOperand(OperandType.INDIRECT_ADDRESS, 2)),
                RealInstruction(Opcode.HLT, None)
            ],
            333,
    ),
])
def test_addr(data, code, expected_acc):
    cu = simulate_until_finish(data, code, 10, [])
    assert cu.data_path.acc == expected_acc


@pytest.mark.parametrize("data, code, expected_acc", [
    (
            [],
            [
                RealInstruction(Opcode.JMP, RealOperand(OperandType.CONSTANT, 2)),
                RealInstruction(Opcode.JMP, RealOperand(OperandType.CONSTANT, 999)),
                RealInstruction(Opcode.ADD, RealOperand(OperandType.CONSTANT, 5)),
                RealInstruction(Opcode.HLT, None)
            ],
            5,
    ),
    (
            [],
            [
                RealInstruction(Opcode.LD, RealOperand(OperandType.CONSTANT, 2)),
                RealInstruction(Opcode.CMP, RealOperand(OperandType.CONSTANT, 2)),
                RealInstruction(Opcode.JE, RealOperand(OperandType.CONSTANT, 3)),
                RealInstruction(Opcode.HLT, None)
            ],
            2,
    ),
])
def test_jmp(data, code, expected_acc):
    cu = simulate_until_finish(data, code, 10, [])
    assert cu.data_path.acc == expected_acc
