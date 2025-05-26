from datetime import datetime

def parse_datetime(value) -> datetime:
    """
    Converte diferentes formatos de data para um objeto datetime.

    :param value: Valor a ser convertido (string de data ou timestamp)
    :return: Objeto datetime
    """
    if value is None:
        return None

    # Se já for um objeto datetime
    if isinstance(value, datetime):
        return value

    # Se for uma string, tenta converter usando diferentes formatos
    if isinstance(value, str):
        try:
            return datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            try:
                return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                pass

    # Se for um número ou string numérica, trata como timestamp
    try:
        return datetime.fromtimestamp(int(value))
    except (ValueError, TypeError):
        raise ValueError(f"Formato de data inválido: {value}")