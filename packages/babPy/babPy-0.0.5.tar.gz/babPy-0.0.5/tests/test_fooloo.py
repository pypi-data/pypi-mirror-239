import pytest
from  babpy.talk import fooloo

class Tests:
    def test_sanity_check(self):
        expected = True
        actual = True
        assert actual == expected, "Expected True to be equal to True"
    
    def test_valid_param(self):
        result = []
        fooloo(3, 1, lambda i: result.append(i))
        assert result == [1, 2, 3]

    def test_boundary_conditions(self):
        result = []
        fooloo(1, 1, lambda i: result.append(i))
        assert result == [1]

        result.clear()
        fooloo(1, 2, lambda i: result.append(i))
        assert result == []

        result.clear()
        fooloo(2, 1, lambda i: result.append(i))
        assert result == [1, 2]

    def test_fooloo_n_less_than_1(self):
        result = []
        def test_function(x):
            result.append(x)
        fooloo(1, 5, test_function)
        assert result == []

if __name__ == "__main__":
    pytest.main()