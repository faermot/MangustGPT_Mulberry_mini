def format_number(number):
    if number >= 1000000:
        millions = round(number / 1000000)
        if millions >= 1000:
            return f"{round(millions / 1000)}м"
        else:
            return f"{millions}м"
    elif number >= 100000:
        thousands = round(number / 1000)
        if thousands >= 1000:
            return f"{round(thousands / 1000)}k"
        else:
            return f"{thousands}к"
    else:
        return "{:,}".format(number).replace(",", " ")
