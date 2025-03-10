import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import openpyxl
from openpyxl import Workbook
import ollama
import re
import logging
import time
import os
import json
import torch
import signal
import threading
import func_timeout
from func_timeout import func_set_timeout

@func_set_timeout(5)
def test_time_out(num):
    for i in range(10):
        print(i)
        time.sleep(1)

if __name__ == '__main__':
    try:
        test_time_out(1)
    except func_timeout.exceptions.FunctionTimedOut:
        print("Function Timed Out")
