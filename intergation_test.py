import copy
from pprint import pprint
import unittest

import io
import contextlib


    
class ObjectSorter:
    def merge_sort(self, myList: list):
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

    
class ObjectFormatter:
    def prettry_print(self, list_to_print: list):
        pprint(list_to_print)
        

class ObjectHandler:
    def __init__(self, values: list):
        self.values = values
        self._of = ObjectFormatter()
        self._os = ObjectSorter()

    def merge_and_pprint(self):
        self._os.merge_sort(self.values)
        self._of.prettry_print(self.values)
        
        

class IntegrationTest(unittest.TestCase):
    
    def test_merge_and_pprint(self):
        # We do not use mocking / faking here
        values = [1, 3, 2, 1, 0]
        tested_values = copy.deepcopy(values)
        self.oh = ObjectHandler(values)
        
        
        f = io.StringIO()
        with contextlib.redirect_stdout(f):  # setting en
            # action: capturing stdout in order to test 
            # what is printed
            parser = self.oh.merge_and_pprint()

        # checks
        self.assertIn("[0, 1, 1, 2, 3]", f.getvalue())
        self.assertEqual(sorted(tested_values), values)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
