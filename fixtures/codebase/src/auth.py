"""Tiny fixture module — locator target for auth.login."""


def login(user: str) -> bool:
    return bool(user)
