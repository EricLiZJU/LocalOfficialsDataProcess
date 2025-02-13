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

# 通过person_id检索姓名
def id2name(person_id, leader_infos):
    names = []
    filted_df = [item for item in leader_infos if item['person_id'] == person_id]
    for filt in filted_df:
        names.append(filt['prov_leader'])
    name = list(set(names))
    if len(name) == 0:
        return 'null'
    return name[0]

# 通过姓名检索person_id
def name2id(prov_leader, leader_infos):
    ids = []
    filted_df = [item for item in leader_infos if item['prov_leader'] == prov_leader]
    for filt in filted_df:
        ids.append(filt['person_id'])
    id = list(set(ids))
    if len(id) == 0:
        return 'null'
    elif len(id) > 1:
        print('more than one person id:', id)
        newid = input('please input the person id you want to check:')
        return newid
    else:
        return id





df = pd.read_excel('/Users/lihongyang/Desktop/testdata.xlsx')
PersonID_List = df['PersonID'].unique()

leader_infos = []

for person_id in PersonID_List:
    experience_list = []
    filtered_df = df[df['PersonID']==person_id]
    prov_leader = filtered_df['prov_leader'].iloc[0]
    for row in filtered_df.itertuples():
        begin_time = row.beginTime           # 工作经历开始时间
        end_time = row.endTime               # 工作经历结束时间
        location1 = str(row.localKey1)       # 工作地点
        location2 = str(row.localKey2)
        location3 = str(row.localKey3)
        if location2 == 'nan':
            location2 = ''
        if location3 == 'nan':
            location3 = ''
        location = location1 + location2 + location3
        type = row.type                      # 工作单位性质
        jobKey1 = str(row.jobKey1)
        jobKey2 = str(row.jobKey2)
        jobKey3 = str(row.jobKey3)
        if jobKey2 == 'nan':
            jobKey2 = ''
        if jobKey3 == 'nan':
            jobKey3 = ''
        position = str(row.position)
        job_name = location + jobKey1 + jobKey2 + jobKey3 + position
        experience = dict(begin_time=begin_time,
                          end_time=end_time,
                          location=str(location1)+str(location2)+str(location3),
                          job_name=job_name)
        experience_list.append(experience)

    leader_info = dict(person_id=person_id, prov_leader=prov_leader, experience_list=experience_list)
    if leader_info not in leader_infos:
        leader_infos.append(leader_info)

# print(leader_infos)


# 待查人员信息
personal_id_tocheck = 110000001983
personal_name_tocheck = '李强'
name = id2name(personal_id_tocheck, leader_infos)
id = name2id(personal_name_tocheck, leader_infos)
print(id)




#输出某一年份所有人的工作经历
data = get_time_related_experiences(1960, leader_infos)




names = []
for i in data:
    names.append(i['prov_leader'])

"""
G = nx.DiGraph()
G.add_nodes_from(names)

plt.rcParams['font.sans-serif'] = 'STHeiti'
plt.figure(figsize = (12,10))

nx.draw(G, with_labels=True)
plt.show()
"""








