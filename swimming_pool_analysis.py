# -*- coding: utf-8 -*-
"""
游泳馆学员缴费数据分析系统
技术栈：Python + Pandas + Matplotlib
功能：数据处理、统计分析、可视化
时间范围：2025-09-01 至 2026-02-28
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import random
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 设置随机种子以确保可复现性
np.random.seed(42)
random.seed(42)

# ==================== 第一部分：生成基础数据 ====================

def generate_base_data():
    """生成游泳馆学员缴费基础数据"""
    
    # 定义数据维度
    cities = ['北京', '上海', '广州', '深圳', '杭州', '南京', '成都', '武汉']
    course_categories = ['少儿游泳', '成人游泳', '私教课程', '亲子游泳', '考级课程', '集训课程']
    
    # 课程名称映射
    course_names_map = {
        '少儿游泳': ['少儿基础班', '少儿进阶班', '少儿强化班', '少儿长训班'],
        '成人游泳': ['成人零基础班', '成人进阶班', '成人自由泳班', '成人蛙泳班'],
        '私教课程': ['一对一私教', '一对二私教', '一对三私教', 'VIP私教'],
        '亲子游泳': ['亲子启蒙班', '亲子互动班', '亲子进阶班', '亲子游戏班'],
        '考级课程': ['一级考级班', '二级考级班', '三级考级班', '四级考级班'],
        '集训课程': ['暑期集训营', '寒假集训营', '周末集训营', '赛前集训营']
    }
    
    payment_methods = ['微信支付', '支付宝', '银行卡', '现金', '分期']
    course_statuses = ['已报名', '已开课', '已结课', '已退费']
    
    # 价格体系（元/节或元/期）
    price_ranges = {
        '少儿游泳': (120, 180),
        '成人游泳': (150, 220),
        '私教课程': (300, 500),
        '亲子游泳': (200, 350),
        '考级课程': (180, 280),
        '集训课程': (1500, 3500)
    }
    
    # 生成日期范围（2025-09-01 至 2026-02-28）
    start_date = datetime(2025, 9, 1)
    end_date = datetime(2026, 2, 28)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # 生成学员数据
    records = []
    student_id = 10001
    
    for _ in range(300):
        city = random.choice(cities)
        category = random.choice(course_categories)
        course_name = random.choice(course_names_map[category])
        
        if category == '集训课程':
            quantity = random.choice([1, 2, 3])
            unit_price = random.randint(price_ranges[category][0], price_ranges[category][1])
        else:
            quantity = random.choice([8, 12, 16, 20, 24, 30, 48])
            unit_price = random.randint(price_ranges[category][0], price_ranges[category][1])
        
        correct_total = quantity * unit_price
        
        if random.random() < 0.1:
            error_factor = random.uniform(0.95, 1.05)
            recorded_total = round(correct_total * error_factor, 2)
        else:
            recorded_total = correct_total
        
        date = random.choice(date_range)
        status = random.choice(course_statuses)
        payment_method = random.choice(payment_methods)
        
        surnames = ['张', '王', '李', '刘', '陈', '杨', '黄', '赵', '吴', '周', '徐', '孙', '马', '朱', '胡', '郭', '何', '林', '罗', '高']
        names = ['伟', '芳', '娜', '敏', '静', '丽', '强', '磊', '军', '洋', '勇', '艳', '杰', '涛', '明', '超', '秀英', '华', '鹏', '飞', '婷', '宇', '浩', '欣', '雨', '晨', '轩', '昊', '瑞', '嘉']
        student_name = random.choice(surnames) + random.choice(names)
        
        records.append({
            '学员ID': f'STU{student_id}',
            '学员姓名': student_name,
            '课程类别': category,
            '课程名称': course_name,
            '报名节数/期数': quantity,
            '单价': unit_price,
            '缴费总额': recorded_total,
            '缴费日期': date.strftime('%Y-%m-%d'),
            '学员所在城市': city,
            '缴费方式': payment_method,
            '课程状态': status
        })
        
        student_id += 1
    
    df = pd.DataFrame(records)
    return df


# ==================== 第二部分：数据处理（Pandas）====================

def process_data(df):
    """数据校验与修正"""
    
    df['计算缴费总额'] = df['报名节数/期数'] * df['单价']
    df['需要修正'] = abs(df['缴费总额'] - df['计算缴费总额']) > 0.01
    
    corrections = df[df['需要修正']].copy()
    correction_records = []
    
    for idx, row in corrections.iterrows():
        correction_records.append({
            '学员ID': row['学员ID'],
            '修正前缴费总额': row['缴费总额'],
            '修正后缴费总额': row['计算缴费总额']
        })
    
    correction_df = pd.DataFrame(correction_records)
    
    df['缴费总额'] = df['计算缴费总额']
    df = df.drop(['计算缴费总额', '需要修正'], axis=1)
    
    return df, correction_df


def generate_monthly_summary(df):
    """生成月度聚合汇总表"""
    
    df['缴费月份'] = pd.to_datetime(df['缴费日期']).dt.to_period('M').astype(str)
    
    summary_by_category = df.groupby(['缴费月份', '课程类别'])['缴费总额'].sum().reset_index()
    summary_by_category.columns = ['月份', '课程类别', '缴费总额']
    summary_by_category = summary_by_category.sort_values(['月份', '缴费总额'], ascending=[True, False])
    
    summary_by_city = df.groupby(['缴费月份', '学员所在城市'])['缴费总额'].sum().reset_index()
    summary_by_city.columns = ['月份', '城市', '缴费总额']
    summary_by_city = summary_by_city.sort_values(['月份', '缴费总额'], ascending=[True, False])
    
    return summary_by_category, summary_by_city


# ==================== 第三部分：统计分析（Pandas）====================

def calculate_dimension_ratios(df):
    """计算各维度占比"""
    
    total_amount = df['缴费总额'].sum()
    
    city_stats = df.groupby('学员所在城市')['缴费总额'].sum().reset_index()
    city_stats['占比(%)'] = (city_stats['缴费总额'] / total_amount * 100).round(2)
    city_stats = city_stats.sort_values('缴费总额', ascending=False)
    city_stats['累计占比(%)'] = city_stats['占比(%)'].cumsum().round(2)
    
    category_stats = df.groupby('课程类别')['缴费总额'].sum().reset_index()
    category_stats['占比(%)'] = (category_stats['缴费总额'] / total_amount * 100).round(2)
    category_stats = category_stats.sort_values('缴费总额', ascending=False)
    category_stats['累计占比(%)'] = category_stats['占比(%)'].cumsum().round(2)
    
    return city_stats, category_stats


def get_top3_courses(df):
    """统计Top3热门课程"""
    
    total_amount = df['缴费总额'].sum()
    
    course_stats = df.groupby('课程名称')['缴费总额'].sum().reset_index()
    course_stats['贡献度(%)'] = (course_stats['缴费总额'] / total_amount * 100).round(2)
    course_stats = course_stats.sort_values('缴费总额', ascending=False)
    
    top3 = course_stats.head(3).copy()
    top3['排名'] = range(1, 4)
    top3 = top3[['排名', '课程名称', '缴费总额', '贡献度(%)']]
    
    return top3, course_stats


def analyze_course_status(df):
    """课程状态分析"""
    
    total_amount = df['缴费总额'].sum()
    
    status_stats = df.groupby('课程状态')['缴费总额'].sum().reset_index()
    status_stats['占比(%)'] = (status_stats['缴费总额'] / total_amount * 100).round(2)
    status_stats = status_stats.sort_values('缴费总额', ascending=False)
    
    refund_amount = status_stats[status_stats['课程状态'] == '已退费']['缴费总额'].sum() if '已退费' in status_stats['课程状态'].values else 0
    refund_ratio = (refund_amount / total_amount * 100).round(2)
    
    return status_stats, refund_amount, refund_ratio


def analyze_city_per_capita(df):
    """城市人均缴费分析"""
    
    city_students = df.groupby('学员所在城市')['学员ID'].nunique().reset_index()
    city_students.columns = ['城市', '学员数量']
    
    city_amount = df.groupby('学员所在城市')['缴费总额'].sum().reset_index()
    city_amount.columns = ['城市', '缴费总额']
    
    city_per_capita = pd.merge(city_amount, city_students, on='城市')
    city_per_capita['人均缴费(元)'] = (city_per_capita['缴费总额'] / city_per_capita['学员数量']).round(2)
    city_per_capita = city_per_capita.sort_values('人均缴费(元)', ascending=False)
    
    return city_per_capita


# ==================== 第四部分：可视化（Matplotlib）====================

def plot_monthly_trend(df):
    """绘制月度缴费总额趋势折线图"""
    
    df['缴费月份'] = pd.to_datetime(df['缴费日期']).dt.to_period('M').astype(str)
    monthly_total = df.groupby('缴费月份')['缴费总额'].sum().reset_index()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(monthly_total['缴费月份'], monthly_total['缴费总额'], 
            marker='o', linewidth=2.5, markersize=8, color='#2E86AB', label='月度缴费总额')
    
    ax.fill_between(monthly_total['缴费月份'], monthly_total['缴费总额'], 
                    alpha=0.3, color='#2E86AB')
    
    for i, (month, amount) in enumerate(zip(monthly_total['缴费月份'], monthly_total['缴费总额'])):
        ax.annotate(f'{amount:,.0f}', xy=(i, amount), textcoords="offset points", 
                   xytext=(0, 10), ha='center', fontsize=9, color='#333333')
    
    ax.set_xlabel('月份', fontsize=12, fontweight='bold')
    ax.set_ylabel('缴费总额（元）', fontsize=12, fontweight='bold')
    ax.set_title('游泳馆月度缴费总额趋势分析（2025-09 至 2026-02）', fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='upper right', fontsize=10)
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('月度缴费总额趋势图.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✓ 月度缴费总额趋势图已保存：月度缴费总额趋势图.png")
    return monthly_total


def plot_category_monthly_trend(df):
    """绘制各课程类别月度缴费趋势折线图"""
    
    df['缴费月份'] = pd.to_datetime(df['缴费日期']).dt.to_period('M').astype(str)
    category_monthly = df.groupby(['缴费月份', '课程类别'])['缴费总额'].sum().reset_index()
    category_pivot = category_monthly.pivot(index='缴费月份', columns='课程类别', values='缴费总额').fillna(0)
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
    
    for idx, category in enumerate(category_pivot.columns):
        ax.plot(category_pivot.index, category_pivot[category], 
                marker='o', linewidth=2, markersize=6, 
                color=colors[idx % len(colors)], label=category)
    
    ax.set_xlabel('月份', fontsize=12, fontweight='bold')
    ax.set_ylabel('缴费总额（元）', fontsize=12, fontweight='bold')
    ax.set_title('各课程类别月度缴费趋势对比', fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='upper left', fontsize=10, ncol=3)
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('课程类别月度趋势图.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✓ 课程类别月度趋势图已保存：课程类别月度趋势图.png")


def plot_funnel_chart(df):
    """绘制缴费分布漏斗图（城市→课程类别→课程状态）"""
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 8))
    
    # 第一层：城市维度
    city_data = df.groupby('学员所在城市')['缴费总额'].sum().sort_values(ascending=True)
    colors_city = plt.cm.Blues(np.linspace(0.4, 0.9, len(city_data)))
    
    ax1 = axes[0]
    bars1 = ax1.barh(city_data.index, city_data.values, color=colors_city, edgecolor='white', linewidth=1.5)
    ax1.set_xlabel('缴费总额（元）', fontsize=11, fontweight='bold')
    ax1.set_title('第一层：学员所在城市分布', fontsize=12, fontweight='bold', pad=15)
    ax1.grid(axis='x', alpha=0.3, linestyle='--')
    
    for i, (city, amount) in enumerate(city_data.items()):
        percentage = (amount / city_data.sum() * 100)
        ax1.text(amount + 5000, i, f'{amount:,.0f} ({percentage:.1f}%)', 
                va='center', fontsize=9, color='#333333')
    
    # 第二层：课程类别维度
    category_data = df.groupby('课程类别')['缴费总额'].sum().sort_values(ascending=True)
    colors_category = plt.cm.Greens(np.linspace(0.4, 0.9, len(category_data)))
    
    ax2 = axes[1]
    bars2 = ax2.barh(category_data.index, category_data.values, color=colors_category, edgecolor='white', linewidth=1.5)
    ax2.set_xlabel('缴费总额（元）', fontsize=11, fontweight='bold')
    ax2.set_title('第二层：课程类别分布', fontsize=12, fontweight='bold', pad=15)
    ax2.grid(axis='x', alpha=0.3, linestyle='--')
    
    for i, (category, amount) in enumerate(category_data.items()):
        percentage = (amount / category_data.sum() * 100)
        ax2.text(amount + 8000, i, f'{amount:,.0f} ({percentage:.1f}%)', 
                va='center', fontsize=9, color='#333333')
    
    # 第三层：课程状态维度
    status_data = df.groupby('课程状态')['缴费总额'].sum().sort_values(ascending=True)
    colors_status = plt.cm.Oranges(np.linspace(0.4, 0.9, len(status_data)))
    
    ax3 = axes[2]
    bars3 = ax3.barh(status_data.index, status_data.values, color=colors_status, edgecolor='white', linewidth=1.5)
    ax3.set_xlabel('缴费总额（元）', fontsize=11, fontweight='bold')
    ax3.set_title('第三层：课程状态分布', fontsize=12, fontweight='bold', pad=15)
    ax3.grid(axis='x', alpha=0.3, linestyle='--')
    
    for i, (status, amount) in enumerate(status_data.items()):
        percentage = (amount / status_data.sum() * 100)
        ax3.text(amount + 8000, i, f'{amount:,.0f} ({percentage:.1f}%)', 
                va='center', fontsize=9, color='#333333')
    
    plt.suptitle('游泳馆缴费分布漏斗图（城市→课程类别→课程状态）', 
                 fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('缴费分布漏斗图.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✓ 缴费分布漏斗图已保存：缴费分布漏斗图.png")


def plot_city_category_heatmap(df):
    """绘制城市-课程类别缴费热力图"""
    
    pivot_data = df.groupby(['学员所在城市', '课程类别'])['缴费总额'].sum().reset_index()
    heatmap_data = pivot_data.pivot(index='学员所在城市', columns='课程类别', values='缴费总额').fillna(0)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    im = ax.imshow(heatmap_data.values, cmap='YlOrRd', aspect='auto')
    
    ax.set_xticks(np.arange(len(heatmap_data.columns)))
    ax.set_yticks(np.arange(len(heatmap_data.index)))
    ax.set_xticklabels(heatmap_data.columns, fontsize=10)
    ax.set_yticklabels(heatmap_data.index, fontsize=10)
    
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    
    for i in range(len(heatmap_data.index)):
        for j in range(len(heatmap_data.columns)):
            value = heatmap_data.iloc[i, j]
            text_color = 'white' if value > heatmap_data.values.max() * 0.5 else 'black'
            ax.text(j, i, f'{value:,.0f}', ha="center", va="center", 
                   color=text_color, fontsize=8, fontweight='bold')
    
    ax.set_title('城市-课程类别缴费热力图', fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('课程类别', fontsize=12, fontweight='bold')
    ax.set_ylabel('学员所在城市', fontsize=12, fontweight='bold')
    
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('缴费总额（元）', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('城市课程类别热力图.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✓ 城市-课程类别热力图已保存：城市课程类别热力图.png")


# ==================== 第五部分：输出结果 ====================

def output_to_excel(df, correction_df, summary_by_category, summary_by_city,
                    city_stats, category_stats, top3, course_stats, 
                    status_stats, refund_amount, refund_ratio, city_per_capita):
    """输出所有结果到Excel文件"""
    
    with pd.ExcelWriter('游泳馆缴费数据分析报告.xlsx', engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='修正后的缴费数据', index=False)
        
        if len(correction_df) > 0:
            correction_df.to_excel(writer, sheet_name='数据修正记录', index=False)
        
        summary_by_category.to_excel(writer, sheet_name='月度课程类别汇总', index=False)
        summary_by_city.to_excel(writer, sheet_name='月度城市汇总', index=False)
        city_stats.to_excel(writer, sheet_name='城市缴费占比', index=False)
        category_stats.to_excel(writer, sheet_name='课程类别占比', index=False)
        top3.to_excel(writer, sheet_name='TOP3热门课程', index=False)
        course_stats.to_excel(writer, sheet_name='全部课程统计', index=False)
        status_stats.to_excel(writer, sheet_name='课程状态分析', index=False)
        city_per_capita.to_excel(writer, sheet_name='城市人均缴费', index=False)
    
    print("✓ Excel报告已保存：游泳馆缴费数据分析报告.xlsx")


def print_summary_to_console(df, correction_df, summary_by_category, summary_by_city,
                             city_stats, category_stats, top3, status_stats, 
                             refund_amount, refund_ratio, city_per_capita):
    """在控制台打印汇总结果"""
    
    print("\n" + "=" * 100)
    print("游泳馆学员缴费数据分析系统 - 结果汇总")
    print("数据时间范围：2025-09-01 至 2026-02-28")
    print("=" * 100)
    
    print("\n【一、数据校验与修正记录】")
    print("-" * 100)
    if len(correction_df) > 0:
        print(f"共发现 {len(correction_df)} 条记录需要修正\n")
        print(correction_df.to_string(index=False))
    else:
        print("未发现需要修正的记录，所有数据计算准确。")
    
    print("\n\n【二、月度-课程类别-缴费总额汇总表】")
    print("-" * 100)
    print(summary_by_category.to_string(index=False))
    
    print("\n\n【三、月度-学员所在城市-缴费总额汇总表】")
    print("-" * 100)
    print(summary_by_city.to_string(index=False))
    
    print("\n\n【四、城市缴费占比分析】")
    print("-" * 100)
    print(city_stats.to_string(index=False))
    
    print("\n\n【五、课程类别缴费占比分析】")
    print("-" * 100)
    print(category_stats.to_string(index=False))
    
    print("\n\n【六、TOP3热门课程分析】")
    print("-" * 100)
    print(top3.to_string(index=False))
    
    print("\n\n【七、课程状态分析】")
    print("-" * 100)
    print(status_stats.to_string(index=False))
    print(f"\n已退费金额: {refund_amount:.2f} 元")
    print(f"退费占比: {refund_ratio:.2f}%")
    
    print("\n\n【八、城市人均缴费分析】")
    print("-" * 100)
    print(city_per_capita.to_string(index=False))
    
    print("\n" + "=" * 100)
    print("所有结果已保存，包含：")
    print("  - Excel报告：游泳馆缴费数据分析报告.xlsx")
    print("  - 可视化图表：月度缴费总额趋势图.png")
    print("  - 可视化图表：课程类别月度趋势图.png")
    print("  - 可视化图表：缴费分布漏斗图.png")
    print("  - 可视化图表：城市课程类别热力图.png")
    print("=" * 100)


# ==================== 主程序入口 ====================

if __name__ == "__main__":
    print("=" * 80)
    print("游泳馆学员缴费数据分析系统")
    print("技术栈：Python + Pandas + Matplotlib")
    print("=" * 80)
    
    print("\n[1/6] 正在生成游泳馆学员缴费数据...")
    df = generate_base_data()
    print(f"✓ 已生成 {len(df)} 条缴费记录")
    
    print("\n[2/6] 正在进行数据校验与修正...")
    df_corrected, correction_df = process_data(df)
    print(f"✓ 数据校验完成，发现 {len(correction_df)} 条记录需要修正")
    
    print("\n[3/6] 正在生成月度聚合汇总表...")
    summary_by_category, summary_by_city = generate_monthly_summary(df_corrected)
    print("✓ 月度汇总表生成完成")
    
    print("\n[4/6] 正在进行统计分析...")
    city_stats, category_stats = calculate_dimension_ratios(df_corrected)
    top3, course_stats = get_top3_courses(df_corrected)
    status_stats, refund_amount, refund_ratio = analyze_course_status(df_corrected)
    city_per_capita = analyze_city_per_capita(df_corrected)
    print("✓ 统计分析完成")
    
    print("\n[5/6] 正在生成可视化图表（Matplotlib）...")
    plot_monthly_trend(df_corrected)
    plot_category_monthly_trend(df_corrected)
    plot_funnel_chart(df_corrected)
    plot_city_category_heatmap(df_corrected)
    print("✓ 可视化图表生成完成")
    
    print("\n[6/6] 正在输出Excel报告...")
    output_to_excel(df_corrected, correction_df, summary_by_category, summary_by_city,
                    city_stats, category_stats, top3, course_stats, 
                    status_stats, refund_amount, refund_ratio, city_per_capita)
    
    print_summary_to_console(df_corrected, correction_df, summary_by_category, summary_by_city,
                            city_stats, category_stats, top3, status_stats, 
                            refund_amount, refund_ratio, city_per_capita)