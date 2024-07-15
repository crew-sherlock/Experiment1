def test_print():
    try:
        print("Hello") is None
    except ValueError:
        print("Test print function failed.")
        assert False
