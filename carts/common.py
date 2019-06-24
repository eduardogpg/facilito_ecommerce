from enum import Enum

class CartStatus(Enum):
    CREATED = 'CREATED'
    CLOSED = 'CLOSED'

choices = [(tag, tag.value) for tag in CartStatus]
