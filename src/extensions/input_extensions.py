def read_int(prompt):
    while True:
        value = input(prompt)
        if value.isdigit():
            return int(value)
