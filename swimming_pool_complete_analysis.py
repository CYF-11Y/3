#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
游泳馆学员缴费数据全流程分析系统
技术栈：Python + Pandas + Matplotlib
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
matplotlib.rcParams['axes.unicode_minus'] = False
import random
from datetime import datetime, timedelta

# ====================== 配置参数 ======================
START_DATE = datetime(2025, 9, 1)
END_DATE = datetime(2026, 2, 28)
TOTAL_RECORDS = 5000

# 课程类别和名称映射
COURSE_CATEGORIES = {
    '少儿游泳': ['少儿蛙泳基础班', '少儿自由泳提高班', '少儿仰泳专项班', '少儿蝶泳精英班'],
    '成人游泳': ['成人蛙泳入门班', '成人自由泳速成班', '成人水中健身课', '成人减脂游泳班'],
    '私教课程': ['一对一私教课', '一对二私教课', '一对三私教课', '私教包月套餐'],
    '亲子游泳': ['亲子启蒙班', '亲子互动班', '亲子技能提升班', '亲子水上游戏课'],
    '考级课程': ['等级考试预备班', '一级考级冲刺班', '二级考级专项班', '三级考级集训班'],
    '集训课程': ['暑期集训营', '寒假集训营', '国庆集训班', '考前集中训练营']
}

CITIES = ['北京', '上海', '广州', '深圳', '杭州', '南京', '成都', '武汉', '西安', '重庆']
PAYMENT_METHODS = ['微信支付', '支付宝', '银行卡', '现金', '分期']
COURSE_STATUSES = ['已报名', '已开课', '已结课', '已退费']

# 模拟中文姓名库
FAMILY_NAMES = ['张', '王', '李', '赵', '刘', '陈', '杨', '黄', '吴', '周', '徐', '孙', '马', '朱', '胡', '林', '郭', '何', '高', '罗']
GIVEN_NAMES = ['伟', '芳', '娜', '敏', '静', '丽', '强', '磊', '洋', '艳', '勇', '军', '杰', '娟', '涛', '明', '超', '秀英', '华', '平']

# ====================== 生成模拟数据 ======================
def generate_chinese_name():
    """生成随机中文姓名"""
    family = random.choice(FAMILY_NAMES)
    given = random.choice(GIVEN_NAMES)
    if random.random() < 0.5:
        given += random.choice(GIVEN_NAMES)
    return family + given

def random_date(start, end):
    """生成随机日期"""
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)

def generate_data():
    """生成模拟缴费数据"""
    data = []
    for i in range(TOTAL_RECORDS):
        student_id = f'STU{10000 + i:05d}'
        student_name = generate_chinese_name()
        
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
            '学员ID': student_id,
            '学员姓名': student_name,
            '课程类别': course_category,
            '课程名称': course_name,
            '报名节数/期数': quantity,
            '单价': unit_price,
            '缴费总额': payment_total,
            '缴费日期': payment_date.strftime('%Y-%m-%d'),
            '学员所在城市': city,
            '缴费方式': payment_method,
            '课程状态': course_status,
            '正确缴费总额': correct_total  # 用于后续校验
        })
    
    return pd.DataFrame(data)

# ====================== 数据处理 ======================
def data_processing(df):
    """数据校验与修正"""
    print("=" * 60)
    print("数据处理：校验与修正")
    print("=" * 60)
    
    # 找出需要修正的记录
    correction_needed = df[df['缴费总额'] != df['正确缴费总额']].copy()
    correction_needed['修正前缴费总额'] = correction_needed['缴费总额']
    correction_needed['修正后缴费总额'] = correction_needed['正确缴费总额']
    
    # 修正数据
    df['缴费总额'] = df['正确缴费总额']
    
    # 删除辅助列
    df = df.drop(columns=['正确缴费总额'])
    
    # 输出修正记录
    print(f"总记录数：{len(df)}")
    print(f"需要修正的记录数：{len(correction_needed)} ({len(correction_needed)/len(df)*100:.2f}%)")
    
    # 保存修正记录表
    correction_table = correction_needed[['学员ID', '修正前缴费总额', '修正后缴费总额']]
    correction_table.to_excel('修正记录标注表.xlsx', index=False)
    print("修正记录标注表已保存：修正记录标注表.xlsx")
    
    # 保存修正后的数据表
    df.to_excel('修正后学员缴费数据表.xlsx', index=False)
    print("修正后的数据表已保存：修正后学员缴费数据表.xlsx")
    
    return df, correction_table

