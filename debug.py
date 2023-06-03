
import sys
import os
print(sys.path)

import pytest


if __name__ == "__main__":
     os.system('pytest -s test_demo.py --alluredir ./report/allure_raw')
     # import os

     # _out = os.popen("allure generate allure-results -o allure_reports/ --clean").read()
     # print(_out)
