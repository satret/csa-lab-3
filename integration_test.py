import pytest
import yaml
from simulation import simulation
from translator import parse_code

# Функция для сборки и запуска ассемблерной программы
def assemble_and_run(asm_file_path):
    with open(asm_file_path, 'r') as file:
        asm_code = file.read()
    data_memory, instructions = parse_code(asm_code)
    # Предполагаем, что нет входных данных для программы, и ограничение на количество инструкций достаточно велико
    output = simulation({'data': data_memory, 'code': instructions}, [], 256, 10000)
    return output

@pytest.mark.parametrize("test_case", ["cat", "hello", "prob2"])
def test_assembly_examples(test_case):
    asm_file = f"examples/{test_case}.asm"
    expected_output_file = f"goldens/{test_case}.yml"

    # Запустить .asm файл и получить его вывод
    output = assemble_and_run(asm_file)

    # Загрузить ожидаемый вывод из .yml файла
    with open(expected_output_file) as f:
        expected_output = yaml.safe_load(f)

    # Сравнить фактический вывод с ожидаемым
    assert output == expected_output, f"Вывод для {test_case} не соответствует ожидаемому."
