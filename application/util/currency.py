def br(value):
    formatted = f"R$ {value:,.2f}"
    return formatted.replace(',', 'X').replace('.', ',').replace('X', '.')