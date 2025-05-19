class EntityNotFoundError(Exception):
    """Exceção lançada quando uma entidade não é encontrada no repositório."""

    def __init__(self, entity_name: str, identifier=None, message=None):
        self.entity_name = entity_name
        self.identifier = identifier
        self.message = message or f"{entity_name} não encontrado{'' if identifier is None else f' com identificador {identifier}'}"
        super().__init__(self.message)

    def __str__(self):
        return self.message