import pytest
import yaml
import os
import subprocess

# Assuming there's a function to execute your .asm files and return their output.
# You'll need to implement this based on how your assembly files should be executed.
def assemble_and_run(asm_file):
    # Placeholder: replace with actual execution logic
    # e.g., subprocess.run(["your_assembler", asm_file], capture_output=True)
    return output

@pytest.mark.parametrize("test_case", ["cat", "hello", "prob2"])
def test_assembly_examples(test_case):
    asm_file = f"examples/{test_case}.asm"
    expected_output_file = f"goldens/{test_case}.yml"

    # Run the .asm file to get its output
    output = assemble_and_run(asm_file)

    # Load the expected output from the .yml file
    with open(expected_output_file) as f:
        expected_output = yaml.safe_load(f)

    # Compare the actual output against the expected output
    assert output == expected_output, f"Output for {test_case} did not match expected output."
