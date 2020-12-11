#!/usr/bin/env python
import random


def generate_secret_code() -> str:
    return "".join(random.choices(str.ascii_uppercase + str.digits, k=64))
