def format_money(cents: int) -> str:
    return f"{cents / 100:.2f}"


def split_sku(sku: str) -> tuple[str, str]:
    head, _, tail = sku.partition("-")
    return head, tail
