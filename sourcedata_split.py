import pandas as pd

df = pd.read_stata('/Users/lihongyang/Desktop/LocalOfficalsDataProcess/SourceData.dta', )
total_rows = df.shape[0]
chunk_size = 1000
num_chunks = (total_rows // chunk_size) + (1 if total_rows % chunk_size != 0 else 0)

for i in range(num_chunks):
    # 获取每个子 DataFrame
    start_row = i * chunk_size
    end_row = min((i + 1) * chunk_size, total_rows)
    chunk_df = df.iloc[start_row:end_row]

    # 保存为新的 .dta 文件
    chunk_df.to_csv(f'/Users/lihongyang/Desktop/LocalOfficalsDataProcess/data/{i+1}.csv', index=False)

    print(f'保存了第 {i + 1} 个文件，包含 {start_row} 到 {end_row} 行数据。')