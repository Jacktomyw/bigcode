import json
import csv
import numpy
import os
import urllib.parse
import urllib.request
import string

f = open('test_data.json', encoding='utf-8')
res = f.read()
data = json.loads(res)
header = ["题目名", "提交次数", "相邻提交分数相同次数", "提交用户数", "未满分用户数", "分数为0用户数", "分数", "平均分", "分数中位数", "平均提交次数",
          "提交次数中位数", "平均相邻提交分数相同次数", "相邻提交分数相同次数中位数"]
cases = {}
# print(data)
count = 0
# cases = data['3544']['cases']  # 这里的3544为user_id，可遍历data字典key实现对user_id的遍历
for user in data.keys():
    count += 1
    for case in data[user]['cases']:
        case_id = case['case_id']

        upload_times = len(case['upload_records'])

        lastScore = 0
        sameTimes = 0
        for upload_record in case['upload_records']:
            score = upload_record['score']
            if score == lastScore:
                sameTimes += 1
            lastScore = score

        final_score = case['final_score']
        isZero = 0
        isNotFull = 1
        if final_score == 100:
            isNotFull = 0
        elif final_score == 0:
            isZero = 1

        if case_id not in cases.keys():
            case_zip = case['case_zip']
            case_name = case_zip[case_zip.index("target/") + 7:case_zip.index("_")]
            cases[case_id] = [case_name, [upload_times], [sameTimes], 1, isNotFull, isZero, [final_score]]
        else:
            cases[case_id][1].append(upload_times)
            cases[case_id][2].append(sameTimes)
            cases[case_id][3] += 1
            cases[case_id][4] += isNotFull
            cases[case_id][5] += isZero
            cases[case_id][6].append(final_score)

with open('result.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for case_id in cases.keys():
        cases[case_id].append(numpy.mean(cases[case_id][6]))
        cases[case_id].append(numpy.median(cases[case_id][6]))

        cases[case_id].append(numpy.mean(cases[case_id][1]))
        cases[case_id].append(numpy.median(cases[case_id][1]))

        cases[case_id].append(numpy.mean(cases[case_id][2]))
        cases[case_id].append(numpy.median(cases[case_id][2]))
        writer.writerow(cases[case_id])

# for item in data.items():
# cases = data[key]['cases']
# print(item)

# for case in cases:
# 下载题目
# print(case["case_id"], case["case_type"])
# filename = urllib.parse.unquote(os.path.basename(case["case_zip"]))
# print(filename)
# url = urllib.parse.quote(case["case_zip"], safe=string.printable)
# print(url)
# urllib.request.urlretrieve(url, filename)
# ====================================================
# for record in case["upload_records"]:
#     print(record["code_url"], record["score"])
#     filename = urllib.parse.unquote(os.path.basename(record["code_url"]))
#     print(filename)
#     urllib.request.urlretrieve(record["code_url"], filename)
