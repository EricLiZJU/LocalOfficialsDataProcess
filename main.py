import pandas as pd
import re
import jieba

df = pd.read_csv('/Users/lihongyang/Desktop/LocalOfficalsDataProcess/data/1.csv')
edubackground_data = df['edu_firstdetail']

print(edubackground_data)

time_pattern = r'(\d{4}[\.年]?\d{2}[\.月]?)——(\d{4}[\.年]?\d{2}[\.月]?)|(\d{4}[年]?)至(\d{4}[年]?)'
school_keywords = ['大学', '学院', '学校']
school_pattern = r'([一-龥]+(?:大学|学院|学校))'
major_pattern = r'([一-龥]+(?:专业|系|班))'
pattern = r'([一-龥]+(?:大学|学院|学校))([一-龥]+(?:专业|系|班))'

time_matches = []
school_matches = []
major_matches = []

jieba.load_userdict('school_name.txt')

for text in edubackground_data:
    if type(text) != str:
        text = str(text)

    matches = re.findall(pattern, text)
    school_names = [match[0] for match in matches]
    major_names = [match[1] for match in matches]

    if len(matches) > 0:
        print(matches)




