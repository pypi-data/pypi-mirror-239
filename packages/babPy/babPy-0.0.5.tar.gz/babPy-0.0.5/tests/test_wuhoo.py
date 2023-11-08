import pytest
from babpy.talk import wuhoo

class Tests:
     
    def test_sanity_check(self):
        expected = True
        actual = True
        assert actual == expected, "Expected True to be equal to True"

    def test_simple_counter_condition(self):
        counter = [5]
        def condition():
            return counter[0] > 0
        def operation():
            counter[0] -= 1
        wuhoo(condition, operation)
        assert counter[0] == 0

    def test_complex_condition(self):
        data = {"value": 10}
        def condition():
            return data["value"] < 15
        def operation():
            data["value"] += 1
        wuhoo(condition, operation)
        assert data["value"] == 15

    def test_no_iteration(self):
        condition_called = [False]
        def condition():
            condition_called[0] = True
            return False
        def operation():
            pass  
        wuhoo(condition, operation)
        assert condition_called[0] is True
       



    
    