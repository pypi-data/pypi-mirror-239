import unittest
import os
from maplewood import chainsaw as cs

class TestChainsaw(unittest.TestCase):
    
    def setUp(self):
        self.chainsaw = cs.Chainsaw(fdir='tests', fname='test_log.txt', module="unittest")
        if os.path.isfile('./tests/test_log.txt'):
            os.remove('./tests/test_log.txt')
        
    def test_open(self):
        self.chainsaw.open()
        self.assertTrue(self.chainsaw.is_open())
        self.assertTrue(os.path.isfile('./tests/test_log.txt'))
        self.chainsaw.close()

    def test_write(self):
        self.chainsaw.open()
        self.chainsaw.write(success=True, message='Test message')
        self.chainsaw.close()
        with open('./tests/test_log.txt', 'r') as f:
            log_content = f.read()
        self.assertIn('Test message', log_content)
        self.assertIn('PASS', log_content)

    def test_write_not_open(self):
        with self.assertRaises(RuntimeError):
            self.chainsaw.write(success=True, message='Test message')
            
    def test_write_all_params(self):
        self.chainsaw.open()
        self.chainsaw.write(success=True, message='Test message', module="unittest", success_str="TEST")
        self.chainsaw.close()
        with open('./tests/test_log.txt', 'r') as f:
            log_content = f.read()
        self.assertIn('Test message', log_content)
        self.assertIn('TEST', log_content)
        self.assertIn('unittest', log_content)
        
    def test_default_logs(self):
        
        self.chainsaw.update(success="Pass message", failure='Fail message')
        
        self.chainsaw.open()
        self.chainsaw.log()
        self.chainsaw.log(True)
        self.chainsaw.close()
        
        with open('./tests/test_log.txt', 'r') as f:
            log_content = f.read()
        self.assertIn('Pass message', log_content)
        self.assertIn('Fail message', log_content)

    def test_close(self):
        self.chainsaw.open()
        self.chainsaw.close()
        self.assertFalse(self.chainsaw.is_open())

    def test_close_not_open(self):
        with self.assertRaises(RuntimeError):
            self.chainsaw.close()

    def test_log(self):
        self.chainsaw.open()
        self.chainsaw.log(True)
        self.chainsaw.close()
        with open('./tests/test_log.txt', 'r') as f:
            log_content = f.read()
        self.assertIn('PASS', log_content)

if __name__ == '__main__':
    unittest.main()