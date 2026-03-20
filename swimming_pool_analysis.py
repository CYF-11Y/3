import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

# 初始化Faker
fake = Faker('zh_CN')
random.seed(42)
np.random.seed(42)

# 配置参数
START_DATE = datetime(2025, 9, 1)
END_DATE = datetime(2026, 2, 28)
TOTAL_RECORDS = 5000

# 定义课程类别和课程名称映射
COURSE_CATEGORIES = {
    '少儿游泳': ['少儿蛙泳基础班', '少儿自由泳提高班', '少儿仰泳专项班', '少儿蝶泳精英班'],
    '成人游泳': ['成人蛙泳入门班', '成人自由泳速成班', '成人水中健身课', '成人减脂游泳班'],
    '私教课程': ['一对一私教课', '一对二私教课', '一对三私教课', '私教包月套餐'],
    '亲子游泳': ['亲子启蒙班', '亲子互动班', '亲子技能提升班', '亲子水上游戏课'],
    '考级课程': ['等级考试预备班', '一级考级冲刺班', '二级考级专项班', '三级考级集训班'],
    '集训课程': ['暑期集训营', '寒假集训营', '国庆集训班', '考前集中训练营']
}

# 定义城市
CITIES = ['北京', '上海', '广州', '深圳', '杭州', '南京', '成都', '武汉', '西安', '重庆']

# 定义缴费方式
PAYMENT_METHODS = ['微信支付', '支付宝', '银行卡', '现金', '分期']

# 定义课程状态
COURSE_STATUSES = ['已报名', '已开课', '已结课', '已退费']

# 生成随机日期
def random_date(start, end):
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)

# 生成模拟数据
data = []
for i in range(TOTAL_RECORDS):
    student_id = f'STU{10000 + i:05d}'
    student_name = fake.name()
    
    # 随机选择课程类别和名称
    course_category = random.choice(list(COURSE_CATEGORIES.keys()))
    course_name = random.choice(COURSE_CATEGORIES[course_category])
    
    # 根据课程类别确定是按期还是按节统计，并生成单价
    if course_category == '集训课程':
        quantity = random.randint(1, 3)  # 期数
        unit_price = random.randint(1500, 3500)  # 元/期
    else:
        quantity = random.randint(10, 50)  # 节数
        unit_price = random.randint(80, 250)  # 元/节
    
    # 计算正确的缴费总额
    correct_total = quantity * unit_price
    
    # 引入一些错误（10%的概率）
    if random.random() < 0.1:
        # 随机增加或减少一些金额作为错误值
        error_amount = random.randint(-200, 200)
        payment_total = max(0, correct_total + error_amount)
    else:
        payment_total = correct_total
    
    payment_date = random_date(START_DATE, END_DATE)
    city = random.choice(CITIES)
    payment_method = random.choice(PAYMENT_METHODS)
    
    # 课程状态分布：已结课最多，已退费最少
    status_weights = [0.15, 0.25, 0.50, 0.10]
    course_status = random.choices(COURSE_STATUSES, weights=status_weights)[0]
    
    data.append({
        '学员 ID': student_id,
        '学员姓名': student_name,
        '课程类别': course_category,
        '课程名称': course_name,
        '报名节数/期数': quantity,
        '单价（元/节/期）': unit_price,
        '缴费总额（元）': payment_total,
        '缴费日期': payment_date.strftime('%Y-%m-%d'),
        '学员所在城市': city,
        '缴费方式': payment_method,
        '课程状态': course_status,
        '正确缴费总额': correct_total  # 用于后续校验
    })

# 创建DataFrame
df = pd.DataFrame(data)

# 数据校验与修正
print("=" * 60)
print("数据校验与修正")
print("=" * 60)

# 找出需要修正的记录
correction_needed = df[df['缴费总额（元）'] != df['正确缴费总额']].copy()
correction_needed['修正前缴费总额'] = correction_needed['缴费总额（元）']
correction_needed['修正后缴费总额'] = correction_needed['正确缴费总额']

# 修正数据
df['缴费总额（元）'] = df['正确缴费总额']

# 删除辅助列
df = df.drop(columns=['正确缴费总额'])

