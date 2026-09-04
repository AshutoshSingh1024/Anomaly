import unittest
from terminal.parser import CommandParser

class ParserTests(unittest.TestCase):
    def test_parse(self):
        c=CommandParser().parse("move north")
        self.assertEqual(c.name,"move")
        self.assertEqual(c.arguments,["north"])
    def test_empty(self):
        self.assertEqual(CommandParser().parse(" ").name,"")

if __name__=="__main__": unittest.main()
