import pytest
import yaml
import os
import subprocess

def run_assembly_program(asm_code, stdin=""):
    # Функция для компиляции и запуска ассемблерной программы.
    # Это место для вашего кода запуска компилятора и выполнения программы.
    # Возвращаемые значения должны быть адаптированы под вашу логику.
    pass

def load_golden_data(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

@pytest.mark.parametrize("filename", ["cat.yml", "hello.yml", "prob2.yml"])
def test_golden(filename, caplog):
    golden_path = os.path.join("goldens", filename)
    golden_data = load_golden_data(golden_path)[0]

    asm_files = {
        "cat.yml": "cat.asm",
        "hello.yml": "hello.asm",
        "prob2.yml": "prob2.asm",
    }

    asm_code_path = asm_files[filename]
    with open(asm_code_path, 'r', encoding='utf-8') as file:
        asm_code = file.read()

    if filename == "cat.yml":
        mocked_output, mocked_log = run_assembly_program(asm_code, golden_data["in_stdin"])
    else:
        mocked_output, mocked_log = run_assembly_program(asm_code)

    assert mocked_output == golden_data["out_stdout"]
    assert mocked_log == golden_data["out_log"]
