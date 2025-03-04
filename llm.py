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

model = ollama.create(model='example', from_='deepseek-r1:7b', system="You are trump who are the president of America")

res = ollama.chat(model="example",
                      stream=False,
                      messages=[{"role": "user",
                                 "content":
                                    "介绍一下你是谁"}],
                      options={"temperature": 0})

print(res.message.content)