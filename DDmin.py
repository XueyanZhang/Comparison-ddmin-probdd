from typing import Callable, Any, Sequence
from Utils import *
import time

Query = 0


def ddmin(test: Callable, inp: Sequence, *test_args: Any) -> Sequence:
    """
    Reduce the input inp, using the outcome of test(fun, inp).
    worst time: O(n^2)
    """

    assert test(inp, *test_args) != PASS
    cache = dict()
    global Query

    n = 2  # Initial granularity
    while len(inp) >= 2:
        start = 0
        subset_length = len(inp) // n
        some_complement_is_failing = False

        while start < len(inp):
            complement = (inp[:start] + inp[start + subset_length:])

            if str(complement) in cache:
                outcome = cache[str(complement)]
            else:
                outcome = test(complement, *test_args)
                cache[str(complement)] = outcome
            Query += 1
            if outcome == FAIL:
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
    c = time.time()
    # result = ddmin(property_check, failing_input, compile_program, error)
    # result = ddmin(property_check, failing_input, error)
    result = ddmin(property_check, failing_input, bench, bash_check)
    print('time:\n',time.time() - c)
    print('input size:\n', len(failing_input))
    print('output size\n', len(result))
    print('querry:\n',Query)
    print('Final Reduced Output -->\n', result)



if __name__ == '__main__':
    main()
