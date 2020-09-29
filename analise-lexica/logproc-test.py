import unittest
from logproc import LogProcLexer

class TestLogProc(unittest.TestCase):
    def setUp(self):
        self.lp_lexer = LogProcLexer()
        fh = open("logproc.out", 'r')
        self.lp_out = fh.read()
        fh.close()

    def test_lexer(self):
        self.assertEqual(str(self.lp_lexer.collect_messages()), self.lp_out.rstrip())
        
if __name__ == '__main__':
    unittest.main()
