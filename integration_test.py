import yaml
from pathlib import Path
from machine.simulation import simulation
from machine.translator import parse_code

def read_asm_file(filename):
    with open(filename, 'r') as file:
        return file.readlines()

def read_golden_file(filename):
    with open(filename, 'r') as file:
        return yaml.safe_load(file)

def assemble_and_run(asm_file):
    # Считываем исходный ассемблерный код
    asm_code = read_asm_file(asm_file)

    # Транслируем ассемблерный код в машинный код
    data_memory, instructions = parse_code(asm_code)

    # Запускаем симуляцию. Предполагаем, что ввод для машины пустой и размер памяти - 256
    # Вы можете изменить эти значения в зависимости от ваших нужд
    output = simulation({'data': data_memory, 'code': instructions}, input_tokens=[], data_memory_size=256, simulation_limit=1000)

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
