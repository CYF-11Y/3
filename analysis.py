import pandas as pd
import numpy as np

df = pd.read_csv('游泳学员缴费数据.csv', encoding='utf-8')

print("=" * 80)
print("一、数据处理")
print("=" * 80)

print("\n【1. 数据校验与修正】")
df['应缴金额'] = df['缴费数量'] * df['单价']
df['金额差异'] = df['缴费金额'] - df['应缴金额']
corrections = df[df['金额差异'] != 0].copy()

print("\n" + "-" * 60)
print("数据修正记录表")
print("-" * 60)

if len(corrections) > 0:
    correction_records = []
    for idx, row in corrections.iterrows():
        correction_records.append({
            '学员ID': row['用户ID'],
            '订单ID': row['订单ID'],
            '课程名称': row['课程名称'],
            '缴费数量': row['缴费数量'],
            '单价(元)': row['单价'],
            '修正前缴费总额(元)': row['缴费金额'],
            '修正后缴费总额(元)': row['应缴金额'],
            '差异金额(元)': row['金额差异']
        })
    correction_df = pd.DataFrame(correction_records)
    print(f"\n发现 {len(correction_df)} 条缴费总额计算偏差记录：\n")
    print(correction_df.to_string(index=False))
    correction_df.to_csv('数据修正记录表.csv', index=False, encoding='utf-8-sig')
    print("\n修正记录已保存至: 数据修正记录表.csv")
else:
    print("\n所有记录缴费总额计算正确，无需修正。")
    print("\n数据修正记录表（空表）：")
    empty_df = pd.DataFrame(columns=['学员ID', '修正前缴费总额(元)', '修正后缴费总额(元)'])
    print(empty_df.to_string(index=False))

df['缴费金额_修正后'] = df['应缴金额']

print("\n【2. 修正后的完整数据表】")
output_df = df[['订单ID', '用户ID', '课程名称', '课程类目', '缴费数量', '单价', '缴费金额', '缴费金额_修正后', '缴费日期', '学员省份', '支付方式', '缴费状态']].copy()
output_df.columns = ['订单ID', '用户ID', '课程名称', '课程类目', '缴费数量', '单价', '原缴费金额', '修正后缴费金额', '缴费日期', '学员省份', '支付方式', '缴费状态']
print(f"\n共 {len(output_df)} 条记录，修正后数据表（前10条预览）：")
print(output_df.head(10).to_string(index=False))
output_df.to_csv('修正后学员缴费数据.csv', index=False, encoding='utf-8-sig')
print("\n完整修正后数据已保存至: 修正后学员缴费数据.csv")

print("\n【3. 月度聚合汇总表】")
df['缴费月份'] = pd.to_datetime(df['缴费日期']).dt.strftime('%Y-%m')

print("\n" + "-" * 60)
print("汇总表1：月度-课程类别-缴费总额")
print("-" * 60)
monthly_category = df.groupby(['缴费月份', '课程类目'])['缴费金额_修正后'].sum().reset_index()
monthly_category.columns = ['月份', '课程类别', '缴费总额(元)']
monthly_category['缴费总额(元)'] = monthly_category['缴费总额(元)'].round(2)
monthly_category = monthly_category.sort_values(['月份', '课程类别'])
print(monthly_category.to_string(index=False))
monthly_category.to_csv('月度课程类别汇总表.csv', index=False, encoding='utf-8-sig')

print("\n" + "-" * 60)
print("汇总表2：月度-学员所在城市-缴费总额")
print("-" * 60)
monthly_city = df.groupby(['缴费月份', '学员省份'])['缴费金额_修正后'].sum().reset_index()
monthly_city.columns = ['月份', '城市', '缴费总额(元)']
monthly_city['缴费总额(元)'] = monthly_city['缴费总额(元)'].round(2)
monthly_city = monthly_city.sort_values(['月份', '城市'])
print(monthly_city.to_string(index=False))
monthly_city.to_csv('月度城市汇总表.csv', index=False, encoding='utf-8-sig')

print("\n" + "=" * 80)
print("二、统计分析")
print("=" * 80)

