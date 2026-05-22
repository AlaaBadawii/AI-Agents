
def factorial(n: int) -> int:
    """
    Calculate the factorial of a non‑negative integer.

    The factorial of n (denoted n!) is the product of all positive integers
    less than or equal to n. By convention, 0! = 1.

    Parameters
    ----------
    n : int
        A non‑negative integer whose factorial is to be computed.

    Returns
    -------
    int
        The factorial of n. For large n the result may be a very large integer;
        Python’s built‑in arbitrary precision integers are used.

    Raises
    ------
    ValueError
        If n is negative, since factorial is defined only for n >= 0.

    Examples
    --------
    >>> factorial(0)
    1
    >>> factorial(1)
    1
    >>> factorial(5)
    120
    >>> factorial(10)
    3628800

    Edge Cases
    ----------
    - Input 0: Returns 1 (by definition).
    - Input 1: Returns 1 (product of integers 1).
    - Negative input: Raises ValueError.
    - Very large n (e.g., n=1000): The function still works because Python
      integers can handle arbitrarily large values, but the result may be
      extremely large and memory‑intensive.

    Note
    ----
    This implementation uses an iterative loop to avoid recursion depth
    limitations. For extremely large n, consider using math.factorial(),
    which is implemented in C and is faster.
    """
    if n < 0:
        raise ValueError("Factorial is defined for non-negative integers only.")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


import unittest

# Assume the factorial function is defined as in the previous answer.
# For completeness, we include it here (but usually it would be imported).
def factorial(n: int) -> int:
    """Calculate the factorial of a non‑negative integer."""
    if n < 0:
        raise ValueError("Factorial is defined for non-negative integers only.")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


class TestFactorial(unittest.TestCase):
    """Unit tests for the factorial function."""

    # Basic functionality
    def test_zero(self):
        """0! should equal 1."""
        self.assertEqual(factorial(0), 1)

    def test_one(self):
        """1! should equal 1."""
        self.assertEqual(factorial(1), 1)

    def test_small_positive(self):
        """Factorial of small positive integers."""
        self.assertEqual(factorial(2), 2)
        self.assertEqual(factorial(3), 6)
        self.assertEqual(factorial(4), 24)
        self.assertEqual(factorial(5), 120)

    def test_medium_positive(self):
        """Factorial of numbers like 10."""
        self.assertEqual(factorial(10), 3628800)

    def test_large_positive(self):
        """Factorial of a larger number (result type check)."""
        result = factorial(20)
        self.assertEqual(result, 2432902008176640000)
        self.assertIsInstance(result, int)  # ensure arbitrary precision

    # Edge cases
    def test_very_large(self):
        """Factorial of 100 to ensure no overflow and result is integer."""
        result = factorial(100)
        # Known value: 100! = 93326215443944152681699238856266700490715968264381621468592963895217599993229915608941463976156518286253697920827223758251185210916864000000000000000000000000
        expected = 93326215443944152681699238856266700490715968264381621468592963895217599993229915608941463976156518286253697920827223758251185210916864000000000000000000000000
        self.assertEqual(result, expected)
        self.assertIsInstance(result, int)

    # Error cases
    def test_negative_input(self):
        """Negative input must raise ValueError."""
        with self.assertRaises(ValueError):
            factorial(-1)
        with self.assertRaises(ValueError):
            factorial(-100)

    def test_negative_zero(self):
        """Negative zero is still zero? In Python, -0 is zero, but not negative."""
        # -0 is treated as 0, so should return 1 (no error)
        self.assertEqual(factorial(-0), 1)

    # Various input scenarios (non‑integer types)
    def test_float_input_raises_type_error(self):
        """Passing a float (e.g., 5.0) should raise a TypeError because range expects int."""
        with self.assertRaises(TypeError):
            factorial(5.0)

    def test_string_input_raises_type_error(self):
        """Passing a string should raise a TypeError."""
        with self.assertRaises(TypeError):
            factorial("5")

    def test_boolean_input(self):
        """Booleans: True is 1, False is 0 -> valid integers."""
        self.assertEqual(factorial(True), 1)
        self.assertEqual(factorial(False), 1)

    # Additional edge: large negative
    def test_large_negative(self):
        """Very large negative integer also raises ValueError."""
        with self.assertRaises(ValueError):
            factorial(-1000)

    # Verify result type for larger numbers
    def test_result_is_int(self):
        """Factorial of any non‑negative integer returns an int."""
        for n in [0, 1, 5, 10, 50]:
            self.assertIsInstance(factorial(n), int)


if __name__ == '__main__':
    unittest.main()