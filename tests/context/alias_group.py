# -*- coding: utf-8 -*-
import unittest
from config.context import Value
from config.context import AliasGroup

class AliasGroupTestCase(unittest.TestCase):

    def setUp(self):
        self.int  = 5
        self.str  = "string"
        self.float= 5.1
        self.nestedInt= 0
        
        self.group= AliasGroup(contexts= [
            ("integer", Value(self, "int", int)),
            ("string", Value(self, "str", str)),
            ("floater", Value(self, "float", float)),
            ("section", AliasGroup(contexts= [
                ("integer",  Value(self, "nestedInt", int))
            ]))
        ])
        
        self.group.addAliases(aliases= {
            "zahl": "integer",
            "wort" : "string" 
        })
        
        self.group.addAliases(aliases={"fließkomma": "floater"})

    def test_construction(self):
        self.assertEqual(self.group.count, 0)
        
        count=0
        for name, ctx in self.group:
            count+= 1
            self.assertEqual(ctx.count, 0)

        self.assertEqual(count, 4)    
    
    
    def test_getContext(self):
        ctx=self.group.getContext("integer")        
        inputString= "123"

        ctx.enter()
        ctx.addContent(inputString)
        ctx.leave()
        
        self.assertEqual(self.int, int(inputString))

        ctx=self.group.getContext("string")        
        inputString= "a long string"
        ctx.enter()
        ctx.addContent(inputString)
        ctx.leave()
        self.assertEqual(self.str, inputString)

        ctx=self.group.getContext("floater")        
        inputString= "1.234"
        ctx.enter()        
        ctx.addContent(inputString)
        ctx.leave()
        self.assertEqual(self.float, float(inputString))
        
        ctx=self.group.getContext("section")
        ctx.enter()
        ctx2= ctx.getContext("integer")        
        ctx2.enter()
        inputString= "1234"
        ctx2.addContent(inputString)
        ctx2.leave()
        ctx.leave()        
        self.assertEqual(self.nestedInt, int(inputString))

        self.assertRaises(KeyError, self.group.getContext, "xxx")
        
        count= 0
        for name, ctx in self.group:
            count+= 1            
            self.assertEqual(ctx.count, 1)
            
        self.assertEqual(count, 4)

        
    def test_aliases(self):
        ctx=self.group.getContext("zahl")
        inputString= "333"

        ctx.enter()
        ctx.addContent(inputString)
        ctx.leave()
        
        self.assertEqual(self.int, int(inputString))
        
        ctx=self.group.getContext("wort")  
        inputString= "a long string"
        ctx.enter()
        ctx.addContent(inputString)
        ctx.leave()
        self.assertEqual(self.str, inputString)
        
        ctx=self.group.getContext("fließkomma")
        inputString= "1.234"
        ctx.enter()
        ctx.addContent(inputString)
        ctx.leave()
        self.assertEqual(self.float, float(inputString))
        
        self.group.clearAliases()
        self.assertRaises(KeyError, self.group.getContext, "zahl")
        
        with self.assertRaises(KeyError):
            self.group.addAliases({"wort": "wort"})
        

    def test_itemAccess(self):
        ctx1= self.group.getContext("wort")
        ctx2= self.group["wort"]
        ctx3= self.group["string"]
        self.assertTrue(ctx1 is ctx2)
        self.assertTrue(ctx1 is ctx3)
        with self.assertRaises(TypeError):
            ctx4= self.group["kein wort"]


    def test_contextInterface(self):
        self.group.enter()
        self.assertRaises(NotImplementedError,
                          self.group.addContent,
                          "ctx")
        self.group.leave()
        
        self.assertRaises(IOError, self.group.enter)
        
        self.group.reset()        
        self.group.enter()
        self.group.addContent(" \n \r\n \t")
        self.group.leave()
        self.assertEqual(self.group.count, 1)

        self.assertEqual(self.group.help, "")
        

def suite():
    """Get Test suite object
    """
    return unittest.TestLoader().loadTestsFromTestCase(AliasGroupTestCase)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run( suite() )