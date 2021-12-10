from typing import Callable, Any, Sequence
from Utils import *


def ddmin(test: Callable, inp: Sequence, *test_args: Any) -> Sequence:
    """
    Reduce the input inp, using the outcome of test(fun, inp).
    worst time: O(n^2)
    """

    assert test(inp, *test_args) != PASS

    n = 2  # Initial granularity
    while len(inp) >= 2:
        start = 0
        subset_length = len(inp) // n
        some_complement_is_failing = False

        while start < len(inp):
            complement = (inp[:start] + inp[start + subset_length:])

            if test(complement, *test_args) == FAIL:
                inp = complement  # update inp to exclude subset
                n = max(n - 1, 2)
                some_complement_is_failing = True
                break

            start += subset_length

        if not some_complement_is_failing:
            if n == len(inp):
                break
            n = min(n * 2, len(inp))

    return inp


def main():
    # result = ddmin(property_check, failing_input, compile_program, error)
    result = ddmin(property_check, failing_input, error)
    print('Final Reduced Output -->', result)



if __name__ == '__main__':
    main()
