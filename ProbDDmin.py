from typing import Callable, Any, Sequence
import collections
from copy import deepcopy
from Utils import *


class ProbDD(object):
    def __init__(self, test, split=None, cache=None, id_prefix=()):
        self._test = test
        self._id_prefix = id_prefix
        self.p = collections.OrderedDict()
        self.initialP = 0.5
        self.threshold = 0.8
        self.min = []

    def __call__(self, inp: Sequence, *test_args: Any):
        for c in inp:
            self.p[c] = self.initialP
        self.min = inp
        while not self._test_done():
            deleteconfig = self.sample()  # select a subsequence to delete
            subsequence = [c for c in self.min if c not in set(deleteconfig)]  # actual subsequence to test
            outcome = self._test_config(subsequence, *test_args)

            # print('deleteconfig = ',deleteconfig)
            # print('subsequence = ',subsequence)
            # print(self.p.values())

            if outcome == FAIL:  # subsequence triggers the Fail bug
                for key in deleteconfig:
                    self.p[key] = 0
                self.min = subsequence  # new min program found
            else:
                increase_ratio = self.computeRatio(deleteconfig, self.p)
                for key in deleteconfig:
                    if self.p[key] != 0 and self.p[key] != 1:
                        self.p[key] = self.p[key] * increase_ratio
                if len(deleteconfig) == 1:
                    # print(str(deleteconfig[0]) + " must preserve\n")
                    self.p[deleteconfig[0]] = 1

        return self.min

    def computeRatio(self, deleteconfig, p):
        """
        Product_j [(1 - p_j) ^ (1 - x_j)] in paper.
        (1 - x_j) is a selector to only include (x_j == 0).
        Elements in the compliment/subsequence (x_j == 1) are excluded.
        """
        product = 1
        for x in deleteconfig:
            if 0 < p[x] < 1:
                product *= (1 - p[x])
        return 1 / (1 - product)

    def sample(self):
        keys_sorted = sorted(self.p, key=self.p.get)
        keys_sorted = [c for c in keys_sorted if 0 < self.p[c] < 1]

        previous_gain = 0
        compliment = []
        for i, key in enumerate(keys_sorted):
            expected_gain = 1
            for j in range(i + 1):
                expected_gain *= (1 - self.p[keys_sorted[j]])
            expected_gain *= (i + 1)
            # print("key=",key,"\tprob = ", self.p[key], "\tgain = ", expected_gain, "\tlast = ", previous_gain)
            if expected_gain < previous_gain:
                break
            previous_gain = expected_gain
            compliment.append(key)

        return compliment

    def _test_done(self):
        tmp = list(set(self.p.values()))
        alldecided = (tmp == [0, 1] or tmp == [0] or tmp == [1])
        if alldecided:
            print("Iteration needs to stop :: because all elements are decided.")
            return True
        for key in self.p.keys():
            if min(self.p[key], 1) < self.threshold:
                return False
        print("Iteration needs to stop :: because of convergence.")
        return True

    def _test_config(self, config, *test_args: Any):
        # config_id = self._id_prefix + config_id
        # input_string = ''.join(config)
        return self._test(config, *test_args)


def main():
    probdd = ProbDD(property_check)
    # result = probdd(failing_input, compile_program)
    result = probdd(failing_input, error)
    print('Final Reduced Output -->', result)
    print(len(result))


if __name__ == '__main__':
    main()
