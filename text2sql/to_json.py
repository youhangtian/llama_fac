import csv 
import json 
import random

from table_info import TABLE_INFO

prompt = '''
你是一个数据库分析专家，可以根据提供的数据库表结构，使用正确的sql代码来回答用户问题。
数据库表结构如下：
{TABLE_INFO}
用户问题如下:
{question}
sql代码:
'''

def get_d(row):
    d = {}
    d['input'] = ''
    d['history'] = []

    question = row[4]
    sql = row[5]

    d['instruction'] = prompt.format(TABLE_INFO=TABLE_INFO, question=question)
    d['output'] = sql
    return d 

output = []

arr = []
with open('newq.csv') as f:
    csv_reader = csv.reader(f)
    for row in csv_reader:
        d = get_d(row)
        arr.append(d)
arr = arr * 3
output.extend(arr)
print('output len:', len(output))

arr = []
with open('newqs.csv') as f:
    csv_reader = csv.reader(f)
    for row in csv_reader:
        d = get_d(row)
        arr.append(d)
output.extend(arr)
print('output len', len(output))

random.shuffle(output)
print(random.choices(output))

with open('data_all.json', 'w') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print('done')
