import unittest

def sum_two_numbers(a: int | float, b: int | float) -> int | float:
    """
    Return the sum of two numbers.

    This function takes two numeric arguments and returns their sum.
    It supports integers, floating-point numbers, and combinations thereof.

    Parameters
    ----------
    a : int or float
        The first number to be added.
    b : int or float
        The second number to be added.

    Returns
    -------
    int or float
        The sum of `a` and `b`. Returns an int if both arguments are ints,
        otherwise returns a float.

    Examples
    --------
    >>> sum_two_numbers(3, 5)
    8
    >>> sum_two_numbers(2.5, 4.3)
    6.8
    >>> sum_two_numbers(-7, 2)
    -5
    >>> sum_two_numbers(1e10, 2e10)
    30000000000.0

    Edge Cases
    ----------
    - Negative numbers are handled correctly.
    - Large numbers are supported (subject to Python's numeric limits).
    - If either argument is a float, the result is a float.
    - Passing non-numeric types (e.g., strings, lists) raises TypeError.

    Raises
    ------
    TypeError
        If either `a` or `b` is not an int or float.
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both arguments must be int or float")
    return a + b


class TestSumTwoNumbers(unittest.TestCase):
    """Unit tests for the sum_two_numbers function."""

    # Basic functionality
    def test_positive_ints(self):
        self.assertEqual(sum_two_numbers(3, 5), 8)

    def test_positive_floats(self):
        self.assertAlmostEqual(sum_two_numbers(2.5, 4.3), 6.8)

    def test_mixed_int_float(self):
        self.assertAlmostEqual(sum_two_numbers(3, 2.5), 5.5)

    # Negative numbers
    def test_negative_ints(self):
        self.assertEqual(sum_two_numbers(-7, 2), -5)

    def test_two_negative_ints(self):
        self.assertEqual(sum_two_numbers(-4, -6), -10)

    def test_negative_float(self):
        self.assertAlmostEqual(sum_two_numbers(-1.5, 0.5), -1.0)

    # Zero
    def test_zero_and_positive(self):
        self.assertEqual(sum_two_numbers(0, 10), 10)

    def test_zero_and_negative(self):
        self.assertEqual(sum_two_numbers(0, -3), -3)

    def test_both_zero(self):
        self.assertEqual(sum_two_numbers(0, 0), 0)

    # Large numbers
    def test_large_ints(self):
        self.assertEqual(sum_two_numbers(1_000_000_000, 2_000_000_000), 3_000_000_000)

    def test_large_floats(self):
        self.assertAlmostEqual(sum_two_numbers(1e10, 2e10), 3e10)

    # Return type
    def test_return_type_int(self):
        result = sum_two_numbers(1, 2)
        self.assertIsInstance(result, int)

    def test_return_type_float(self):
        result = sum_two_numbers(1.0, 2)
        self.assertIsInstance(result, float)

    # Error handling - invalid types
    def test_string_first_arg(self):
        with self.assertRaises(TypeError):
            sum_two_numbers("hello", 5)

    def test_string_second_arg(self):
        with self.assertRaises(TypeError):
            sum_two_numbers(5, "world")

    def test_list_arg(self):
        with self.assertRaises(TypeError):
            sum_two_numbers([1, 2], 3)

    def test_none_arg(self):
        with self.assertRaises(TypeError):
            sum_two_numbers(None, 5)

    def test_both_invalid(self):
        with self.assertRaises(TypeError):
            sum_two_numbers("a", "b")

    # Boolean inputs (bool is subclass of int)
    def test_boolean_true(self):
        self.assertEqual(sum_two_numbers(True, 2), 3)

    def test_boolean_false(self):
        self.assertEqual(sum_two_numbers(False, 5), 5)

    def test_both_booleans(self):
        self.assertEqual(sum_two_numbers(True, False), 1)


if __name__ == "__main__":
    unittest.main()