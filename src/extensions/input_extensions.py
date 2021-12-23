def read_int(prompt):
    while True:
        value = input(prompt)
        if value.replace('-', '').isdigit():
            return int(value)
