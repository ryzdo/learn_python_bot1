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
    index_operation: int = -1
    operations: str = '+-*/'
    numbers_str: list[str] = []
    operations_list: list[str] = []

    if not string:
        return 'Введите алгебраическое выражение после /calc'
    elif string.isalnum():
        return f'Строка "{string}" не является алгебраическим выражением'

    for index in range(len(string)):
        if string[index] in operations:
            numbers_str.append(string[index_operation+1:index])
            operations_list.append(string[index])
            index_operation = index
    numbers_str.append(string[index_operation+1:])

    try:
        numbers: list[float] = []
        for number in numbers_str:
            numbers.append(float(number.strip()))
    except (ValueError, TypeError):
        return f'Строка "{string}" не является алгебраическим выражением'

    result: float = numbers[0]
    for index in range(len(operations_list)):
        if operations_list[index] == '+':
            result += numbers[index+1]
        elif operations_list[index] == '-':
            result -= numbers[index+1]
        elif operations_list[index] == '/':
            if not numbers[index+1]:
                return 'Делить на ноль нельзя'
            result /= numbers[index+1]
        elif operations_list[index] == '*':
            result *= numbers[index+1]

    return result


if __name__ == "__main__":
    doctest.testmod()
    print(calc(input('Введи алгебраическое выражение: ')))