# 输出修正记录
print(f"总记录数：{len(df)}")
print(f"需要修正的记录数：{len(correction_needed)}")
print("\n修正记录明细：")
correction_records = correction_needed[['学员 ID', '修正前缴费总额', '修正后缴费总额']]
print(correction_records.to_string(index=False))

# 输出修正后的数据表
print("\n" + "=" * 60)
print("修正后的数据表（前20条）")
print("=" * 60)
print(df.head(20).to_string(index=False))

# 保存修正后的数据表为CSV
df.to_csv('修正后学员缴费数据表.csv', index=False, encoding='utf_8_sig')
print(f"\n修正后的数据表已保存到：修正后学员缴费数据表.csv")

# 月度聚合汇总
print("\n" + "=" * 60)
print("月度聚合汇总")
print("=" * 60)

# 提取月份
df['缴费日期'] = pd.to_datetime(df['缴费日期'])
df['月份'] = df['缴费日期'].dt.strftime('%Y-%m')

# 「月度 - 课程类别 - 缴费总额」汇总表
monthly_by_category = df.groupby(['月份', '课程类别'])['缴费总额（元）'].sum().reset_index()
monthly_by_category = monthly_by_category.rename(columns={'缴费总额（元）': '缴费总额'})
monthly_by_category = monthly_by_category.sort_values(['月份', '课程类别'])

print("\n「月度 - 课程类别 - 缴费总额」汇总表：")
print(monthly_by_category.to_string(index=False))
monthly_by_category.to_csv('月度_课程类别_缴费总额汇总表.csv', index=False, encoding='utf_8_sig')

# 「月度 - 学员所在城市 - 缴费总额」汇总表
monthly_by_city = df.groupby(['月份', '学员所在城市'])['缴费总额（元）'].sum().reset_index()
monthly_by_city = monthly_by_city.rename(columns={'缴费总额（元）': '缴费总额', '学员所在城市': '城市'})
monthly_by_city = monthly_by_city.sort_values(['月份', '城市'])

print("\n「月度 - 学员所在城市 - 缴费总额」汇总表：")
print(monthly_by_city.to_string(index=False))
monthly_by_city.to_csv('月度_城市_缴费总额汇总表.csv', index=False, encoding='utf_8_sig')

# 统计分析
print("\n" + "=" * 60)
print("统计分析")
print("=" * 60)

total_payment = df['缴费总额（元）'].sum()
print(f"\n总缴费额：{total_payment:,.2f} 元")

# 1. 维度占比计算 - 城市
print("\n" + "-" * 60)
print("1. 各城市缴费额占比")
print("-" * 60)
city_payment = df.groupby('学员所在城市')['缴费总额（元）'].sum().reset_index()
city_payment = city_payment.rename(columns={'缴费总额（元）': '缴费总额', '学员所在城市': '城市'})
city_payment['占比（%）'] = (city_payment['缴费总额'] / total_payment * 100).round(2)
city_payment = city_payment.sort_values('缴费总额', ascending=False)
print(city_payment.to_string(index=False))

# 2. 维度占比计算 - 课程类别
print("\n" + "-" * 60)
print("2. 各课程类别缴费额占比")
print("-" * 60)
category_payment = df.groupby('课程类别')['缴费总额（元）'].sum().reset_index()
category_payment = category_payment.rename(columns={'缴费总额（元）': '缴费总额'})
category_payment['占比（%）'] = (category_payment['缴费总额'] / total_payment * 100).round(2)
category_payment = category_payment.sort_values('缴费总额', ascending=False)
print(category_payment.to_string(index=False))

# 3. 课程TOP3评选
print("\n" + "-" * 60)
print("3. 缴费总额最高的Top3热门课程")
print("-" * 60)
course_payment = df.groupby('课程名称')['缴费总额（元）'].sum().reset_index()
course_payment = course_payment.rename(columns={'缴费总额（元）': '缴费总额'})
course_payment['贡献度（%）'] = (course_payment['缴费总额'] / total_payment * 100).round(2)
course_payment = course_payment.sort_values('缴费总额', ascending=False).head(3)
print(course_payment.to_string(index=False))

