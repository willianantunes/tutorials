def strip_left_and_right_sides(value: str, rules: str = " \t\r\n") -> str:
    return value.strip(rules)
