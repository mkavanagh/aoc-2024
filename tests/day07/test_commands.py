from day07.commands import _can_satisfy


def test_can_satisfy():
    assert _can_satisfy(5, [4, 1]) == True
    assert _can_satisfy(5, [2, 2, 1]) == True
    assert _can_satisfy(5, [1, 1, 1, 1, 1]) == True
    assert _can_satisfy(5, [1, 1, 1, 1, 1, 0]) == True
