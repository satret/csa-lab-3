import pytest

from machine.isa import OperandType
from machine.translator import parse_data_block, parse_text_block, RealInstruction, RealOperand, parse_code


@pytest.mark.parametrize("data_block, expected_data_mem, expected_data_mem_map", [
    ("var: word 99", [99], {'var': 0}),
    ("a: word 1\nb: word 3", [1, 3], {'a': 0, 'b': 1}),
    ("str: db \"abc\"", [97, 98, 99], {'str': 0}),
])
def test_parse_data_block(data_block, expected_data_mem, expected_data_mem_map):
    data_memory, data_memory_map = parse_data_block(data_block)
    assert data_memory == expected_data_mem
    assert data_memory_map == expected_data_mem_map


@pytest.mark.parametrize("text_block, expected_text_mem, expected_text_mem_map", [
    ("ld val", [RealInstruction('ld', RealOperand(OperandType.LABEL_TO_REPLACE, 'val'))], {}),
    ("jmp .exit", [RealInstruction('jmp', RealOperand(OperandType.LABEL_TO_REPLACE, '.exit'))], {}),
    ("ld #4", [RealInstruction('ld', RealOperand(OperandType.CONSTANT, 4))], {}),
    ("start:\nadd #4\nend:\nhlt", [RealInstruction('add', RealOperand(OperandType.CONSTANT, 4)),
                                   RealInstruction('hlt', None)], {'start': 0, 'end': 1}),
])
def test_parse_test_block(text_block, expected_text_mem, expected_text_mem_map):
    data_memory, data_memory_map = parse_text_block(text_block)
    assert data_memory == expected_text_mem
    assert data_memory_map == expected_text_mem_map


@pytest.mark.parametrize("code, expected_data, expected_code", [
    (
            """
    section .data
        a: word 44
        b: word 555
        val: word 777
    section .text
            ld val
            add #-1
        start:
            st val
        jmp start
    """,
            [44, 555, 777],
            [RealInstruction('ld', RealOperand(OperandType.DIRECT_ADDRESS, 2)),
             RealInstruction('add', RealOperand(OperandType.CONSTANT, -1)),
             RealInstruction('st', RealOperand(OperandType.CONSTANT, 2)),
             RealInstruction('jmp', RealOperand(OperandType.CONSTANT, 2)),
             ],
    ),
])
def test_parse_all(code, expected_data, expected_code):
    parsed_data, parsed_code = parse_code(code.split('\n'))
    assert parsed_data == expected_data
    assert parsed_code == expected_code
