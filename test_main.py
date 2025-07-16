import unittest

def main():
    
# menjalankan semua file di dalam folder tests
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir='tests', pattern='test_*.py')

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
if __name__ == "__main__":
    main()