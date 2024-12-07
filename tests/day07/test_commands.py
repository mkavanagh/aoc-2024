from day07.commands import default_solver


def test_default_solver():
    assert default_solver.can_solve(5, [4, 1]) == True
    assert default_solver.can_solve(5, [2, 2, 1]) == True
    assert default_solver.can_solve(5, [1, 1, 1, 1, 1]) == True
    assert default_solver.can_solve(5, [1, 1, 1, 1, 1, 0]) == True
