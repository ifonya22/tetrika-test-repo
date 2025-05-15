import pytest

from solution import strict


@strict
def sum_two_int(a: int, b: int) -> int:
    return a + b


@strict
def sum_two_return_diff_type(a: int, b: int) -> float:
    return a + b


def test_correct_args():
    assert sum_two_int(322, 222) == 544
    assert sum_two_int(a=-756, b=756) == 0
    assert sum_two_int(b=100_000_000_000, a=100_000_000_000) == 200_000_000_000


def test_wrong_type():
    with pytest.raises(TypeError, match="Аргумент a=1.0 имеет тип float вместо ожидаемого int"):
        sum_two_int(1.0, 2)

    with pytest.raises(TypeError, match="Аргумент a=True имеет тип bool вместо ожидаемого int"):
        sum_two_int(True, 2)

    with pytest.raises(TypeError, match="Аргумент a=dva имеет тип str вместо ожидаемого int"):
        sum_two_int("dva", 2)

    with pytest.raises(TypeError, match="Аргумент b=2.0 имеет тип float вместо ожидаемого int"):
        sum_two_int(1, 2.0)

    with pytest.raises(TypeError, match="Аргумент b=False имеет тип bool вместо ожидаемого int"):
        sum_two_int(1, False)

    with pytest.raises(TypeError, match="Аргумент b=tri имеет тип str вместо ожидаемого int"):
        sum_two_int(1, "tri")

    with pytest.raises(TypeError, match="Аргумент a=1.0 имеет тип float вместо ожидаемого int"):
        sum_two_int(1.0, b=2)

    with pytest.raises(TypeError, match="Аргумент a=True имеет тип bool вместо ожидаемого int"):
        sum_two_int(True, b=2)

    with pytest.raises(TypeError, match="Аргумент a=dva имеет тип str вместо ожидаемого int"):
        sum_two_int("dva", b=2)

    with pytest.raises(TypeError, match="Аргумент b=2.0 имеет тип float вместо ожидаемого int"):
        sum_two_int(a=1, b=2.0)

    with pytest.raises(TypeError, match="Аргумент b=False имеет тип bool вместо ожидаемого int"):
        sum_two_int(a=1, b=False)

    with pytest.raises(TypeError, match="Аргумент b=tri имеет тип str вместо ожидаемого int"):
        sum_two_int(a=1, b="tri")


def test_wrong_return_type():
    with pytest.raises(TypeError, match="Результат выполнения функции 3 имеет тип int вместо ожидаемого float"):
        sum_two_return_diff_type(1, 2)


def test_too_many_args():
    with pytest.raises(TypeError):
        sum_two_int(1, 2.0, 3.0)


def test_missing_args():
    with pytest.raises(IndexError):
        sum_two_int(1)
    with pytest.raises(IndexError):
        sum_two_int(b=2.0)