total_amount = df['缴费金额_修正后'].sum()
print(f"\n总缴费额: {total_amount:,.2f} 元")

print("\n" + "-" * 60)
print("表1：各城市缴费额占比分析表")
print("-" * 60)
city_amount = df.groupby('学员省份')['缴费金额_修正后'].sum().reset_index()
city_amount.columns = ['城市', '缴费总额(元)']
city_amount['缴费总额(元)'] = city_amount['缴费总额(元)'].round(2)
city_amount['占比(%)'] = (city_amount['缴费总额(元)'] / total_amount * 100).round(2)
city_amount = city_amount.sort_values('缴费总额(元)', ascending=False)
city_amount['排名'] = range(1, len(city_amount) + 1)
city_amount = city_amount[['排名', '城市', '缴费总额(元)', '占比(%)']]
print(city_amount.to_string(index=False))

print("\n" + "-" * 60)
print("表2：各课程类别缴费额占比分析表")
print("-" * 60)
category_amount = df.groupby('课程类目')['缴费金额_修正后'].sum().reset_index()
category_amount.columns = ['课程类别', '缴费总额(元)']
category_amount['缴费总额(元)'] = category_amount['缴费总额(元)'].round(2)
category_amount['占比(%)'] = (category_amount['缴费总额(元)'] / total_amount * 100).round(2)
category_amount = category_amount.sort_values('缴费总额(元)', ascending=False)
category_amount['排名'] = range(1, len(category_amount) + 1)
category_amount = category_amount[['排名', '课程类别', '缴费总额(元)', '占比(%)']]
print(category_amount.to_string(index=False))

print("\n" + "-" * 60)
print("表3：TOP3热门课程及贡献度分析表")
print("-" * 60)
course_amount = df.groupby('课程名称')['缴费金额_修正后'].sum().reset_index()
course_amount.columns = ['课程名称', '缴费总额(元)']
course_amount['缴费总额(元)'] = course_amount['缴费总额(元)'].round(2)
course_amount['贡献度(%)'] = (course_amount['缴费总额(元)'] / total_amount * 100).round(2)
course_amount = course_amount.sort_values('缴费总额(元)', ascending=False)
course_amount['排名'] = range(1, len(course_amount) + 1)
top3 = course_amount.head(3)[['排名', '课程名称', '缴费总额(元)', '贡献度(%)']]
print(top3.to_string(index=False))

print("\n" + "-" * 60)
print("表4：课程状态分析表")
print("-" * 60)
status_amount = df.groupby('缴费状态')['缴费金额_修正后'].sum().reset_index()
status_amount.columns = ['课程状态', '缴费总额(元)']
status_amount['缴费总额(元)'] = status_amount['缴费总额(元)'].round(2)
status_amount['占比(%)'] = (status_amount['缴费总额(元)'] / total_amount * 100).round(2)
status_amount = status_amount.sort_values('缴费总额(元)', ascending=False)
status_amount['排名'] = range(1, len(status_amount) + 1)
status_amount = status_amount[['排名', '课程状态', '缴费总额(元)', '占比(%)']]
print(status_amount.to_string(index=False))

refund_total = df[df['缴费状态'] == '已退款']['缴费金额_修正后'].sum()
refund_rate = refund_total / total_amount * 100
print(f"\n退费专项分析：已退费总额 = {refund_total:,.2f} 元，退费占比 = {refund_rate:.2f}%")

print("\n退费高发课程分析表：")
refund_by_course = df[df['缴费状态'] == '已退款'].groupby('课程名称')['缴费金额_修正后'].agg(['sum', 'count']).reset_index()
refund_by_course.columns = ['课程名称', '退费金额(元)', '退费订单数']
refund_by_course['退费金额(元)'] = refund_by_course['退费金额(元)'].round(2)
refund_by_course = refund_by_course.sort_values('退费金额(元)', ascending=False)
print(refund_by_course.to_string(index=False))

