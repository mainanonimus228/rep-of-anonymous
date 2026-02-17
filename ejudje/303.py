def is_operator(c):
    return c in "+-*"

# Mapping triplets to digits
str_to_digit = {
    "ZER": "0",
    "ONE": "1",
    "TWO": "2",
    "THR": "3",
    "FOU": "4",
    "FIV": "5",
    "SIX": "6",
    "SEV": "7",
    "EIG": "8",
    "NIN": "9"
}

# Reverse mapping
digit_to_str = {v: k for k, v in str_to_digit.items()}


def convert_to_number(s):
    number = ""
    for i in range(0, len(s), 3):
        triplet = s[i:i+3]
        number += str_to_digit[triplet]
    return int(number)


def convert_to_string(num):
    if num == 0:
        return "ZER"
    
    result = ""
    for digit in str(num):
        result += digit_to_str[digit]
    return result


def calculate_expression(s):
    # Find operator position
    for i in range(len(s)):
        if is_operator(s[i]):
            operator = s[i]
            left = s[:i]
            right = s[i+1:]
            break

    num1 = convert_to_number(left)
    num2 = convert_to_number(right)

    if operator == "+":
        result = num1 + num2
    elif operator == "-":
        result = num1 - num2
    else:  # "*"
        result = num1 * num2

    return convert_to_string(result)


# ---- Main ----
s = input().strip()
print(calculate_expression(s))
