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



logging.basicConfig(filename='example.log',  # 日志文件
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

with open('OfficialRank.json', 'r', encoding='utf-8') as file:
    offcial_rank = json.load(file)


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


# 从excel表中提取人员信息
def chart2info(df):
    PersonID_List = df['PersonID'].unique()

    leader_infos = []

    for person_id in PersonID_List:
        experience_list = []
        filtered_df = df[df['PersonID'] == person_id]
        prov_leader = filtered_df['prov_leader'].iloc[0]
        for row in filtered_df.itertuples():
            begin_time = row.beginTime  # 工作经历开始时间
            end_time = row.endTime  # 工作经历结束时间
            location1 = str(row.localKey1)  # 工作地点
            location2 = str(row.localKey2)
            location3 = str(row.localKey3)
            if location1 == 'nan':
                location1 = ''
            if location2 == 'nan':
                location2 = ''
            if location3 == 'nan':
                location3 = ''
            location = location1 + location2 + location3
            type = row.type  # 工作单位性质
            rank = row.rank  # 行政级别
            if rank in offcial_rank.keys():
                rank = offcial_rank[rank]
            else:
                rank = 0
            jobKey1 = str(row.jobKey1)
            jobKey2 = str(row.jobKey2)
            jobKey3 = str(row.jobKey3)
            if jobKey1 == 'nan':
                jobKey1 = '地点缺失'
            if jobKey2 == 'nan':
                jobKey2 = ''
            if jobKey3 == 'nan':
                jobKey3 = ''
            position = str(row.position)
            job_name = location + jobKey1 + jobKey2 + jobKey3 + position
            experience = dict(begin_time=begin_time,
                              end_time=end_time,
                              location=str(location1) + str(location2) + str(location3),
                              type=type,
                              rank=rank,
                              job_name=job_name)
            experience_list.append(experience)

        leader_info = dict(person_id=person_id, prov_leader=prov_leader, experience_list=experience_list)
        if leader_info not in leader_infos:
            leader_infos.append(leader_info)

    return leader_infos


# deepseek判断上下级关系
@func_set_timeout(5)
def deepseek_judge(tocheck_experience, related_experience):
    res = ollama.chat(model="deepseek-r1:7b",
                      stream=False,
                      messages=[{"role": "user",
                                 "content":
                                     f"只回答“是”或“否”，判断后面的职务是否为前面职务的上级：{tocheck_experience} 和 {related_experience}"}],
                      options={"temperature": 0})
    response_content = re.sub(r'<think>.*?</think>', '', str(res.message.content), flags=re.DOTALL)

    return response_content


# 对某特定id检索上下级关系
def superior_judge(personal_id_tocheck, data):
    tocheck_infos = []
    superior_relations = []
    name = id2name(personal_id_tocheck, data)

    for i in data:
        if i['person_id'] == personal_id_tocheck:
            tocheck_infos.append(i)

    person_count = 0

    for tocheck_info in tocheck_infos:
        person_count += 1
        print(
            f"待查询人第{person_count}/{len(tocheck_infos)}个职务，待查询人姓名: {tocheck_info['prov_leader']}，待查询人ID: {tocheck_info['person_id']}")
        print(f"待查询人职务: {tocheck_info['experience']}")
        logging.info(tocheck_info)

        related_infos = []
        superior_infos = []

        tocheck_experience = tocheck_info['experience']['job_name']
        for info in tocheck_infos:
            for i in data:
                if (((((info['experience']['location'] == i['experience']['location']) or
                       (i['experience']['location'] in info['experience']['location'])))
                     and (i['experience']['type'] == info['experience']['type']))
                        and ((i['experience']['rank'] - info['experience']['rank'] >= 0) and
                             (i['experience']['rank'] - info['experience']['rank'] <= 3)
                             or (info['experience']['rank'] == 0)
                             or (i['experience']['rank'] == 0))):
                    related_infos.append(i)

        info_count = 0
        for info in related_infos:
            if info["person_id"] == personal_id_tocheck:
                continue
            start_time = time.time()
            related_experience = info['experience']['job_name']
            try:
                response_content = deepseek_judge(tocheck_experience, related_experience)
            except func_timeout.exceptions.FunctionTimedOut:
                print("判断超时，已自动跳过")
                continue
            info_count += 1
            end_time = time.time()

            execution_time = end_time - start_time
            print(f"已判断{info_count}/{len(related_infos)}，用时{execution_time}秒")
            logging.info(f"已判断{info_count}/{len(related_infos)}，用时{execution_time}秒")
            if "是" in response_content:
                superior_infos.append(info)

        superior_relation = dict(person_id=personal_id_tocheck,
                                 name=name,
                                 experience=tocheck_info['experience'],
                                 superiors=superior_infos)
        superior_relations.append(superior_relation)

    print(superior_relations)

    return superior_relations


def run(filepath, year):
    wb = Workbook()
    ws = wb.active
    ws.title = "AllData"
    resfilepath = f"results/{year}.xlsx"
    wb.save(resfilepath)
    df = pd.read_excel(filepath)
    leader_infos = chart2info(df)
    leader_ids = []
    for leader_info in leader_infos:
        leader_ids.append(leader_info["person_id"])
    leader_ids = set(leader_ids)
    total_num = len(leader_ids)
    count = 0
    ollama.create(model='JudgeModel', from_='deepseek-r1:7b',
                  system="You're a language model for determining the hierarchical relationships of Chinese officials.")

    if not os.path.exists(resfilepath):
        df_init = pd.DataFrame(columns=["person_id", "name", "experience", "superiors"])
        df_init.to_excel(resfilepath, sheet_name="AllData", index=False)

    for leader_id in leader_ids:
        if (count % 20) == 19:
            ollama.delete(model='JudgeModel')
            ollama.create(model='JudgeModel', from_='deepseek-r1:7b',
                          system="You're a language model for determining the hierarchical relationships of Chinese officials.")
            print("---提示：模型已刷新---")
        count += 1
        print(f"------------第{count}/{total_num}位查询人------------")
        data = get_time_related_experiences(year, leader_infos)

        superior_relations = superior_judge(leader_id, data)
        superior_relations_df = pd.DataFrame(superior_relations)
        existing_data = pd.read_excel(resfilepath, sheet_name='AllData')
        df_combined = pd.concat([existing_data, superior_relations_df], ignore_index=True)

        with pd.ExcelWriter(resfilepath, mode='w', engine='openpyxl') as writer:
            df_combined.to_excel(writer, sheet_name="AllData", index=False)
        print(f"第{count}/{total_num}位查询人数据已追加")
    print("所有数据已处理完成")


if __name__ == '__main__':
    filepath = 'testdata.xlsx'
    for year in range(2002, 2005):
        print(f'---------------------分析{year}年数据---------------------')
        run(filepath, year)