def create_monthly_summary(df):
    """生成月度聚合汇总表"""
    print("\n" + "=" * 60)
    print("生成月度聚合汇总表")
    print("=" * 60)
    
    # 转换日期格式并提取月份
    df['缴费日期'] = pd.to_datetime(df['缴费日期'])
    df['月份'] = df['缴费日期'].dt.strftime('%Y-%m')
    
    # 「月度 - 课程类别 - 缴费总额」汇总表
    monthly_by_category = df.groupby(['月份', '课程类别'])['缴费总额'].sum().reset_index()
    monthly_by_category = monthly_by_category.sort_values(['月份', '课程类别'])
    monthly_by_category.to_excel('月度_课程类别_缴费总额汇总表.xlsx', index=False)
    print("「月度 - 课程类别 - 缴费总额」汇总表已保存：月度_课程类别_缴费总额汇总表.xlsx")
    
    # 「月度 - 学员所在城市 - 缴费总额」汇总表
    monthly_by_city = df.groupby(['月份', '学员所在城市'])['缴费总额'].sum().reset_index()
    monthly_by_city = monthly_by_city.rename(columns={'学员所在城市': '城市'})
    monthly_by_city = monthly_by_city.sort_values(['月份', '城市'])
    monthly_by_city.to_excel('月度_城市_缴费总额汇总表.xlsx', index=False)
    print("「月度 - 学员所在城市 - 缴费总额」汇总表已保存：月度_城市_缴费总额汇总表.xlsx")
    
    return monthly_by_category, monthly_by_city

