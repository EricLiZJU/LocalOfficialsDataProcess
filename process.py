import pandas as pd
import re
from eduinformation_extraction import *

_PATH = '/Users/lihongyang/Desktop/LocalOfficalsDataProcess/data'
filesPath = get_csv_files_paths(_PATH)

for path in filesPath:
    print(path)
    edu_years, school_names, major_names = eduinformation_extraction(path)
    add_column_to_csv(path, 'edu_years', edu_years)
    add_column_to_csv(path, 'school_names', school_names)
    add_column_to_csv(path, 'major_names', major_names)