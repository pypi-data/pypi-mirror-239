import pytest
from  babpy.talk import fuh

class Tests:
    def test_sanity_check(self):
        expected = True
        actual = True
        assert actual == expected, "Expected True to be equal to True"
    
    def test_fuh_valid_true_condition(self):
        # Test that fuh correctly returns the result of the if_true callable
        condition = True
        if_true = lambda: "Correct"
        if_false = lambda: "Incorrect"
        expected = "Correct"
        actual = fuh(condition, if_true, if_false)
        assert actual == expected, "fuh should return 'Correct' when the condition is True"

    def test_fuh_valid_false_condition(self):
        # Test that fuh correctly returns the result of the if_false callable
        condition = False
        if_true = lambda: "Incorrect"
        if_false = lambda: "Correct"
        expected = "Correct"
        actual = fuh(condition, if_true, if_false)
        assert actual == expected, "fuh should return 'Correct' when the condition is False"

    def test_fuh_invalid_if_true(self):
        # Test that fuh raises ValueError if if_true is not callable
        condition = True
        if_true = "Not callable"
        if_false = lambda: "Correct"
        with pytest.raises(ValueError):
            fuh(condition, if_true, if_false)

    def test_fuh_invalid_if_false(self):
        # Test that fuh raises ValueError if if_false is not callable
        condition = False
        if_true = lambda: "Correct"
        if_false = "Not callable"
        with pytest.raises(ValueError):
            fuh(condition, if_true, if_false)

if __name__ == "__main__":
    pytest.main()