# ====================== 统计分析 ======================
def statistical_analysis(df):
    """统计分析"""
    print("\n" + "=" * 60)
    print("统计分析结果")
    print("=" * 60)
    
    total_payment = df['缴费总额'].sum()
    print(f"\n总缴费额：{total_payment:,.2f} 元")
    
    # 1. 城市缴费占比表
    print("\n" + "-" * 60)
    print("1. 各城市缴费额占比")
    print("-" * 60)
    city_payment = df.groupby('学员所在城市')['缴费总额'].sum().reset_index()
    city_payment = city_payment.rename(columns={'缴费总额': '缴费总额', '学员所在城市': '城市'})
    city_payment['占比(%)'] = (city_payment['缴费总额'] / total_payment * 100).round(2)
    city_payment = city_payment.sort_values('缴费总额', ascending=False).reset_index(drop=True)
    city_payment.index += 1  # 排名从1开始
    city_payment.index.name = '排名'
    print(city_payment.to_string())
    city_payment.to_excel('城市缴费占比表.xlsx')
    
    # 2. 课程类别缴费占比表
    print("\n" + "-" * 60)
    print("2. 各课程类别缴费额占比")
    print("-" * 60)
    category_payment = df.groupby('课程类别')['缴费总额'].sum().reset_index()
    category_payment['占比(%)'] = (category_payment['缴费总额'] / total_payment * 100).round(2)
    category_payment = category_payment.sort_values('缴费总额', ascending=False).reset_index(drop=True)
    category_payment.index += 1
    category_payment.index.name = '排名'
    print(category_payment.to_string())
    category_payment.to_excel('课程类别缴费占比表.xlsx')
    
    # 3. Top3热门课程及贡献度
    print("\n" + "-" * 60)
    print("3. 缴费总额最高的Top3热门课程")
    print("-" * 60)
    course_payment = df.groupby('课程名称')['缴费总额'].sum().reset_index()
    course_payment['贡献度(%)'] = (course_payment['缴费总额'] / total_payment * 100).round(2)
    course_payment = course_payment.sort_values('缴费总额', ascending=False).head(3).reset_index(drop=True)
    course_payment.index += 1
    course_payment.index.name = '排名'
    print(course_payment.to_string())
    course_payment.to_excel('Top3热门课程表.xlsx')
    
    # 4. 课程状态分析表
    print("\n" + "-" * 60)
    print("4. 课程状态分析")
    print("-" * 60)
    status_payment = df.groupby('课程状态')['缴费总额'].sum().reset_index()
    status_payment['占比(%)'] = (status_payment['缴费总额'] / total_payment * 100).round(2)
    status_payment = status_payment.sort_values('缴费总额', ascending=False).reset_index(drop=True)
    status_payment.index += 1
    status_payment.index.name = '排名'
    print(status_payment.to_string())
    
    # 退费专项分析
    refund_amount = df[df['课程状态'] == '已退费']['缴费总额'].sum()
    refund_ratio = (refund_amount / total_payment * 100).round(2)
    print(f"\n已退费总额：{refund_amount:,.2f} 元")
    print(f"退费占比：{refund_ratio}%")
    
    # 退费高发课程
    print("\n退费高发课程Top5：")
    refund_by_course = df[df['课程状态'] == '已退费'].groupby('课程名称')['缴费总额'].sum().reset_index()
    refund_by_course = refund_by_course.sort_values('缴费总额', ascending=False).head(5).reset_index(drop=True)
    refund_by_course.index += 1
    refund_by_course.index.name = '排名'
    print(refund_by_course.to_string())
    
    # 保存退费分析
    with pd.ExcelWriter('退费分析表.xlsx') as writer:
        status_payment.to_excel(writer, sheet_name='课程状态分布')
        refund_by_course.to_excel(writer, sheet_name='退费高发课程')
    
    # 5. 城市人均缴费分析表
    print("\n" + "-" * 60)
    print("5. 城市人均缴费分析")
    print("-" * 60)
    # 按学员ID去重统计各城市学员数
    city_students = df.drop_duplicates('学员ID').groupby('学员所在城市')['学员ID'].count().reset_index()
    city_students = city_students.rename(columns={'学员所在城市': '城市', '学员ID': '学员数'})
    
    # 计算各城市总缴费额
    city_total = df.groupby('学员所在城市')['缴费总额'].sum().reset_index()
    city_total = city_total.rename(columns={'缴费总额': '总缴费额', '学员所在城市': '城市'})
    
    # 合并计算人均缴费
    city_analysis = pd.merge(city_students, city_total, on='城市')
    city_analysis['人均缴费额(元)'] = (city_analysis['总缴费额'] / city_analysis['学员数']).round(2)
    city_analysis = city_analysis.sort_values('人均缴费额(元)', ascending=False).reset_index(drop=True)
    city_analysis.index += 1
    city_analysis.index.name = '排名'
    print(city_analysis.to_string())
    city_analysis.to_excel('城市人均缴费分析表.xlsx')
    
    return {
        'city_payment': city_payment,
        'category_payment': category_payment,
        'course_payment': course_payment,
        'status_payment': status_payment,
        'city_analysis': city_analysis
    }

