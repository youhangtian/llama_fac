import requests
import csv
import random
from tqdm import tqdm

api_url = 'http://localhost:11434/api/generate'
model_name = 'qwen2:72b'
data_name = 'newq.csv'
output_name = 'newqs.csv'
num = 20

loc = ['绍兴市', '越城区', '柯桥区', '上虞区', '新昌县', '诸暨市', '嵊州市']
t = [
    '昨天', 
    '最近七天/一周', 
    '最近三十天/一个月', 
    '上个月', 
    '今年', 
    '今年某月',
    '今年第几季度',
    '去年',
    '去年某月', 
    '去年第几季度',
    '具体到某年',
    '具体到某年某月'
]
ts = [
    "DATE_FORMAT(dt, '%Y-%m-%d') = DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 1 DAY), '%Y-%m-%d')",
    "dt <= DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 1 DAY), '%Y-%m-%d') and dt >= DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 7 DAY), '%Y-%m-%d')",
    "dt <= DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 1 DAY), '%Y-%m-%d') and dt >= DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 30 DAY), '%Y-%m-%d')",
    "DATE_FORMAT(dt, '%Y-%m') = DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 1 MONTH), '%Y-%m')",
    "YEAR(dt) = YEAR(CURDATE())",
    "YEAR(dt) = YEAR(CURDATE()) AND MONTH(dt) = x",
    "YEAR(dt) = YEAR(CURDATE()) AND QUARTER(dt) = x",
    "YEAR(dt) = YEAR(CURDATE()) - 1", 
    "YEAR(dt) = YEAR(CURDATE()) - 1 AND MONTH(dt) = x", 
    "YEAR(dt) = YEAR(CURDATE()) - 1 AND QUARTER(dt) = x",
    "DATE_FORMAT(dt, '%Y') = 'xxxx'",
    "DATE_FORMAT(dt, '%Y-%m') = 'xxxx-xx'"
]

PROMPT = '''
你是一个数据库sql分析专家，通过提供的数据库表结构生成一个针对该数据库的问题和回答该问题对应的sql语句。
数据库表结构如下：
{table_info}
回答示例：
```question {question}```
```sql {sql}```
请严格按照如下格式进行回答：
```question 你修改后的的问题```
```sql 你修改后的sql语句```
回答要求：
1，对回答示例里的question和sql稍作修改，只能修改里面涉及到的地点和时间，比如地点改为{rloc}， 时间改为{rt}，该时间对应的sql是{rts}
2，确保你修改后的sql能在数据库里执行，并且执行后提取的数据能准确地回答你修改后的question
3，如果问到的地点是‘绍兴市’，要统计表里的所有区县，你的sql里不能有‘district_name = xxx‘或者‘district_name like xx‘这样限定区县的字段
4，你只需要输出一个question和一个sql
请按要求进行回答：
'''

datas = []

with open(data_name) as f:
    csv_reader = csv.reader(f)
    for row in tqdm(csv_reader, desc='csv_reader'):
        for n in tqdm(range(num), desc='num'):
            r1 = random.randint(0, len(loc)-1)
            r2 = random.randint(0, len(t)-1)
            prompt = PROMPT.format(table_info=row[1], question=row[-2], sql=row[-1], rloc=loc[r1], rt=t[r2], rts=ts[r2])
            print('prompt:', prompt)

            request_data = {
                'model': model_name,
                'prompt': prompt,
                'stream': False,
                'options': {
                    'temprature': 0.8
                }
            }

            response = requests.post(api_url, json=request_data)
            output = response.json()['response']
            print('output:', output)

            q2 = output.split('```question')[-1].split('```')[0]
            while q2 and (q2[0] == '\n' or q2[0] == ' '):
                q2 = q2[1:]
            while q2 and (q2[-1] == '\n' or q2[-1] == ' '):
                q2 = q2[:-1]

            s2 = output.split('```sql')[-1].split('```')[0]
            while s2 and (s2[0] == '\n' or s2[0] == ' '):
                s2 = s2[1:]
            while s2 and (s2[-1] == '\n' or s2[-1] == ' '):
                s2 = s2[:-1]

            row2 = [r for r in row]
            row2[-2] = q2
            row2[-1] = s2
            datas.append(row2)
            print('------')

    print('------')

with open(output_name, 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerows(datas)

print('done')
