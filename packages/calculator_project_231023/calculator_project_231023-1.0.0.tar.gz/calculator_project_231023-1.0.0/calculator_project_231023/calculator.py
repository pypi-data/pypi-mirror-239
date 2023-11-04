import sys
from decimal import Decimal, getcontext, InvalidOperation

PRECISION = 10
MATH_OPERATIONS = ['+', '-', '*', '/', '**']
ACTIONS = ['c', 'r', 'q']
MAX_ATTEMPTS = 3


class Calculator:
    """
    Performs the inbuilt Python math operations of addition (+), subtraction (-),
    multiplication (*), and division (/). It can also take (n) root of a number
    by using Python inbuilt exponentiation operation (**). The calculator stores one most recent
    operation result and appies additional operations to that result until explicitly instructed to
    clear the result. All the operations are carried out in the Decimal format for more precision.

    Attributes:
        result: Holds the most recent operation result.

    Methods:
        clear_result(): Resets the calculator result to 0.
        add(addend: Decimal): Adds the given addend to the current result.
        subtract(subtrahend: Decimal): Subtracts the given subtrahend from the current result.
        multiply(multiplier: Decimal): Multiplies the current result by the given multiplier.
        divide(divisor: Decimal): Divides the current result by the given divisor.
        root(degree: Decimal): Calculates the root of the current result with the given degree by
        using the ** exponent operation.
    """

    def __init__(self) -> None:
        """
        Initializes the class with 0 for a result.
        """
        self.result = Decimal(0)

    def clear_result(self) -> None:
        """
        Resets the calculator result to 0.
        """
        self.result = Decimal(0)
        print("Calculator reset to 0\n")
        return

    def add(self, addend: Decimal) -> None:
        """
        Adds the given addend to the current result.

        Args:
            addend: The value to be added to the current result.
        """
        self.result += Decimal(addend)
        return

    def subtract(self, subtrahend: Decimal) -> None:
        """
        Subtracts the given subtrahend from the current result.

        Args:
            subtrahend: The value to be subtracted from the current result.
        """
        self.result -= Decimal(subtrahend)
        return

    def multiply(self, multiplier: Decimal) -> None:
        """
        Multiplies the current result by the given multiplier.

        Args:
            multiplier: The value by which the current result is multiplied.
        """
        self.result *= Decimal(multiplier)
        self.result = self.result.normalize()
        return

    def divide(self, divisor: Decimal) -> None:
        """
        Divides the current result by the given divisor.

        Args:
            divisor: The value by which the current result is divided.
        """
        self.result /= Decimal(divisor)
        return

    def root(self, degree: Decimal) -> None:
        """
        Calculates the root of the current result with the given degree by using the **
        exponent operation. For example 3rd degree root user input is provided as 3, but
        would be carried out as **(1/3).

        Args:
            degree: The degree of the root to be calculated.
        """
        try:
            self.result = self.result ** Decimal((1 / degree))
            return
        except InvalidOperation:
            print(f"!!! Sorry, this operation is not possible: {degree} degree root of \
                  {self.result}. Resetting the memory to 0.")
            self.result = Decimal(0)
            return


def get_valid_number(prompt: str) -> Decimal:
    """
    Prompts the user for a valid number input and returns the input as a float.
    The function is on an infinite loop untill a valid input is provided.

    Args:
        prompt: The prompt message displayed to the user.

    Returns:
        The valid number input as a float.

    Raises:
        ValueError: If the input cannot be converted to a float.
        TypeError: If the input is of an incorrect type.

    """
    attempts = 0
    while attempts < MAX_ATTEMPTS:
        try:
            value = Decimal(input(prompt))
            return value
        except InvalidOperation:
            print("Invalid number input. Should be integer or float.")
            attempts += 1
    if attempts == 3:
        print("Too many error attempts, quitting the calculator.")
        sys.exit()


def get_valid_operation(prompt: str, options) -> str:
    """
    Prompts the user for a valid operation input and returns the input as a string.
    The function is on an infinite loop until a valid input is provided.

    Args:
        prompt: The prompt message displayed to the user.

    Returns:
        The valid operation input as a string.

    Raises:
        ValueError: If the input is not a valid operation option.

    """
    attempts = 0
    while attempts < MAX_ATTEMPTS:
        try:
            value = (input(prompt)).lower()
            if value in options:
                return value
            else:
                raise ValueError(f'{value!r} not a valid option.  should be one of: {options}')
        except (ValueError, TypeError) as e:
            print(f"Invalid operation input: {e}.")
            attempts += 1
    if attempts == 3:
        print("Too many error attempts, quitting the calculator.")
        sys.exit()


def run_interface() -> None:

    # Set precision for Decimal calculations.
    getcontext().prec = PRECISION

    # Welcome the user
    print("Welcome to the calculator")
    print("Use it to add, subtract, multiply, divide, or take a root")

    # Initiate the calculator
    calculator = Calculator()

    # Start arythmetic operations with a reset (0) calculator result.
    while True:
        # Get the valid first argument input from the user
        first_number = get_valid_number("Enter the first element (integer or float): ")
        calculator.result = first_number

        # Until reset is True, keep modifying the last calculator result.
        reset = False
        while not reset:
            # Get the valid arythmetic operation input from the user
            operation = get_valid_operation(
                "Enter arithmetic operation (options: +, -, *, /, **): ", MATH_OPERATIONS)

            # Get the valid second argument input from the user
            second_number = get_valid_number(
                "Enter the second element (integer or float): ")

            # Perform the math operation
            if operation == '+':
                calculator.add(second_number)
            elif operation == '-':
                calculator.subtract(second_number)
            elif operation == '*':
                calculator.multiply(second_number)
            elif operation == '/':
                calculator.divide(second_number)
            elif operation == '**':
                calculator.root(second_number)

            # Print the current result
            print(f"Result: {calculator.result}\n")

            # Get valid user input for the next action
            next_action = get_valid_operation(
                "C to continue with the result, R to reset the calculator, Q to quit: ", ACTIONS)
            if next_action == 'c':
                continue
            elif next_action == 'r':
                calculator.clear_result()
                reset = True
            elif next_action == 'q':
                print("Thank you for using the calculator")
                sys.exit()


if __name__ == '__main__':
    run_interface()
