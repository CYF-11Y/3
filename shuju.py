import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# ===================== 1. 设置固定随机种子（保证数据可复现） =====================
random.seed(12345)
np.random.seed(12345)

# ===================== 2. 定义基础配置（贴合你的需求） =====================
# 时间范围：2025-09-01 至 2026-02-28
start_date = datetime(2025, 9, 1)
end_date = datetime(2026, 2, 28)
date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

# 城市列表（覆盖你要求的城市）
cities = ["北京", "上海", "广州", "深圳", "杭州", "南京", "成都", "武汉"]

# 课程类别+对应课程名称+单价范围
course_config = {
    "K12文化课": {
        "courses": ["小学数学", "小学英语", "初中数学", "初中物理", "高中语文", "高中英语"],
        "price_range": (100, 500)  # 单价100-500元/节
    },
    "素质课": {
        "courses": ["少儿美术", "钢琴一对一", "篮球集训", "编程启蒙", "书法课"],
        "price_range": (200, 800)  # 单价200-800元/节
    },
    "职业技能课": {
        "courses": ["Python入门", "办公软件进阶", "短视频剪辑", "电商运营"],
        "price_range": (150, 600)  # 单价150-600元/节
    }
}

# 学员年级
grades = ["小学1年级", "小学2年级", "小学3年级", "小学4年级", "小学5年级", "小学6年级",
          "初中1年级", "初中2年级", "初中3年级", "高中1年级", "高中2年级", "高中3年级"]

# 模拟中文名（随机组合）
first_names = ["张", "李", "王", "刘", "陈", "杨", "赵", "黄", "周", "吴"]
last_names = ["伟", "芳", "娜", "敏", "静", "强", "磊", "洋", "杰", "婷"]


# ===================== 3. 生成模拟数据 =====================
def generate_random_data(n=1000):
    """生成n条模拟缴费数据"""
    data = []
    for i in range(n):
        # 学员ID（唯一）
        student_id = f"S{str(i + 1).zfill(4)}"

        # 学员姓名（随机组合）
        name = random.choice(first_names) + random.choice(last_names)

        # 城市
        city = random.choice(cities)

        # 课程类别+课程名称+单价
        course_type = random.choice(list(course_config.keys()))
        course_name = random.choice(course_config[course_type]["courses"])
        price = round(np.random.uniform(*course_config[course_type]["price_range"]), 2)

        # 报名节数（1-20节）
        class_count = random.randint(1, 20)

        # 缴费总额（自动计算）
        total_amount = round(class_count * price, 2)

        # 缴费日期（随机）
        pay_date = random.choice(date_range).strftime("%Y-%m-%d")

        # 学员年级
        grade = random.choice(grades)

        # 拼接单条数据
        data.append([
            student_id, name, city, course_type, course_name,
            class_count, price, total_amount, pay_date, grade
        ])
    return data


# 生成1000条模拟数据（可修改n调整数据量）
simulated_data = generate_random_data(n=1000)

# ===================== 4. 生成Excel表格（已移除错误的encoding参数） =====================
# 定义表头
headers = [
    "学员ID", "学员姓名", "城市", "课程类别", "课程名称",
    "报名节数", "单价（元/节）", "缴费总额（元）", "缴费日期", "学员年级"
]

# 转换为DataFrame
df = pd.DataFrame(simulated_data, columns=headers)

# 保存为Excel（移除了错误的encoding参数，其他不变）
output_file = "学员缴费销售数据.xlsx"
df.to_excel(output_file, index=False, engine="openpyxl")  # ✅ 关键修改：删除encoding="utf-8"

print(f"✅ 模拟数据生成完成！共{len(df)}条记录，已保存至：{output_file}")
print("\n📌 前5条数据预览：")
print(df.head())