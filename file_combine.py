import pandas as pd
import glob

def merge_csv_to_dta(csv_folder_path, output_dta_path):
    # 获取所有 CSV 文件路径
    csv_files = glob.glob(f"{csv_folder_path}/*.csv")

    # 读取所有 CSV 文件并合并到一个 DataFrame
    df_list = [pd.read_csv(file) for file in csv_files]
    combined_df = pd.concat(df_list, ignore_index=True)

    # 将合并后的 DataFrame 保存为 .dta 文件
    combined_df.to_csv(output_dta_path)

    print(f"CSV 文件成功合并并保存为 {output_dta_path}")


# 使用示例
csv_folder_path = '/Users/lihongyang/Desktop/LocalOfficalsDataProcess/data'  # CSV 文件所在的文件夹路径
output_dta_path = '/Users/lihongyang/Desktop/LocalOfficalsDataProcess/output_file.csv'  # 输出的 .dta 文件路径

merge_csv_to_dta(csv_folder_path, output_dta_path)