print("\n" + "-" * 60)
print("表5：城市人均缴费分析表")
print("-" * 60)
city_stats = df.groupby('学员省份').agg({
    '用户ID': 'nunique',
    '缴费金额_修正后': 'sum'
}).reset_index()
city_stats.columns = ['城市', '学员数(人)', '总缴费额(元)']
city_stats['总缴费额(元)'] = city_stats['总缴费额(元)'].round(2)
city_stats['人均缴费额(元)'] = (city_stats['总缴费额(元)'] / city_stats['学员数(人)']).round(2)
city_stats = city_stats.sort_values('人均缴费额(元)', ascending=False)
city_stats['排名'] = range(1, len(city_stats) + 1)
city_stats = city_stats[['排名', '城市', '学员数(人)', '总缴费额(元)', '人均缴费额(元)']]
print(city_stats.to_string(index=False))

print("\n" + "=" * 80)
print("三、可视化说明")
print("=" * 80)

print("""
【1. 月度缴费总额趋势折线图】

适用场景：
(1) 季节性运营分析：游泳馆经营具有明显的季节性特征，折线图可直观展示旺季（如暑期前后、
    寒假期间）与淡季的缴费波动，帮助运营团队识别业务周期规律，合理安排教练排班、泳池
    维护等资源调度，避免旺季人手不足或淡季资源闲置。

(2) 招生推广效果追踪：当游泳馆推出新课程或促销活动后，通过折线图观察月度缴费趋势变化，
    可快速评估营销活动的实际转化效果，对比活动前后缴费额增幅，为后续推广策略调整提供
    数据支撑，优化营销预算分配。

(3) 营收目标达成监控：将月度实际缴费额与预算目标线叠加展示，形成"实际vs目标"双线对比，
    便于管理层实时掌握营收进度，及时发现业绩偏差并采取应对措施，支撑月度经营复盘会议。

业务价值：
(1) 资源配置优化：根据缴费趋势预判未来学员流量，合理调配教练资源、泳池时段安排，降低
    运营成本，提升服务效率。

(2) 现金流管理：月度缴费趋势直接反映游泳馆现金流入节奏，帮助财务部门做好资金规划，
    确保淡季期间有充足资金覆盖固定成本支出，维持财务稳健。

(3) 战略决策支持：长期趋势数据可揭示市场变化规律，为年度经营计划制定、新馆选址、课程
    定价调整等重大决策提供量化依据。

【2. 城市→课程类别→课程状态漏斗图】

适用场景：
(1) 招生渠道优化：从城市维度出发，漏斗图第一层清晰展示各城市的缴费贡献占比，识别核心
    市场（如河北、重庆缴费额排名前列）与潜力市场，为区域招生资源投放、广告投放策略
    提供精准指导，提升营销ROI。

(2) 课程结构分析：在城市细分基础上，第二层展示不同课程类别的缴费分布，帮助运营团队
    了解各城市学员的课程偏好差异，实现课程供给与市场需求的精准匹配，优化课程开设比例。

(3) 服务质量监控：最终层级的课程状态分布可直观呈现已支付、已退款、部分退款等状态占比，
    快速识别退费高发环节，定位服务短板，推动课程质量和服务体验持续改进。

业务价值：
(1) 精准营销投放：通过城市→课程类别的层层下钻，可识别高价值城市-课程组合，将有限的
    市场推广预算集中投放在转化率最高的区域和课程，避免资源浪费。

(2) 课程优化决策：漏斗图可清晰展示各课程类别的缴费流向及最终状态，发现哪些课程虽然
    报名量大但退费率高，为课程内容优化、教练培训、服务流程改进指明方向。

(3) 风险预警机制：当某一城市或课程类别的退费占比异常升高时，漏斗图可快速定位问题源头，
    便于管理层及时介入调查，防范声誉风险和财务损失，维护品牌形象。
""")

print("\n" + "=" * 80)
print("分析完成！")
print("=" * 80)
print("\n生成的文件列表：")
print("  1. 数据修正记录表.csv")
print("  2. 修正后学员缴费数据.csv")
print("  3. 月度课程类别汇总表.csv")
print("  4. 月度城市汇总表.csv")
