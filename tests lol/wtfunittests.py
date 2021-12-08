import unittest
import inputtotape as iot


class InputTapeTests(unittest.TestCase):
    def test_master_iot(self):
        self.assertEqual(str(iot.master_tape("0 1", "po", "q w", " ")),
                         "[0][1]\033[4m[po]\033[0m[q][w]")
        self.assertEqual(str(iot.master_tape("0 1", "po", "", " ")),
                         "[0][1]\033[4m[po]\033[0m")
        self.assertEqual(str(iot.master_tape("", "po", "q w", " ")),
                         "\033[4m[po]\033[0m[q][w]")
        self.assertEqual(str(iot.master_tape("", "po", "", " ")),
                         "\033[4m[po]\033[0m")
        self.assertEqual(str(iot.master_tape("", "", "", " ")),
                         "\033[4m[]\033[0m")



if __name__ == '__main__':
    unittest.main()
