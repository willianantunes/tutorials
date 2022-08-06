def return_none_if_provided_value_is_falsy_or_strange(value):
    if value is not None and (value == "" or value == b"" or value in (".", "none")):
        return None
    return value


def clean_dict_with_falsy_or_strange_values(value: dict) -> dict:
    return {k: v for k, v in value.items() if return_none_if_provided_value_is_falsy_or_strange(v) or v == 0}
