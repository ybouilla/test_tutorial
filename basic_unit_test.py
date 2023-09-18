# basic demonstration of a unit test

class MyClass:
    
    def __init__(self, a: float, b: float):
        self.a = a
        self.b = b
        
    def sum_values(self) -> float:
        return self.a + self.b
    
    
def test_unit_test():
    a = 1
    b = 2
    mc = MyClass(a, b)
    
    assert mc.sum_values() == a+b
    


# dummies: very specific cases where object is not used / type is not tested

from unittest.mock import MagicMock
import unittest

class SomeObject:
    def __init__(self, values: list=None):
        self._values = values
        # do stuff
    def call_something(a: list) -> list:
        return a + [1]
    
    def merge_sort(self, myList):
        if len(myList) > 1:
            mid = len(myList) // 2
            left = myList[:mid]
            right = myList[mid:]

            # Recursive call on each half
            self.merge_sort(left)
            self.merge_sort(right)

            # Two iterators for traversing the two halves
            i = 0
            j = 0
            
            # Iterator for the main list
            k = 0
            
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    # The value from the left half has been used
                    myList[k] = left[i]
                    # Move the iterator forward
                    i += 1
                else:
                    myList[k] = right[j]
                    j += 1
                # Move to the next slot
                k += 1

            # For all the remaining values
            while i < len(left):
                myList[k] = left[i]
                i += 1
                k += 1

            while j < len(right):
                myList[k]=right[j]
                j += 1
                k += 1
        return myList 
                
def function( ob: SomeObject):
    return {'entry1': ob}
    
 

def function2(an_object: SomeObject) -> list:
    res = an_object.call_something([1,2,3])
    return res

def function2_2(an_object: SomeObject):
    try:
        function2(an_object)
    except TypeError:
        raise NameError("this should be caught")


def function3(ob: SomeObject, list_to_sort: list) :
    # handle list through reference
    ob.merge_sort(list_to_sort)


# stubs in testing



class FakeSomeObject:
    # could also be creted through inheritance
    sorted_list = []
    def __init__(self, values=None):
        self._values = values
    def merge_sort(self, input_list):
        input_list.clear()
        input_list.extend(FakeSomeObject.sorted_list)

class TestTuto(unittest.TestCase):
    def test_with_dummy(self):
        dummy = MagicMock(spec=SomeObject)
        res = function(dummy)
        assert {'entry1': dummy} == res


    def test_with_stub(self):
        stub = MagicMock(spec=SomeObject)
        # Stub will return programmed value [1,2,3]
        stub.call_something = MagicMock(return_value = [1,2,3, 1])
        
        res = function2(stub)
        self.assertEqual(res, [1,2,3,1])
        
        # stubs can also be used to test if an exception is raised
        stub.call_something.side_effect=TypeError("This error is"
                                        "triggered for the sake of testing")
        
        # here we are testing exception is raised and handled accordingly by the try/catch statement
        with self.assertRaises(NameError):
            function2_2(stub)
        
        
    def test_with_spy(self):
        # we want to see if function is called with the correct 
        spy = MagicMock(spec=SomeObject)
        function2(spy)
        
        # we check here stub has been called with array [1, 2, 3]
        spy.call_something.assert_called_once_with([1,2,3])
    
    def test_with_fake(self):
        
        FakeSomeObject.sorted_list = [1,2,3]  # here we pass the result of the sorting operation
        fake = FakeSomeObject()
        
        test_list = [2,1,3]

        function3(fake, test_list)
        
        
        self.assertEqual(test_list, [1, 2, 3])
        
    
    def test_with_mock(self):
        # by oppositon to stubs, mocks come with one extra step: set_expectation
        test_list = [2,1,3]
        
        mock = MagicMock(spec=SomeObject)
        def mock_merge_sort(list_to_be_sorted):
            if not (list_to_be_sorted, list):
                raise TypeError 
            list_to_be_sorted.clear()
            list_to_be_sorted.extend([1,2,3])
        mock.merge_sort.side_effect = mock_merge_sort

        function3(mock, test_list)

        # checks
        self.assertEqual(test_list, [1, 2, 3])

        
        
if __name__ == '__main__':  # pragma: no cover
    unittest.main()
