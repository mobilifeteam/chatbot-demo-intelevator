def add_dict(a, b):
    if (
        (type(a) is int or type(a) is float) and
        (type(b) is int or type(b) is float)
    ):
        return a + b
    
    if (
        (type(a) is not dict and type(a) is not list) or
        (type(b) is not dict and type(b) is not list)
    ):
        return a

    for key in (b if type(b) is dict else range(len(b))):
        if (
            key not in a
            if type(a) is dict
            else key >= len(a)
        ):
            while type(a) is list and len(a) <= key:
                a.append(None)
            a[key] = b[key]
        elif type(a[key]) == type(b[key]):
            a[key] = add_dict(a[key], b[key])
    return a


def uniform_list(size):
    size = int(size)
    return [1.0 / size] * size


def sum_list(value_list):
    total = 0
    for value in value_list:
        if type(value) is int or type(value) is float:
            total += value
        elif type(value) is tuple or type(value) is list:
            total += sum_list(value)
    return total


def normalize_list(value_list, total=None):
    if total is None:
        total = sum_list(value_list)

    return [
        (
            value / total
            if type(value) is int or type(value) is float
            else (
                normalize_list(value, total)
                if type(value) is tuple or type(value) is list
                else []
            )
        ) for value in value_list
    ]


def day_to_number(day_name):
    value = {
        "sun": 0,
        "mon": 1,
        "tue": 2,
        "wed": 3,
        "thu": 4,
        "fri": 5,
        "sat": 6
    }[day_name[:3].lower()]

    return -1 if value is None else value


def number_to_day(day_number):
    return [
        "sunday",
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday"
    ][day_number]
