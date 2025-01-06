import pandas as pd
import re
from pathlib import Path

path = '/Users/lihongyang/Desktop/LocalOfficalsDataProcess/data/1.csv'

def get_csv_files_paths(directory):
    path = Path(directory)
    csv_files_paths = [str(file) for file in path.glob('*.csv')]

    return csv_files_paths

def eduinformation_extraction(path):
    df = pd.read_csv(path)
    edubackground_data = df['edu_firstdetail']

    time_pattern = r'(\d{4})(?=年|\D|\b)'
    pattern = r'([一-龥]+(?:大学|学院|学校))([一-龥]+(?:专业|系|班))'

    edu_years = []
    school_names = []
    major_names = []

    for text in edubackground_data:
        if type(text) != str:
            text = str(text)
        years = re.findall(time_pattern, text)
        if len(years) == 0:
            edu_years.append('missing')
        elif len(years) == 1:
            edu_years.append(years[0])
        elif len(years) >= 2:
            edu_years.append(years[0] + '——' + years[1])

        matches = re.findall(pattern, text)
        if len(matches) == 0:
            matches = [('missing', 'missing')]
            school_name = matches[0][0]
            major_name = matches[0][1]
        else:
            school_name = matches[0][0]
            major_name = matches[0][1]
            while True:
                cleaned_text = re.sub(r'^(年|月|日|毕业|在|到|入|于|从)', '', school_name)
                if len(cleaned_text) == len(school_name):
                    break
                school_name = cleaned_text

        school_names.append(school_name)
        major_names.append(major_name)

    return edu_years, school_names, major_names


def add_column_to_csv(file_path, new_column_name, new_column_values):
    df = pd.read_csv(file_path)
    df[new_column_name] = new_column_values
    df.to_csv(file_path, index=False)

if __name__ == '__main__':
    edu_years, school_names, major_names = eduinformation_extraction(path)
    print(edu_years)
    print(school_names)
    print(major_names)








