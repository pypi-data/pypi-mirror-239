import pytest
from calculator_project_231023.calculator import Calculator, run_interface, get_valid_number, get_valid_operation, \
    MATH_OPERATIONS, ACTIONS
from decimal import Decimal


def test_my_class():
    calculator = Calculator()
    assert calculator.result == 0  # Set a zero result


def test_clear_result():
    calculator = Calculator()
    calculator.result = Decimal(10)  # Set a non-zero result
    calculator.clear_result()
    assert calculator.result == Decimal(0)


def test_add():
    calculator = Calculator()
    calculator.result = Decimal(5)
    calculator.add(Decimal(3))
    assert calculator.result == Decimal(8)


def test_subtract():
    calculator = Calculator()
    calculator.result = Decimal(5)
    calculator.subtract(Decimal(3))
    assert calculator.result == Decimal(2)


def test_multiply():
    calculator = Calculator()
    calculator.result = Decimal(5)
    calculator.multiply(Decimal(3))
    assert calculator.result == Decimal(15)


def test_divide():
    calculator = Calculator()
    calculator.result = Decimal(10)
    calculator.divide(Decimal(2))
    assert calculator.result == Decimal(5)


def test_root():
    calculator = Calculator()
    calculator.result = Decimal(9)
    calculator.root(Decimal(2))
    assert calculator.result == Decimal(3)


def test_2_root():
    calculator = Calculator()
    calculator.result = Decimal(-8)  # Test for negative number root
    calculator.root(Decimal(2))
    assert calculator.result == Decimal(0)


def test_1_get_valid_number(monkeypatch):
    test_inputs = [
        ("3.14", Decimal("3.14")),  # Valid input: decimal number
        ("10", Decimal("10")),      # Valid input: integer number
        ("-5", Decimal("-5")),      # Valid input: negative number
    ]

    for user_input, expected_output in test_inputs:
        monkeypatch.setattr('builtins.input', lambda _: user_input)  # Mock user input

        number = get_valid_number("Enter a number: ")
        assert number == expected_output


def test_2_get_valid_number(monkeypatch):
    test_inputs = [
        ("abc", None),               # Invalid input: non-numeric string
        ("2.5.3", None),             # Invalid input: multiple decimal points
        ("1,000", None),             # Invalid input: comma separator
        ("1 000", None),             # Invalid input: space separator
        (" ", None),                 # Invalid input: empty space
    ]

    for user_input, expected_output in test_inputs:
        monkeypatch.setattr('builtins.input', lambda _: user_input)  # Mock user input

        # Use pytest.raises() to catch the SystemExit exception
        with pytest.raises(SystemExit):
            number = get_valid_number("Enter a number: ")
            assert number == expected_output


def test_1_get_valid_operation(monkeypatch):
    test_inputs = [
        ("+", "+"),    # Valid input: addition
        ("-", "-"),    # Valid input: subtraction
        ("*", "*"),    # Valid input: multiplication
        ("/", "/"),    # Valid input: division
        ("**", "**"),  # Valid input: root
    ]

    for user_input, expected_output in test_inputs:
        monkeypatch.setattr('builtins.input', lambda _: user_input)  # Mock user input

        operation = get_valid_operation(
                "Enter arithmetic operation (options: +, -, *, /, **): ", MATH_OPERATIONS)
        assert operation == expected_output


def test_2_get_valid_operation(monkeypatch):
    test_inputs = [
        ("abc", None),    # Invalid input: non-numeric string
        ("2.5.3", None),  # Invalid input: multiple decimal points
        ("1,000", None),  # Invalid input: comma separator
        ("1 000", None),  # Invalid input: space separator
        (" ", None),                 # Invalid input: empty space
    ]

    for user_input, expected_output in test_inputs:
        monkeypatch.setattr('builtins.input', lambda _: user_input)  # Mock user input

        with pytest.raises(SystemExit):
            operation = get_valid_operation(
                "Enter arithmetic operation (options: +, -, *, /, **): ", MATH_OPERATIONS)
            assert operation == expected_output


def test_3_get_valid_operation(monkeypatch):
    test_inputs = [
        ("C", "c"),       # Valid input: continue
        ("R", "r"),       # Valid input: reset
        ("Q", "q"),       # Valid input: quit
        ("c", "c"),       # Valid input: continue
        ("r", "r"),       # Valid input: reset
        ("q", "q"),       # Valid input: quit
    ]

    for user_input, expected_output in test_inputs:
        monkeypatch.setattr('builtins.input', lambda _: user_input)  # Mock user input

        operation = get_valid_operation(
                "C to continue with the result, R to reset result to 0, Q to quit: ", ACTIONS)
        assert operation == expected_output


def test_4_get_valid_operation(monkeypatch):
    test_inputs = [
        ("abc", None),               # Invalid input: non-numeric string
        ("2.5.3", None),             # Invalid input: multiple decimal points
        ("1,000", None),             # Invalid input: comma separator
        ("1 000", None),             # Invalid input: space separator
        (" ", None),                 # Invalid input: empty space
    ]

    for user_input, expected_output in test_inputs:
        monkeypatch.setattr('builtins.input', lambda _: user_input)  # Mock user input

        with pytest.raises(SystemExit):
            operation = get_valid_operation(
                "C to continue with the result, R to reset result to 0, Q to quit: ", ACTIONS)
            assert operation == expected_output


def test_simple_run_interface(monkeypatch, capsys):
    test_inputs = [
        # Test case 1: Addition
        ["1", "+", "2", "q", "Result: 3"],
        # Test case 2: Addition floats
        ["2", "+", "-3.1", "q", "Result: -1.1"],
        # Test case 3: Subtraction
        ["5", "-", "3", "q", "Result: 2"],
        # Test case 4: Multiplication
        ["2", "*", "4", "q", "Result: 8"],
        # Test case 5: Multiplication floats
        ["2", "*", "-3.1", "q", "Result: -6.2"],
        # Test case 6: Division
        ["10", "/", "2", "q", "Result: 5"],
        # Test case 7: Division
        ["10", "/", "-3", "q", "Result: -3.333333333"],
        # Test case 7: Division
        ["98765432.1", "/", "12345678.9", "q", "Result: 8.000000073"],
        # Test case 8: Root
        ["9", "**", "2", "q", "Result: 3"],
    ]

    for inputs in test_inputs:
        monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0))

        with pytest.raises(SystemExit):
            run_interface()

        captured = capsys.readouterr()
        print(captured)
        print(captured.out)
        assert inputs[-1] in captured.out


def test_complex_run_interface(monkeypatch, capsys):
    test_inputs = [
        # Test case 1: Reset
        ["1", "+", "2", "r", "2", "+", "2", "q", "Result: 3", "Result: 4", \
         "Calculator reset to 0"],
        # Test case 1: Continue
        ["1", "+", "2", "c", "+", "2", "q", "Result: 3", "Result: 5"],
        # Test case 3: Invalid number inputs
        ["1", "+", "2", "c", "+", "erwq", "erwq", "erwq", \
            "Invalid number input. Should be integer or float.", \
            "Too many error attempts, quitting the calculator."],
        # Test case 4: Invalid operation inputs
        ["1", "+", "2", "c", "erwq", "erwq", "erwq", "Invalid operation input:", \
            "Too many error attempts, quitting the calculator."],
    ]

    for inputs in test_inputs:
        monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0))

        with pytest.raises(SystemExit):
            run_interface()

        captured = capsys.readouterr()
        for input in inputs:
            assert input in captured.out
