#!/usr/bin/env python
import random
import string


def generate_secret_code() -> str:
    return "".join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=48))
