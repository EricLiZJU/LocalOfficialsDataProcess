import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# 检查某一年份是不是在begin_time和end_time之间
def year_check(year, begin_date, end_date):
    begin_year = begin_date.year
    end_year = end_date.year
    if begin_year > end_year:
        return False
    if (begin_year < year) & (year < end_year):
        return True
    else:
        return False

# 检查两个时间段是否有重合
def overlap_check(begin_date_tocheck, end_date_tocheck, begin_date, end_date):
    if end_date_tocheck < begin_date:
        return False
    elif begin_date_tocheck > end_date:
        return False
    else:
        return True

# 检索包含给定年份的所有工作经历
def get_time_related_experiences(year, leader_infos):
    filtered_df = []
    for leader_info in leader_infos:
        experience_list = leader_info['experience_list']
        for experience in experience_list:
            if year_check(year, experience['begin_time'], experience['end_time']):
                filted_experience = dict(person_id=leader_info['person_id'],
                                         prov_leader=leader_info['prov_leader'],
                                         experience=experience)
                filtered_df.append(filted_experience)

    return filtered_df



df = pd.read_excel('/Users/lihongyang/Desktop/testdata.xlsx')
PersonID_List = df['PersonID'].unique()

leader_infos = []

for person_id in PersonID_List:
    experience_list = []
    filtered_df = df[df['PersonID']==person_id]
    prov_leader = filtered_df['prov_leader'].iloc[0]
    for row in filtered_df.itertuples():
        begin_time = row.beginTime
        end_time = row.endTime
        location1 = str(row.localKey1)
        location2 = str(row.localKey2)
        experience = dict(begin_time=begin_time, end_time=end_time, location1=location1, location2=location2)
        experience_list.append(experience)

    leader_info = dict(person_id=person_id, prov_leader=prov_leader, experience_list=experience_list)
    if leader_info not in leader_infos:
        leader_infos.append(leader_info)

data = get_time_related_experiences(1950, leader_infos)


names = []
for i in data:
    names.append(i['prov_leader'])


G = nx.DiGraph()
G.add_nodes_from(names)

plt.figure(figsize = (12,10))
nx.draw(G, with_labels=True)
plt.show()

##







