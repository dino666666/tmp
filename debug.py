
import sys
import os
sys.path.append("/var/lib/jenkins/.local/lib/python3.10/site-packages")
print(sys.path)

import pytest


if __name__ == "__main__":
     pytest.main(['-s', '-v', 'test_demo.py', '-q', '--alluredir=report/allure_raw'])
     # os.system('pytest -s test_demo.py --alluredir ./report/allure_raw')
     # import os

     # _out = os.popen("allure generate allure-results -o allure_reports/ --clean").read()
     # print(_out)
