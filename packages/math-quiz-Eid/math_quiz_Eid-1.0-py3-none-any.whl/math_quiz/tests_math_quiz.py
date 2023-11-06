import unittest
from math_quiz import generate_random_int, choose_random_op, operator


class TestMathGame(unittest.TestCase):

    def test_generate_random_int(self):
        # Test if random numbers generated are within the specified range
        min_val = 1
        max_val = 10
        for _ in range(1000):  # Test a large number of random values
            rand_num = generate_random_int(min_val, max_val)
            self.assertTrue(min_val <= rand_num <= max_val)

    def choose_random_op(self):
        # Test if random operators generated are within the specified range
        operators = ['+', '-', '*']
        for _ in range(1000):
            rand_op = choose_random_op()
            self.assertTrue(rand_op in operators)
        

    def test_function_C(self):
            test_cases = [
                (5, 2, '+', '5 + 2', 7),
                (8, 3, '-', '8 - 3', 5),
                (4, 6, '*', '4 * 6', 24),
            ]

            for x in test_cases:
                # TODO
                # Unpack the test case tuple into variables
                # Call the function operator(num1, num2, operator) and compare
                problem, answer = operator(x[0], x[1], x[2])
                # the result with the expected result for each test case
                self.assertEqual(x[3], problem)
                self.assertEqual(x[4], answer)

if __name__ == "__main__":
    unittest.main()
