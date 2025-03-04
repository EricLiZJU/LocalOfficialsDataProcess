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

with open('OfficialRank.json', 'r', encoding='utf-8') as file:
    offcial_rank = json.load(file)

