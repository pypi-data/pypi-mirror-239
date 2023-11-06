from codes.design.singleton1 import singleton1


def test_1():
    singleton1.val = 1
    assert singleton1.val == 1


def test_2():
    assert singleton1.val == 1