# ====================== 可视化 ======================
def create_visualizations(df, monthly_by_category):
    """用Matplotlib绘制可视化图表"""
    print("\n" + "=" * 60)
    print("生成可视化图表")
    print("=" * 60)
    
    # 1. 月度缴费总额趋势折线图
    print("生成：月度缴费总额趋势折线图")
    df['缴费日期'] = pd.to_datetime(df['缴费日期'])
    df['月份'] = df['缴费日期'].dt.strftime('%Y-%m')
    monthly_total = df.groupby('月份')['缴费总额'].sum().reset_index()
    
    plt.figure(figsize=(12, 6))
    plt.plot(monthly_total['月份'], monthly_total['缴费总额'], marker='o', linewidth=2, markersize=8, color='#1f77b4')
    plt.title('月度缴费总额趋势图（2025.09-2026.02）', fontsize=14, pad=20)
    plt.xlabel('月份', fontsize=12)
    plt.ylabel('缴费总额（元）', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    
    # 添加数据标签
    for x, y in zip(monthly_total['月份'], monthly_total['缴费总额']):
        plt.text(x, y + 50000, f'{y/10000:.1f}万', ha='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('月度缴费总额趋势折线图.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. 缴费分布漏斗图（简化版，使用Matplotlib实现）
    print("生成：缴费分布漏斗图")
    
    # 计算各层级金额（城市→课程类别→课程状态）
    total = df['缴费总额'].sum()
    
    # 层级1：城市维度取缴费Top3的城市合计
    top3_cities_total = df.groupby('学员所在城市')['缴费总额'].sum().sort_values(ascending=False).head(3).sum()
    
    # 层级2：课程类别维度取缴费Top2的类别合计（基于Top3城市）
    top3_cities = df.groupby('学员所在城市')['缴费总额'].sum().sort_values(ascending=False).head(3).index.tolist()
    top3_cities_data = df[df['学员所在城市'].isin(top3_cities)]
    top2_categories_total = top3_cities_data.groupby('课程类别')['缴费总额'].sum().sort_values(ascending=False).head(2).sum()
    
    # 层级3：课程状态-已结课
    completed_total = df[df['课程状态'] == '已结课']['缴费总额'].sum()
    
    # 层级4：课程状态-已开课
    ongoing_total = df[df['课程状态'] == '已开课']['缴费总额'].sum()
    
    # 漏斗数据
    funnel_levels = ['总缴费额', 'Top3城市合计', 'Top2类别合计', '已结课', '已开课']
    funnel_values = [total, top3_cities_total, top2_categories_total, completed_total, ongoing_total]
    funnel_percents = [v/total*100 for v in funnel_values]
    
    # 绘制漏斗图
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # 漏斗宽度
    max_width = 0.8
    widths = [max_width * (v / total) for v in funnel_values]
    
    # 颜色渐变
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    # 绘制每个层级
    y_positions = range(len(funnel_levels))
    for i, (level, value, percent, width) in enumerate(zip(funnel_levels, funnel_values, funnel_percents, widths)):
        # 绘制矩形
        left = (max_width - width) / 2
        rect = plt.Rectangle((left, i - 0.4), width, 0.8, color=colors[i], alpha=0.7)
        ax.add_patch(rect)
        
        # 添加文本标签
        plt.text(max_width/2, i, f'{level}\n{value/10000:.1f}万 ({percent:.1f}%)', 
                 ha='center', va='center', fontsize=11, fontweight='bold')
    
    ax.set_xlim(0, max_width)
    ax.set_ylim(-0.5, len(funnel_levels) - 0.5)
    ax.set_yticks(y_positions)
    ax.set_yticklabels([])  # 隐藏y轴刻度
    ax.set_xticks([])  # 隐藏x轴刻度
    ax.set_title('缴费分布漏斗图（城市→课程类别→课程状态）', fontsize=14, pad=20)
    
    # 移除边框
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig('缴费分布漏斗图.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. 补充：课程类别饼图
    print("生成：课程类别缴费分布饼图")
    category_total = df.groupby('课程类别')['缴费总额'].sum()
    plt.figure(figsize=(10, 8))
    category_total.plot(kind='pie', autopct='%1.1f%%', colors=colors[:6])
    plt.title('课程类别缴费分布', fontsize=14)
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig('课程类别缴费分布饼图.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("\n图表已生成：")
    print("1. 月度缴费总额趋势折线图.png")
    print("2. 缴费分布漏斗图.png")
    print("3. 课程类别缴费分布饼图.png")

# ====================== 主函数 ======================
def main():
    print("=" * 70)
    print("游泳馆学员缴费数据全流程分析系统")
    print("技术栈：Python + Pandas + Matplotlib")
    print("=" * 70)
    
    # 1. 生成数据
    print("\n[1/5] 生成模拟数据...")
    df = generate_data()
    print(f"成功生成 {len(df)} 条记录")
    
    # 2. 数据处理
    print("\n[2/5] 数据校验与修正...")
    df_clean, correction_table = data_processing(df)
    
    # 3. 月度汇总
    print("\n[3/5] 生成月度汇总表...")
    monthly_by_category, monthly_by_city = create_monthly_summary(df_clean)
    
    # 4. 统计分析
    print("\n[4/5] 统计分析...")
    stats_results = statistical_analysis(df_clean)
    
    # 5. 可视化
    print("\n[5/5] 生成可视化图表...")
    create_visualizations(df_clean, monthly_by_category)
    
    print("\n" + "=" * 70)
    print("分析完成！所有结果已保存到当前目录。")
    print("=" * 70)

if __name__ == "__main__":
    main()
