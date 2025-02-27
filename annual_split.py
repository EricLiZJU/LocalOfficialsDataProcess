import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import ollama
import re
from relation_extraction import *

def annual_split(df, year):
    leader_infos = chart2info(df)
    data = get_time_related_experiences(2004, leader_infos)

    return data

if __name__ == "__main__":
    df = pd.read_excel('/Users/lihongyang/Desktop/testdata.xlsx')

    years = range(1949, 2025)
    for year in years:

        data = annual_split(df, year)

        data_df = pd.DataFrame(data)
        data_df.to_excel(f'annual_data/{year}.xlsx')

