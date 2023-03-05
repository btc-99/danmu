import pandas as pd
import requests as re
import json
import csv
from time import sleep

start_time, end_time = 0, 3
danmus = []
dm_len = 500

# noinspection SpellCheckingInspection
vid = "85BAvqK0dVRMG4Lm"
while True:
    dms = json.loads(
        re.get(
            f"https://v.douyu.com/wgapi/vod/center/getBarrageList?vid={vid}&start_time={start_time * 10000}&end_time={end_time * 10000}"
        ).text
    )["data"]["list"]


    # 确定所有弹幕获取完毕后break
    if start_time > 6 * 121 and dms.__len__() < dm_len:
        break

    # 如果没有完成获取，则end_time -= 1后重新获取
    if dms.__len__() >= dm_len:
        print(f"{start_time}：{end_time}\tfail")
        end_time -= 1
        continue

    # 完整获取后，写入弹幕，到下一区间继续获取
    danmus.extend(dms)
    print(f"{start_time}：{end_time}\t本轮获取：{dms.__len__()}\t总获取：{danmus.__len__()}")
    step = end_time - start_time
    start_time += step
    end_time += step

    # 如果这一次获取到的弹幕量比较少，考虑向后多移动一分钟
    if dms.__len__() < 250:
        end_time += 1

    sleep(0.2)

with open(f"output.txt", "w", newline='', encoding='UTF-8') as fp:
    csv.writer(fp).writerow(danmus[0].keys())
    csv.writer(fp).writerows(list(map(lambda x: x.values(), danmus)))
