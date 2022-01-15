from api.validate import check_null_value


def test_check_null_value():
    assert check_null_value(7) == 7
    assert check_null_value("null") is None
