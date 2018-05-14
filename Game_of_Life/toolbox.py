def get_integer(prompt):
    """Asks the user the prompt and verifies they enter an integer"""
    if prompt[-1] != " ":
        prompt = prompt + " "
    number = input(prompt)
    prompt = prompt + "(integers only) "
    while not is_integer(number):
        number = input(prompt)
    number = int(number)
    return number

def is_integer(number):
    """Returns True is number is an interger else it returns False."""
    isInteger = True
    number = str(number).strip()
    if number in ['', '.', '+', '-']:
        isInteger = False
    if isInteger and number[0] in '+-':
        number = number[1:]
    position = 0
    legalValues = '0123456789.'
    while isInteger and position <= len(number) - 1:
        if number[position] not in legalValues:
            isInteger = False
        if number[position] == '.':
            legalValues = '0'
        position += 1
    return isInteger

def get_string(prompt):
    """Get and return a non-empty string"""
    if prompt[-1] != " ":
        prompt = prompt + " "
    string = input(prompt)
    while not string and not "":
        if prompt[-31:] != " (you have to enter something) ":
            prompt = prompt + "(you have to enter something) "
        string = input(prompt)
    return string

def get_boolean(prompt):
    """Ask the user a yes or no question"""
    prompt = prompt + " (y/n) "
    answer = input(prompt)
    answer = answer.lower()
    if answer in ['yes', 'sure', 'yeah', 'true', 'absolutely', 'y', 'da', 'si']:
        answer = True
    elif answer in ['n', 'no', 'nope', 'nah']:
        answer = False
    else:
        prompt = "Does " + answer + " mean yes or no?"
        answer = get_boolean(prompt)
    return answer

def yes_or_no(prompt):
    """This allows my older code to work."""
    return get_boolean(prompt)

def is_number(number):
    '''Returns True is testValue is a number, otherwise returns False.'''
    isNumber = True
    testValue = str(number)
    isNumber = True
    number = str(number).strip()
    if number in ['', '.', '+', '-']:
        isNumber = False
    if isNumber and number[0] in '+-':
        number = number[1:]
    legalValues = '.0123456789'
    for character in number:
        if character not in legalValues:
            isNumber = False
        if character == '.':
            legalValues = '0123456789'
    return isNumber

def get_number(prompt):
    """Asks the user the prompt and verifies they enter a float"""
    if prompt[-1] != " ":
        prompt += " "
    number = input(prompt)
    while not is_number(number):
        if prompt[-16:] != " (numbers only) ":
            prompt = prompt + "(numbers only) "
        number = input(prompt)
    number = float(number)
    return number

def get_positive_number(prompt):
    """returns a positive number."""
    number = get_number(prompt)
    while number < 0:
        print("You have to enter a positive value.")
        number = get_number(prompt)
    return number