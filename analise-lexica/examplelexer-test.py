import unittest
from examplelexer import Ex351Lexer

class TestEx351(unittest.TestCase):
    ex_lexer = None

    def setUp(self):
        self.ex_lexer = Ex351Lexer()

    def test_lexerA(self):
        self.ex_lexer.setData("while if x then 3 <= 4 else 20 >= 1")
        oh = open("ex351a.out", "r")
        out = oh.read()
        oh.close()
        self.assertEqual(str(self.ex_lexer.tokenize()), out.rstrip())

    def test_lexerB(self):
        self.ex_lexer.setData("while if x then 3 < 4 else 20 == 1")
        oh = open("ex351b.out", "r")
        out = oh.read()
        oh.close()
        self.assertEqual(str(self.ex_lexer.tokenize()), out.rstrip())

    def test_lexerC(self):
        self.ex_lexer.setData("while if _x then 3 > 4 else 20 == 1")
        oh = open("ex351c.out", "r")
        out = oh.read()
        oh.close()
        self.assertEqual(str(self.ex_lexer.tokenize()), out.rstrip())

    def test_lexerD(self):
        self.ex_lexer.setData("while if _x then 3 < 4 else 20 == \"ola\"")
        oh = open("ex351d.out", "r")
        out = oh.read()
        oh.close()
        self.assertEqual(str(self.ex_lexer.tokenize()), out.rstrip())
        
if __name__ == '__main__':
    unittest.main()
