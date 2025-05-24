import unittest
import sys
import os

# Add the current directory to the path so we can import app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import app

class TestApp(unittest.TestCase):
    
    def test_greet_default(self):
        """Test default greeting"""
        result = app.greet()
        self.assertEqual(result, "Hello World from Jenkins Pipeline!")
    
    def test_greet_custom_name(self):
        """Test greeting with custom name"""
        result = app.greet("Jenkins")
        self.assertEqual(result, "Hello Jenkins from Jenkins Pipeline!")
    
    def test_get_system_info(self):
        """Test system info function"""
        info = app.get_system_info()
        
        # Check that required keys exist
        self.assertIn("python_version", info)
        self.assertIn("timestamp", info)
        self.assertIn("platform", info)
        
        # Check that values are not empty
        self.assertTrue(info["python_version"])
        self.assertTrue(info["timestamp"])
        self.assertTrue(info["platform"])

if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)