# 4. 课程状态分析
print("\n" + "-" * 60)
print("4. 课程状态分析")
print("-" * 60)
status_payment = df.groupby('课程状态')['缴费总额（元）'].sum().reset_index()
status_payment = status_payment.rename(columns={'缴费总额（元）': '缴费总额'})
status_payment['占比（%）'] = (status_payment['缴费总额'] / total_payment * 100).round(2)
status_payment = status_payment.sort_values('缴费总额', ascending=False)
print(status_payment.to_string(index=False))

# 退费统计
refund_amount = df[df['课程状态'] == '已退费']['缴费总额（元）'].sum()
refund_ratio = (refund_amount / total_payment * 100).round(2)
print(f"\n已退费总额：{refund_amount:,.2f} 元")
print(f"退费占比：{refund_ratio}%")

# 退费高发课程
print("\n退费高发课程（按已退费金额排序）：")
refund_by_course = df[df['课程状态'] == '已退费'].groupby('课程名称')['缴费总额（元）'].sum().reset_index()
refund_by_course = refund_by_course.sort_values('缴费总额（元）', ascending=False).head(5)
print(refund_by_course.to_string(index=False))

# 5. 城市人均缴费分析
print("\n" + "-" * 60)
print("5. 城市人均缴费分析")
print("-" * 60)
# 按学员ID去重统计各城市学员数
city_students = df.drop_duplicates('学员 ID').groupby('学员所在城市')['学员 ID'].count().reset_index()
city_students = city_students.rename(columns={'学员所在城市': '城市', '学员 ID': '学员数'})

# 计算各城市总缴费额
city_total = df.groupby('学员所在城市')['缴费总额（元）'].sum().reset_index()
city_total = city_total.rename(columns={'缴费总额（元）': '总缴费额', '学员所在城市': '城市'})

# 合并计算人均缴费
city_analysis = pd.merge(city_students, city_total, on='城市')
city_analysis['人均缴费额（元）'] = (city_analysis['总缴费额'] / city_analysis['学员数']).round(2)
city_analysis = city_analysis.sort_values('人均缴费额（元）', ascending=False)
print(city_analysis.to_string(index=False))

# 保存所有统计结果
with open('统计分析结果.txt', 'w', encoding='utf-8') as f:
    f.write("=" * 60 + "\n")
    f.write("游泳馆学员缴费数据统计分析结果\n")
    f.write("=" * 60 + "\n")
    f.write(f"\n总缴费额：{total_payment:,.2f} 元\n")
    
    f.write("\n" + "-" * 60 + "\n")
    f.write("1. 各城市缴费额占比\n")
    f.write("-" * 60 + "\n")
    f.write(city_payment.to_string(index=False) + "\n")
    
    f.write("\n" + "-" * 60 + "\n")
    f.write("2. 各课程类别缴费额占比\n")
    f.write("-" * 60 + "\n")
    f.write(category_payment.to_string(index=False) + "\n")
    
    f.write("\n" + "-" * 60 + "\n")
    f.write("3. 缴费总额最高的Top3热门课程\n")
    f.write("-" * 60 + "\n")
    f.write(course_payment.to_string(index=False) + "\n")
    
    f.write("\n" + "-" * 60 + "\n")
    f.write("4. 课程状态分析\n")
    f.write("-" * 60 + "\n")
    f.write(status_payment.to_string(index=False) + "\n")
    f.write(f"\n已退费总额：{refund_amount:,.2f} 元\n")
    f.write(f"退费占比：{refund_ratio}%\n")
    
    f.write("\n" + "-" * 60 + "\n")
    f.write("5. 城市人均缴费分析\n")
    f.write("-" * 60 + "\n")
    f.write(city_analysis.to_string(index=False) + "\n")

print("\n" + "=" * 60)
print("执行完成！")
print("=" * 60)
print("生成的文件：")
print("1. 修正后学员缴费数据表.csv")
print("2. 月度_课程类别_缴费总额汇总表.csv")
print("3. 月度_城市_缴费总额汇总表.csv")
print("4. 统计分析结果.txt")
