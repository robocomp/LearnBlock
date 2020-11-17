import unittest

from learnbot_dsl.learnbotCode.Parser import Parser, PythonGenerator, Typechecker, parserLearntBotCodeFromCode

TEST_TEXT = \
    """

main:
    x = 2
end

"""


class ParserTesting(unittest.TestCase):
    def setUp(self):
        self.tree = Parser.parse_str(TEST_TEXT)

    def test_parse_tree(self):
        self.assertEqual(self.tree.defs, [])
        self.assertEqual(self.tree.defs, [])
        self.assertEqual(self.tree.imports, [])
        self.assertEqual(self.tree.inits, [])
        self.assertEqual(self.tree.end, (5, 4, 21))
        self.assertEqual(self.tree.start, (3, 1, 2))
        self.assertEqual(self.tree.used_vars, {'x'})

    def test_python_generator(self):
        python_text = PythonGenerator.generate(self.tree)
        self.assertEqual(python_text, "x = 2")

    def test_type_checker(self):
        mismatches = Typechecker.check(self.tree)
        self.assertEqual(mismatches, [])

    def test_parser_learnbot(self):
        result = parserLearntBotCodeFromCode(TEST_TEXT, "robots")
        self.assertEqual(result, ('\n'
                                  '#EXECUTION: python code.py\n'
                                  'from __future__ import print_function, absolute_import\n'
                                  'import sys, os, time, traceback\n'
                                  'sys.path.insert(0, os.path.join(os.getenv(\'HOME\'), ".learnblock", "clients"))\n'
                                  'from robots import Robot\n'
                                  'import signal\n'
                                  'import sys\n'
                                  '\n'
                                  'usedFunctions = []\n'
                                  '\n'
                                  'try:\n'
                                  '\trobot = Robot(availableFunctions = usedFunctions)\n'
                                  'except Exception as e:\n'
                                  '\tprint("Problems creating a robot instance")\n'
                                  '\ttraceback.print_exc()\n'
                                  '\traise(e)\n'
                                  '\n'
                                  '\n'
                                  'time_global_start = time.time()\n'
                                  'def elapsedTime(umbral):\n'
                                  '\tglobal time_global_start\n'
                                  '\ttime_global = time.time()-time_global_start\n'
                                  '\treturn time_global > umbral\n'
                                  '\n'
                                  '\n'
                                  'def signal_handler(sig, frame):\n'
                                  '\trobot.stop()\n'
                                  '\tsys.exit(0)\n'
                                  '\n'
                                  'signal.signal(signal.SIGTERM, signal_handler)\n'
                                  'signal.signal(signal.SIGINT, signal_handler)\n'
                                  '\n'
                                  'x = 2\n'
                                  'robot.stop()\n'
                                  'sys.exit(0)\n'
                                  '\n'
                                  '', []))


if __name__ == '__main__':
    unittest.main()
