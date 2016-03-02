# -*- coding: utf-8 -*-
import unittest
from config.context import List


class ListTestCase(unittest.TestCase):

    def setUp(self):
        self.list1=[]
        self.list2=[]

        self.list1Value= List( self, "list1", int )
        self.list2Value= List( self, "list2", float, maxCount=3)
        
        
    def test_construction(self):
        self.assertEqual(self.list1Value.count, 0)
        self.assertEqual(self.list2Value.count, 0)
        
    
    def test_parse(self):
        inputString="123, 456, 7"
        self.list1Value.enter()        
        self.list1Value.addContent(inputString)
        self.list1Value.leave()
        
        self.list2Value.enter()
        self.list2Value.addContent(inputString)
        self.list2Value.leave()
        
        self.assertEqual(self.list1, [123, 456, 7])
        self.assertEqual(self.list2, [123., 456., 7.])
        self.assertEqual(self.list1Value.count, 1)
        self.assertEqual(self.list2Value.count, 1)

        self.assertRaises(IOError, self.list1Value.enter)
        self.list2Value.enter()        
        self.list2Value.addContent("2.0, 3.")
        self.list2Value.leave()
        self.assertEqual(self.list2, [2., 3.])
        
        self.list2Value.enter()
        self.list2Value.addContent("4.2")
        self.list2Value.leave()
        
        self.assertEqual(self.list2, [4.2])
        self.assertRaises(IOError, self.list2Value.enter)
        
        
    def test_contextInterface(self):
        self.assertRaises(NotImplementedError, self.list1Value.getContext, "ctx")
        

def suite():
    """Get Test suite object
    """
    return unittest.TestLoader().loadTestsFromTestCase(ListTestCase)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run( suite() )