from turtle import clear
import pandas as pd
import os


class Cleaner:
    def __init__(self, dataset_path, output_path):
        self.dataset = dataset_path
        self.outputpath = output_path

    def clean_json(task_name):
        total = pd.DataFrame()

        for root, _, files in os.walk(dataset + task_name):
            # 遍历文件
            for file in files:
                df = pd.read_json(os.path.join(root, file),
                                encoding='utf-8', orient='records')
                # 增加uid
                cols = df.columns
                df["uid"] = file[-8:-5]
                df = df[["uid"] + list(cols)]

                # 删除json中本身含有null标志的记录
                if 'null' in df.columns:
                    df = df[df['null'].isna()]
                    df = df.dropna(axis=1, how='all')

                # 删除数据中带有回车符的记录，避免csv无法对齐
                df = df.applymap(lambda x: x.strip() if type(x) == str else x)

                # 添加到总表
                total = pd.concat([total, df], axis=0, ignore_index=True)

        # 检查输出目录是否存在
        try:
            os.path.isdir(output_path)
        except:
            os.mkdir(output_path)

        total.to_csv(output_path + task_name + ".csv", index=False)


if __name__ == "__main__":
    dataset = "D:\\OneDrive - pku.edu.cn\\datasets\\studentlife\\EMA\\response\\"
    output_path = ".\\EMA\\"

    cln = Cleaner(dataset, output_path)

    tasks = list(set(os.listdir(dataset)) - set(["PAM", "QR_Code"]))
    print(tasks)
    for task in tasks:
        Cleaner.clean_json(task)
