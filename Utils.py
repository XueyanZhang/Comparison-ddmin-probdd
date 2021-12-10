from typing import Callable, Any, Sequence, List
import tempfile
import os
import subprocess
import shutil


PASS = 'PASS'
FAIL = 'FAIL'
UNRESOLVED = 'UNRESOLVED'


### ----------------- SAMPLE string input
def generic_test(inp: Sequence, fun: Callable, expected_exc=None) -> str:
    result = None
    detail = ""
    try:
        result = fun(inp)
        outcome = PASS
    except Exception as exc:
        detail = f" ({type(exc).__name__}: {str(exc)})"
        if expected_exc is None:
            outcome = FAIL
        elif type(exc) == type(expected_exc) and str(exc) == str(expected_exc):
            outcome = FAIL
        else:
            outcome = UNRESOLVED

    print(f"{fun.__name__}({repr(inp)}):\t{outcome}\t{detail}")
    return outcome


def mystery(inp: str) -> None:
    x = inp.find(chr(0o17 + 0o31))
    y = inp.find(chr(0o27 + 0o22))
    if 0 <= x < y and y >= 0:
        raise ValueError("Invalid input")
    else:
        pass


### SAMPLE
# sample_input = 'V"/+!aF-(V4EOz*+s/Q,7)2@0_'
# sample_input2 = '(V)2w'
#
# failing_input = sample_input
# property_check = generic_test
# compile_program = mystery
# error = ValueError('Invalid input')


### ----------------- TOY python input
def read2list(filename: str) -> List[str]:
    with open(filename, 'r') as f:
        lines = f.readlines()
    return lines


def test_py_program(sequence: List[str], expected_exc=None) -> str:
    fd, path = tempfile.mkstemp(suffix='.py')
    with open(path, 'w') as f:
        f.writelines(sequence)
    os.close(fd)

    try:
        subprocess.check_output(['python3', path],stderr=subprocess.STDOUT)
        outcome = PASS
    except subprocess.CalledProcessError as exc:
        if expected_exc in exc.output:
            outcome = FAIL
        else:
            outcome = UNRESOLVED

    print(f"Test({list(sequence)}):\t{outcome}")
    return outcome


### TOY
# toy_input1 = read2list('Toy1.py')
# test_py_program(toy_input1, b'TypeError: can only concatenate str (not "int") to str')
#
# failing_input = toy_input1
# property_check = test_py_program
# error = b'TypeError: can only concatenate str (not "int") to str'




### ----------------- BENCHMARK
def read_token(filename: str) -> List[str]:
    with open(filename, 'r') as f:
        tokens = f.read().split(' ')
    return tokens

def test_token_program(sequence: List[str], bench: str, bash_check: str) -> str:
    with tempfile.TemporaryDirectory() as td:
        shutil.copyfile(bash_check, f"{td}/r.sh")
        filepath = td+"/"+bench
        with open(filepath, 'w') as f:
            f.write(' '.join(sequence))

        os.chdir(td)
        try:
            proc = subprocess.run(['bash', f"{td}/r.sh"],stderr=subprocess.STDOUT)
            if proc.returncode == 0:
                outcome = FAIL
            else:
                outcome = PASS
        except Exception as e:
            outcome = UNRESOLVED

    print(f"Test({list(sequence)}):\t{outcome}")
    return outcome

def test_program(sequence: List[str], bench: str, bash_check: str) -> str:
    with tempfile.TemporaryDirectory() as td:
        shutil.copyfile(bash_check, f"{td}/r.sh")
        filepath = td+"/"+bench
        with open(filepath, 'w') as f:
            f.writelines(sequence)

        os.chdir(td)
        try:
            proc = subprocess.run(['bash', f"{td}/r.sh"],stderr=subprocess.STDOUT)
            if proc.returncode == 0:
                outcome = FAIL
            else:
                outcome = PASS
        except Exception as e:
            outcome = UNRESOLVED

    print(f"Test({list(sequence)}):\t{outcome}")
    return outcome

bench = 't.cpp'
# input = read2list(f'benchmark_toys/cpp_print/{bench}')
input = read_token(f'benchmark_toys/cpp_print/{bench}')
print(input)

failing_input = input
# property_check = test_program
property_check = test_token_program
bash_check = '/Users/x2336zha/Documents/DD_vs_ProbDD/benchmark_toys/cpp_print/r.sh'