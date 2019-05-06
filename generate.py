"""
Input file generator for HackerRank for Work
programming problems

author: Pawel Kacprzak (pkacprzak)

Allows to either generate a single test file that is written to stdout
or a full test suite that is written to given output directory.
"""

import sys
import os
import string

from random import seed
from random import randint as rand
from random import choice
from random import sample
from random import shuffle
from random import random
from random import uniform
from random import gauss

import math
import networkx as nx

NUM_MAX_TESTS = 15

class TestSuite(object):
    """
    Collection of test files. A single test is an tuple of values.
    Example format count be a tuple (price, cost) where price is a list
    and cost is integer.
    """

    def __init__(self):
        self.tests = []

    def add(self, test):
        """
        Adds a single test to the suite
        :param test: test to be added
        """
        if len(self.tests) == NUM_MAX_TESTS:
            raise ValueError("Max number of test files is %d" % NUM_MAX_TESTS)
        self.tests.append(test)

    def __len__(self):
        return len(self.tests)

    def __getitem__(self, key):
        return self.tests[key]

class TestWriter(object):
    """
    Reponsible for writing tests from TestSuite to given output
    """

    def __init__(self, test_suite, test_serializer):
        """
        :param test_suite: TestSuite instance
        :param test_serializer: function that takes a test from TestSuite
        and returns this test serialized as string
        """
        self.test_suite = test_suite

    def write_single(self, test_id, output_file):
        """
        :param test_id: id of the test to write
        :param output_file: output file pointer, can be stdout as well
        """
        assert 0 <= test_id < len(self.test_suite)
        output_file.write(test_serializer(*self.test_suite[test_id]))

# Complete this function
def test_serializer(arr):
    """
    Takes unpacked tuple corresponding to a single test
    and returns a string encoding of the test.
    The output of this function should match the expected
    input of the HRW stub reading the input file
    """
    n = len(arr)
    out = "%d\n" % n
    for e in arr:
        out += "%d\n" % e
    return out

# Settings
VAL_RANGE = 1, 10**9
SMALL_N = 10
LARGE_N = 10**5

# Helper functions
def get_unique_random_values(n):
    values = set([VAL_RANGE[0], VAL_RANGE[1]])
    while len(values) < n:
        values.add(rand(*VAL_RANGE))
    assert len(values) == n
    return list(values)

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--test_id", type=int, choices=range(NUM_MAX_TESTS))
    group.add_argument("--output_dir")

    args = parser.parse_args()
    assert args.test_id is not None or args.output_dir is not None

    # initialization
    seed(42)
    test_suite = TestSuite()

    # generating samples
    samples = (
        [3, 1, 2],
        [5, 2, 3, 16, 1, 4],
        [5, 4, 3, 2, 1],
    )
    for arr in samples:
        test_suite.add((arr,))

    # generating non-samples

    # n, reps
    test_params = [
        (SMALL_N, 3),
        (LARGE_N, 7),
    ]
    for n, reps in test_params:
        for _ in xrange(reps):
            arr = get_unique_random_values(n)
            test = (arr,)
            test_suite.add(test)

    writer = TestWriter(test_suite, test_serializer)
    if args.output_dir is not None:
        for file_id in range(len(test_suite)):
            output_path = os.path.join(args.output_dir, "input%03d.txt" % file_id)
            with open(output_path, 'w') as fp:
                writer.write_single(file_id, fp)
    else:
        writer.write_single(args.test_id, sys.stdout)
