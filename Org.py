#!/usr/bin/env python
from dataclasses import dataclass


@dataclass
class Org:
    """
    Модель организатора дней рождений
    """

    id: int
    name: str
    chat_id: int
