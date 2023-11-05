from calculator_project_231023.calculator import Calculator, run_interface, get_valid_number, \
    get_valid_operation, MATH_OPERATIONS, ACTIONS
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
    assert calculator.result == Decimal(-8)


def test_1_perform_operation():
    test_inputs = [
        ("+", Decimal("3.14"), Decimal("5.14")),    # Valid input
        ("-", Decimal("1"), Decimal("1")),          # Valid input
        ("*", Decimal("2"), Decimal("4")),          # Valid input
        ("/", Decimal("2"), Decimal("1")),          # Valid input
        ("**", Decimal("1"), Decimal("2")),         # Valid input
        (" ", Decimal("3.14"), Decimal("2")),       # Invalid input
        (" ", "dafdadds", Decimal("2")),            # Invalid input
    ]

    for operation, operand, expected_result in test_inputs:
        calculator = Calculator()
        calculator.result = Decimal(2)
        calculator.perform_operation(operation, operand)
        assert calculator.result == expected_result


def test_2_perform_operation(capsys):
    test_inputs = [
        (" ", Decimal("3.14"), "Invalid operation:"),       # Invalid input
        ("afda", Decimal("3.14"), "Invalid operation:"),    # Invalid input
        ("+", "dfadsf", "Invalid operand or operation."),   # Invalid input
    ]

    for operation, operand, expected_result in test_inputs:
        calculator = Calculator()
        calculator.result = Decimal(2)
        calculator.perform_operation(operation, operand)
        captured = capsys.readouterr()  # Capture the output
        output_text = captured.out  # Get the captured stdout as a string
        assert expected_result in output_text


def test_get_valid_number(monkeypatch):
    test_inputs = [
        ("3.14", (Decimal("3.14"), False, False)),  # Valid input: decimal number
        ("10", (Decimal("10"), False, False)),      # Valid input: integer number
        ("-5", (Decimal("-5"), False, False)),      # Valid input: negative number
        ("abc", (0, True, True)),                   # Invalid input: non-numeric string
        ("2.5.3", (0, True, True)),                 # Invalid input: multiple decimal points
        ("1,000", (0, True, True)),                 # Invalid input: comma separator
        ("1 000", (0, True, True)),                 # Invalid input: space separator
        (" ", (0, True, True)),                     # Invalid input: empty space
    ]

    for user_input, expected_output in test_inputs:
        monkeypatch.setattr('builtins.input', lambda _: user_input)  # Mock user input
        number = get_valid_number("Enter a number: ")
        assert number == expected_output


def test_1_get_valid_operation(monkeypatch):
    test_inputs = [
        ("+", ("+", False, False)),     # Valid input: addition
        ("-", ("-", False, False)),     # Valid input: subtraction
        ("*", ("*", False, False)),     # Valid input: multiplication
        ("/", ("/", False, False)),     # Valid input: division
        ("**", ("**", False, False)),   # Valid input: root
        ("abc", (None, True, True)),    # Invalid input: non-numeric string
        ("2.5.3", (None, True, True)),  # Invalid input: multiple decimal points
        ("1,000", (None, True, True)),  # Invalid input: comma separator
        ("1 000", (None, True, True)),  # Invalid input: space separator
        (" ", (None, True, True)),      # Invalid input: empty space
    ]

    for user_input, expected_output in test_inputs:
        monkeypatch.setattr('builtins.input', lambda _: user_input)  # Mock user input
        operation = get_valid_operation(
            "Enter arithmetic operation (options: +, -, *, /, **): ", list(MATH_OPERATIONS.keys()))
        assert operation == expected_output


def test_2_get_valid_operation(monkeypatch):
    test_inputs = [
        ("C", ("c", False, False)),       # Valid input: continue
        ("R", ("r", False, False)),       # Valid input: reset
        ("Q", ("q", False, False)),       # Valid input: quit
        ("c", ("c", False, False)),       # Valid input: continue
        ("r", ("r", False, False)),       # Valid input: reset
        ("q", ("q", False, False)),       # Valid input: quit
        ("abc", (None, True, True)),      # Invalid input: non-numeric string
        ("2.5.3", (None, True, True)),    # Invalid input: multiple decimal points
        ("1,000", (None, True, True)),    # Invalid input: comma separator
        ("1 000", (None, True, True)),    # Invalid input: space separator
        (" ", (None, True, True)),        # Invalid input: empty space
    ]

    for user_input, expected_output in test_inputs:
        monkeypatch.setattr('builtins.input', lambda _: user_input)  # Mock user input

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
        run_interface()
        captured = capsys.readouterr()  # Capture the output
        output_text = captured.out  # Get the captured stdout as a string
        print(output_text)
        assert inputs[-1] in output_text


def test_complex_run_interface(monkeypatch, capsys):
    test_inputs = [
        # Test case 1: Reset
        ["1", "+", "2", "r", "2", "+", "2", "q", "Result: 3", "Result: 4", \
         "Calculator reset to 0"],
        # Test case 2: Continue
        ["1", "+", "2", "c", "+", "2", "q", "Result: 3", "Result: 5"],
        # Test case 3: Invalid number inputs
        ["1", "+", "2", "c", "+", "erwq", "erwq", "erwq", \
            "Invalid number input. Should be integer or float.", \
            "Too many error attempts, quitting the calculator."],
        # Test case 4: Invalid operation inputs
        ["1", "+", "2", "c", "erwq", "erwq", "erwq", "Invalid operation input:", \
            "Too many error attempts, quitting the calculator."],
        # Test case 5: Root of a negative number
        ["1", "+", "-20", "c", "**", "-", "5", "q", "Result: -24"],
    ]

    for inputs in test_inputs:
        monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0))
        run_interface()
        captured = capsys.readouterr()  # Capture the output
        output_text = captured.out  # Get the captured stdout as a string
        print(output_text)
        for remaining_input in inputs:
            assert remaining_input in output_text
