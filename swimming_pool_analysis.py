# -*- coding: utf-8 -*-
"""
游泳馆学员缴费数据分析系统
功能：数据处理、统计分析、可视化说明
时间范围：2025-09-01 至 2026-02-28
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

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
        '集训课程': (1500, 3500)  # 按期，每期价格
    }
    
    # 生成日期范围（2025-09-01 至 2026-02-28）
    start_date = datetime(2025, 9, 1)
    end_date = datetime(2026, 2, 28)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # 生成学员数据
    records = []
    student_id = 10001
    
    # 生成约300条缴费记录
    for _ in range(300):
        # 随机选择城市和课程
        city = random.choice(cities)
        category = random.choice(course_categories)
        course_name = random.choice(course_names_map[category])
        
        # 确定是按期还是按节
        if category == '集训课程':
            # 集训课程按期
            quantity = random.choice([1, 2, 3])  # 期数
            unit_price = random.randint(price_ranges[category][0], price_ranges[category][1])
        else:
            # 其他课程按节
            quantity = random.choice([8, 12, 16, 20, 24, 30, 48])  # 节数
            unit_price = random.randint(price_ranges[category][0], price_ranges[category][1])
        
        # 计算正确的缴费总额
        correct_total = quantity * unit_price
        
        # 模拟部分数据存在计算偏差（约10%的记录有偏差）
        if random.random() < 0.1:
            # 产生偏差（±5%范围内）
            error_factor = random.uniform(0.95, 1.05)
            recorded_total = round(correct_total * error_factor, 2)
        else:
            recorded_total = correct_total
        
        # 随机日期（考虑淡旺季因素：9月、10月、2月为旺季，11月、12月、1月为淡季）
        date = random.choice(date_range)
        
        # 课程状态
        status = random.choice(course_statuses)
        
        # 缴费方式
        payment_method = random.choice(payment_methods)
        
        # 生成学员姓名
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


# ==================== 第二部分：数据处理 ====================

def process_data(df):
    """数据校验与修正"""
    
    # 计算正确的缴费总额
    df['计算缴费总额'] = df['报名节数/期数'] * df['单价']
    
    # 找出需要修正的记录
    df['需要修正'] = abs(df['缴费总额'] - df['计算缴费总额']) > 0.01
    
    # 记录修正信息
    corrections = df[df['需要修正']].copy()
    correction_records = []
    
    for idx, row in corrections.iterrows():
        correction_records.append({
            '学员ID': row['学员ID'],
            '修正前缴费总额': row['缴费总额'],
            '修正后缴费总额': row['计算缴费总额']
        })
    
    correction_df = pd.DataFrame(correction_records)
    
    # 修正缴费总额
    df['缴费总额'] = df['计算缴费总额']
    
    # 删除辅助列
    df = df.drop(['计算缴费总额', '需要修正'], axis=1)
    
    return df, correction_df


def generate_monthly_summary(df):
    """生成月度聚合汇总表"""
    
    # 提取月份
    df['缴费月份'] = pd.to_datetime(df['缴费日期']).dt.to_period('M').astype(str)
    
    # 表1：月度-课程类别-缴费总额汇总表
    summary_by_category = df.groupby(['缴费月份', '课程类别'])['缴费总额'].sum().reset_index()
    summary_by_category.columns = ['月份', '课程类别', '缴费总额']
    summary_by_category = summary_by_category.sort_values(['月份', '缴费总额'], ascending=[True, False])
    
    # 表2：月度-学员所在城市-缴费总额汇总表
    summary_by_city = df.groupby(['缴费月份', '学员所在城市'])['缴费总额'].sum().reset_index()
    summary_by_city.columns = ['月份', '城市', '缴费总额']
    summary_by_city = summary_by_city.sort_values(['月份', '缴费总额'], ascending=[True, False])
    
    return summary_by_category, summary_by_city


# ==================== 第三部分：统计分析 ====================

def calculate_dimension_ratios(df):
    """计算各维度占比"""
    
    total_amount = df['缴费总额'].sum()
    
    # 城市占比
    city_stats = df.groupby('学员所在城市')['缴费总额'].sum().reset_index()
    city_stats['占比(%)'] = (city_stats['缴费总额'] / total_amount * 100).round(2)
    city_stats = city_stats.sort_values('缴费总额', ascending=False)
    city_stats['累计占比(%)'] = city_stats['占比(%)'].cumsum().round(2)
    
    # 课程类别占比
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
    
    # 计算退费相关指标
    refund_amount = status_stats[status_stats['课程状态'] == '已退费']['缴费总额'].sum() if '已退费' in status_stats['课程状态'].values else 0
    refund_ratio = (refund_amount / total_amount * 100).round(2)
    
    return status_stats, refund_amount, refund_ratio


def analyze_city_per_capita(df):
    """城市人均缴费分析"""
    
    # 按学员ID去重统计各城市学员数量
    city_students = df.groupby('学员所在城市')['学员ID'].nunique().reset_index()
    city_students.columns = ['城市', '学员数量']
    
    # 各城市缴费总额
    city_amount = df.groupby('学员所在城市')['缴费总额'].sum().reset_index()
    city_amount.columns = ['城市', '缴费总额']
    
    # 合并计算人均缴费
    city_per_capita = pd.merge(city_amount, city_students, on='城市')
    city_per_capita['人均缴费(元)'] = (city_per_capita['缴费总额'] / city_per_capita['学员数量']).round(2)
    city_per_capita = city_per_capita.sort_values('人均缴费(元)', ascending=False)
    
    return city_per_capita


# ==================== 第四部分：输出结果 ====================

def output_to_csv(df, correction_df, summary_by_category, summary_by_city,
                  city_stats, category_stats, top3, course_stats, 
                  status_stats, refund_amount, refund_ratio, city_per_capita):
    """输出所有结果到CSV文件"""
    
    # 1. 修正后的学员缴费数据表
    df.to_csv('修正后的学员缴费数据表.csv', index=False, encoding='utf-8-sig')
    
    # 2. 修正记录表
    if len(correction_df) > 0:
        correction_df.to_csv('数据修正记录表.csv', index=False, encoding='utf-8-sig')
    
    # 3. 月度汇总表
    summary_by_category.to_csv('月度课程类别缴费汇总表.csv', index=False, encoding='utf-8-sig')
    summary_by_city.to_csv('月度城市缴费汇总表.csv', index=False, encoding='utf-8-sig')
    
    # 4. 统计分析结果
    city_stats.to_csv('城市缴费占比分析表.csv', index=False, encoding='utf-8-sig')
    category_stats.to_csv('课程类别缴费占比分析表.csv', index=False, encoding='utf-8-sig')
    top3.to_csv('TOP3热门课程分析表.csv', index=False, encoding='utf-8-sig')
    course_stats.to_csv('全部课程缴费统计表.csv', index=False, encoding='utf-8-sig')
    status_stats.to_csv('课程状态分析表.csv', index=False, encoding='utf-8-sig')
    city_per_capita.to_csv('城市人均缴费分析表.csv', index=False, encoding='utf-8-sig')
    
    # 5. 生成分析报告文本
    with open('游泳馆缴费数据分析报告.txt', 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("游泳馆学员缴费数据分析报告\n")
        f.write("数据时间范围：2025-09-01 至 2026-02-28\n")
        f.write("=" * 80 + "\n\n")
        
        # 数据修正记录
        f.write("【一、数据修正记录】\n")
        f.write("-" * 80 + "\n")
        if len(correction_df) > 0:
            f.write(f"共发现 {len(correction_df)} 条记录需要修正\n\n")
            for idx, row in correction_df.iterrows():
                f.write(f"学员ID: {row['学员ID']}\n")
                f.write(f"  修正前缴费总额: {row['修正前缴费总额']:.2f} 元\n")
                f.write(f"  修正后缴费总额: {row['修正后缴费总额']:.2f} 元\n\n")
        else:
            f.write("未发现需要修正的记录，所有数据计算准确。\n\n")
        
        # 城市占比分析
        f.write("\n【二、城市缴费占比分析】\n")
        f.write("-" * 80 + "\n")
        f.write(f"{'城市':<10} {'缴费总额':>15} {'占比(%)':>12} {'累计占比(%)':>15}\n")
        f.write("-" * 80 + "\n")
        for idx, row in city_stats.iterrows():
            f.write(f"{row['学员所在城市']:<10} {row['缴费总额']:>15.2f} {row['占比(%)']:>12.2f} {row['累计占比(%)']:>15.2f}\n")
        
        # 课程类别占比分析
        f.write("\n\n【三、课程类别缴费占比分析】\n")
        f.write("-" * 80 + "\n")
        f.write(f"{'课程类别':<12} {'缴费总额':>15} {'占比(%)':>12} {'累计占比(%)':>15}\n")
        f.write("-" * 80 + "\n")
        for idx, row in category_stats.iterrows():
            f.write(f"{row['课程类别']:<12} {row['缴费总额']:>15.2f} {row['占比(%)']:>12.2f} {row['累计占比(%)']:>15.2f}\n")
        
        # TOP3热门课程
        f.write("\n\n【四、TOP3热门课程分析】\n")
        f.write("-" * 80 + "\n")
        f.write(f"{'排名':<8} {'课程名称':<20} {'缴费总额':>15} {'贡献度(%)':>15}\n")
        f.write("-" * 80 + "\n")
        for idx, row in top3.iterrows():
            f.write(f"{row['排名']:<8} {row['课程名称']:<20} {row['缴费总额']:>15.2f} {row['贡献度(%)']:>15.2f}\n")
        
        # 课程状态分析
        f.write("\n\n【五、课程状态分析】\n")
        f.write("-" * 80 + "\n")
        f.write(f"{'课程状态':<12} {'缴费总额':>15} {'占比(%)':>12}\n")
        f.write("-" * 80 + "\n")
        for idx, row in status_stats.iterrows():
            f.write(f"{row['课程状态']:<12} {row['缴费总额']:>15.2f} {row['占比(%)']:>12.2f}\n")
        f.write("-" * 80 + "\n")
        f.write(f"已退费金额: {refund_amount:.2f} 元\n")
        f.write(f"退费占比: {refund_ratio:.2f}%\n")
        
        # 城市人均缴费分析
        f.write("\n\n【六、城市人均缴费分析】\n")
        f.write("-" * 80 + "\n")
        f.write(f"{'城市':<10} {'缴费总额':>15} {'学员数量':>12} {'人均缴费(元)':>15}\n")
        f.write("-" * 80 + "\n")
        for idx, row in city_per_capita.iterrows():
            f.write(f"{row['城市']:<10} {row['缴费总额']:>15.2f} {int(row['学员数量']):>12} {row['人均缴费(元)']:>15.2f}\n")
        
        # 可视化说明
        f.write("\n\n" + "=" * 80 + "\n")
        f.write("【七、可视化说明】\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("1. 折线图：展示「月度缴费总额趋势」\n")
        f.write("-" * 80 + "\n")
        f.write("【适用场景】\n")
        f.write("  ① 淡旺季营收波动监测：通过折线图直观呈现9月（开学季）、10月（国庆黄金周）\n")
        f.write("    、2月（寒假春节）等旺季与11-1月淡季的营收差异，帮助运营团队提前制定\n")
        f.write("    淡旺季促销策略和人员排班计划。\n")
        f.write("  ② 月度业绩目标追踪：将实际月度缴费额与预设业绩目标对比，及时发现业绩缺口，\n")
        f.write("    便于管理层在月中调整营销策略或加大推广力度。\n")
        f.write("  ③ 同比环比分析：结合去年同期数据，分析年度增长趋势，评估游泳馆品牌影响力和\n")
        f.write("    市场占有率的变化情况。\n\n")
        
        f.write("【业务价值】\n")
        f.write("  ① 精准预测现金流：基于历史月度趋势，财务部门可更准确地预测未来3-6个月的\n")
        f.write("    现金流入，合理安排场馆维护、教练薪资等支出，避免资金链紧张。\n")
        f.write("  ② 优化资源配置：根据月度缴费高峰和低谷，动态调整教练排班、泳池开放时段、\n")
        f.write("    客服人员数量，降低人力成本的同时提升服务体验。\n")
        f.write("  ③ 指导招生节奏：识别缴费高峰期后，可在高峰期前2-4周集中投放广告、开展体验\n")
        f.write("    课活动，最大化招生转化率，提升营销ROI。\n\n")
        
        f.write("\n2. 漏斗图：展示「学员所在城市→课程类别→课程状态」的缴费额分布\n")
        f.write("-" * 80 + "\n")
        f.write("【适用场景】\n")
        f.write("  ① 多层级转化分析：从城市维度（流量入口）→课程类别（产品选择）→课程状态\n")
        f.write("    （转化结果）三层漏斗，清晰展示从潜在市场到实际收入的完整转化路径，识别\n")
        f.write("    各层级的流失节点。\n")
        f.write("  ② 区域市场渗透评估：对比不同城市在漏斗各层级的表现，识别高潜力但渗透不足的\n")
        f.write("    城市，或发现某些城市在特定课程类别上的偏好差异。\n")
        f.write("  ③ 退费风险预警：在课程状态层级重点监控「已退费」占比，当某城市或某课程类别\n")
        f.write("    的退费比例异常升高时，及时介入调查原因（如教练问题、设施问题、服务问题）。\n\n")
        
        f.write("【业务价值】\n")
        f.write("  ① 精准定位运营瓶颈：通过漏斗各层级的转化率，快速定位问题环节。例如，若某\n")
        f.write("    城市缴费额高但「已结课」比例低，可能反映课程完成率低，需优化课程设计或\n")
        f.write("    加强学员跟进。\n")
        f.write("  ② 差异化营销策略制定：根据不同城市-课程类别的缴费分布，制定差异化的定价和\n")
        f.write("    推广策略。如一线城市主推高客单价私教课程，二三线城市主推性价比高的团课。\n")
        f.write("  ③ 退费管控与服务质量提升：通过漏斗末端的退费数据，追溯退费集中发生的城市和\n")
        f.write("    课程类型，针对性改进教学质量和服务流程，降低退费损失，提升学员满意度和口碑。\n")
        f.write("  ④ 新店选址与扩张决策：基于城市层级的缴费规模数据，评估各城市市场容量，为\n")
        f.write("    游泳馆连锁扩张、新店选址提供数据支撑，优先进入缴费规模大且增长快的城市。\n\n")
        
        f.write("=" * 80 + "\n")
        f.write("报告生成完毕\n")
        f.write("=" * 80 + "\n")


def print_summary_to_console(df, correction_df, summary_by_category, summary_by_city,
                             city_stats, category_stats, top3, status_stats, 
                             refund_amount, refund_ratio, city_per_capita):
    """在控制台打印汇总结果"""
    
    print("=" * 100)
    print("游泳馆学员缴费数据分析系统 - 结果汇总")
    print("数据时间范围：2025-09-01 至 2026-02-28")
    print("=" * 100)
    
    # 1. 数据修正记录
    print("\n【一、数据校验与修正记录】")
    print("-" * 100)
    if len(correction_df) > 0:
        print(f"共发现 {len(correction_df)} 条记录需要修正\n")
        print(correction_df.to_string(index=False))
    else:
        print("未发现需要修正的记录，所有数据计算准确。")
    
    # 2. 月度汇总表
    print("\n\n【二、月度-课程类别-缴费总额汇总表】")
    print("-" * 100)
    print(summary_by_category.to_string(index=False))
    
    print("\n\n【三、月度-学员所在城市-缴费总额汇总表】")
    print("-" * 100)
    print(summary_by_city.to_string(index=False))
    
    # 3. 统计分析
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
    print("所有结果已保存至CSV文件，详细分析报告已保存至「游泳馆缴费数据分析报告.txt」")
    print("=" * 100)


# ==================== 主程序入口 ====================

if __name__ == "__main__":
    print("正在生成游泳馆学员缴费数据...")
    df = generate_base_data()
    print(f"已生成 {len(df)} 条缴费记录")
    
    print("\n正在进行数据校验与修正...")
    df_corrected, correction_df = process_data(df)
    
    print("正在生成月度聚合汇总表...")
    summary_by_category, summary_by_city = generate_monthly_summary(df_corrected)
    
    print("正在进行统计分析...")
    city_stats, category_stats = calculate_dimension_ratios(df_corrected)
    top3, course_stats = get_top3_courses(df_corrected)
    status_stats, refund_amount, refund_ratio = analyze_course_status(df_corrected)
    city_per_capita = analyze_city_per_capita(df_corrected)
    
    print("正在输出结果...")
    output_to_csv(df_corrected, correction_df, summary_by_category, summary_by_city,
                  city_stats, category_stats, top3, course_stats, 
                  status_stats, refund_amount, refund_ratio, city_per_capita)
    
    print_summary_to_console(df_corrected, correction_df, summary_by_category, summary_by_city,
                            city_stats, category_stats, top3, status_stats, 
                            refund_amount, refund_ratio, city_per_capita)
