from typing import Union


def rupiah(val: Union[int, float]) -> str:
    return f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")