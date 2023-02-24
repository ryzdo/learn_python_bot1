import doctest


def calc(string: str) -> str | float:
    """
    Performs basic arithmetic operations with two numbers: addition, subtraction, multiplication and division.

    >>> calc('2-3')
    -1.0
    >>> calc('1')
    'Строка "1" не является алгебраическим выражением'
    >>> calc('2+3')
    5.0
    >>> calc('2*3')
    6.0
    >>> calc('3/2')
    1.5
    >>> calc('3/0')
    'Делить на ноль нельзя'
    >>> calc('120-13')
    107.0
    >>> calc('12.5-13')
    -0.5
    >>> calc('12б')
    'Строка "12б" не является алгебраическим выражением'
    >>> calc(None)
    'Введите алгебраическое выражение после /calc'
    >>> calc('12 - 13')
    -1.0
    >>> calc('1 2-13')
    'Строка "1 2-13" не является алгебраическим выражением'
    >>> calc('120-13-6.5')
    100.5
    >>> calc('120-13*2')
    94.0
    """
    index_operation: int = 0
    operations: str = '+-*/'

    if not string:
        return 'Введите алгебраическое выражение после /calc'
    elif string.isalnum():
        return f'Строка "{string}" не является алгебраическим выражением'

    for index in range(len(string)):
        if string[index] in operations:
            index_operation = index

    number_str_1: str = string[:index_operation].strip()
    number_str_2: str = string[index_operation+1:].strip()
    operation: str = string[index_operation]

    try:
        number1: float = float(number_str_1)
        number2: float = float(number_str_2)
    except (ValueError, TypeError):
        return f'Строка "{string}" не является алгебраическим выражением'

    if operation == '+':
        return number1 + number2
    elif operation == '-':
        return number1 - number2
    elif operation == '/':
        if not number2:
            return 'Делить на ноль нельзя'
        return number1 / number2
    elif operation == '*':
        return number1 * number2

    return '????'


if __name__ == "__main__":
    doctest.testmod()
    print(calc(input('Введи алгебраическое выражение: ')))
