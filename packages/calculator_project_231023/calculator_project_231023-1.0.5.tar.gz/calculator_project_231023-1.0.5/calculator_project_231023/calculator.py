from typing import Union

from decimal import Decimal, getcontext, InvalidOperation

PRECISION = 10
MATH_OPERATIONS = {
    '+': 'add',
    '-': 'subtract',
    '*': 'multiply',
    '/': 'divide',
    '**': 'root'
}
ACTIONS = ['c', 'r', 'q']
MAX_ATTEMPTS = 3


class Calculator:
    """
    Performs the inbuilt Python math operations of addition (+), subtraction (-),
    multiplication (*), and division (/). It can also take (n) root of a number
    by using Python inbuilt exponentiation operation (**). The calculator stores one most recent
    operation result and appies additional operations to that result until explicitly instructed to
    clear the result. All the operations are carried out in the Decimal format for more precision.

    !!! Note: the class methods were designed to be used through the interface function, not as
    stand alone methods, so they do not have extensive input validation attached to them. This is
    by design.

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
        perform_peration(operator: str, operand: Decimal): retrived the respective calculation
            method, runs it, updates the calculator result and prints the result.
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

        Works only on positive numbers.

        Args:
            degree: The degree of the root to be calculated.

        Raises:
            InvalidOperation: If the operation cannot be carried out, e.g. negative number root.
        """
        try:
            self.result = self.result ** Decimal((1 / degree))
            return
        except InvalidOperation:
            print(f"Sorry, this operation is not possible: {degree} degree root of {self.result}.")
            return

    def perform_operation(self, operator: str, operand: Decimal) -> None:
        """
        Performs the specified operation on the current result with the given operand.

        Args:
            operator: The math operation to be performed.
            operand: The value to be used in the operation.
        """
        operation_method = MATH_OPERATIONS.get(operator)
        if operation_method is None:
            print(f"Invalid operation: {operator}")
            return

        try:
            getattr(self, operation_method)(Decimal(operand))
            print(f"Result: {self.result}\n")
            return
        except InvalidOperation:
            print("Invalid operand or operation.")
            return


def get_valid_number(prompt: str) -> tuple[Decimal, bool, bool]:
    """
    Prompts the user for a valid number input and returns a valid input as
    a Decimal, or the information for the parent function to quit the calculator.
    The function iterates 3 times if an invalid input is provided.

    Args:
        prompt: The prompt message displayed to the user.

    Returns:
        A tuple with 3 components:
        If the input was valid - the valid number input as a Decimal and False markers for breaking
        the interface loop.
        If the input was invalid - the Decimal(0) and True markers for breaking the interface loop -
        this will cause the run_inteface() function to exit the calculator nicely.

    Raises:
        InvalidOperation: If the number input cannot be converted to Decimal format.
    """
    attempts = 0
    while attempts < MAX_ATTEMPTS:
        try:
            value = Decimal(input(prompt))
            return value, False, False
        except InvalidOperation:
            print("Invalid number input. Should be integer or float.")
            attempts += 1

    print("Too many error attempts, quitting the calculator.")
    return Decimal(0), True, True


def get_valid_operation(prompt: str, options) -> tuple[Union[None, str], bool, bool]:
    """
    Prompts the user for a valid operation input and returns a valid string, or the information
    for the parent function to quit the calculator.
    The function iterates 3 times if an invalid input is provided.

    Args:
        prompt: The prompt message displayed to the user.

    Returns:
        A tuple with 3 components:
        If the input was valid - the valid string and False markers for breaking
        the interface loop.
        If the input was invalid - the None value and True markers for breaking the interface loop -
        this will cause the run_inteface() function to exit the calculator nicely.

    Raises:
        ValueError or TypeError: If the input is not a valid operation option.

    """
    attempts = 0
    while attempts < MAX_ATTEMPTS:
        try:
            value = (input(prompt)).lower()
            if value in options:
                return value, False, False
            else:
                raise ValueError(f'{value!r} not a valid option.  should be one of: {options}')
        except (ValueError, TypeError) as e:
            print(f"Invalid operation input: {e}.")
            attempts += 1

    print("Too many error attempts, quitting the calculator.")
    return None, True, True


def run_interface() -> None:
    """
    This is the main function for interfacing between the user and the calculator class.
    It runs other functions which ask the user to provide calculator inputs.
    It sets the Decimal calculation precision (default is 10 digits).
    It initiates the calculator and instructs it to carry out calculations.
    It controls and resets the calculator memory.
    It controls when to quit the calculator:
        - when the user chooses to quit
        - when 3 consequitive invalid number or operation inputs are provided, this is done
        intentionaly for demo purposes to avoid using infinite loops

    Args:
        calculator: the instance of the Calculator class used to carry out operations.
        shoud_exit: variable used to control when to exit the calculator.
        reset: variable used to control when to reset the calculator memory.
        first_number: first numeric argument provided by the user for calculation.
        second_number: second numeric argument provided by the user for calculation.
        operation: math operation selected by the user to be carried out.
        next_action: user selection how to proceed after each math calculation
                    (continue, reset, or quit).
    """

    # Set precision for Decimal calculations.
    getcontext().prec = PRECISION

    # Welcome the user
    print("Welcome to the calculator")
    print("Use it to add, subtract, multiply, divide, or take a root")

    # Initiate the calculator
    calculator = Calculator()
    should_exit = False
    # Start arythmetic operations with a reset (0) calculator result.
    while not should_exit:
        # Get the valid first argument input from the user
        first_number, should_exit, _ = \
            get_valid_number("Enter the first element (integer or float): ")
        if should_exit is True:
            break
        calculator.result = first_number

        # Until reset is True, keep modifying the last calculator result.
        reset = False
        while not reset:

            # Get the valid arythmetic operation input from the user
            math_operations_list = list(MATH_OPERATIONS.keys())
            if calculator.result >= 0:
                operation, should_exit, reset = get_valid_operation(
                    "Enter operation (options: +, -, *, /, **): ", math_operations_list)
                # If no valid operation was returned, this is an indication to exit the calculator.
                if reset is True:
                    break
            else:
                operation, should_exit, reset = get_valid_operation(
                    "Enter operation (negative number root not possible). Options: +, -, *, /  ",
                    math_operations_list[:-1])
                # If no valid operation was returned, this is an indication to exit the calculator.
                if reset is True:
                    break

            # Get the valid second argument input from the user
            second_number, should_exit, reset = get_valid_number(
                "Enter the second element (integer or float): ")
            # If no valid number was returned, this is an indication to exit the calculator.
            if reset is True:
                break

            # Perform the math operation
            if operation:  # This check is for mypy, otherwise there is a type incompatibility.
                calculator.perform_operation(operation, second_number)

            # Get valid user input for the next action
            next_action, should_exit, reset = get_valid_operation(
                "C to continue with the result, R to reset the calculator, Q to quit: ", ACTIONS)
            print(reset)
            print(should_exit)
            if reset is True:
                break
            elif next_action == 'c':
                continue
            elif next_action == 'r':
                calculator.clear_result()
                reset = True
            elif next_action == 'q':
                print("Thank you for using the calculator")
                reset = True
                should_exit = True


if __name__ == '__main__':
    run_interface()
