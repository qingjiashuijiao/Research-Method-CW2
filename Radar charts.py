import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 读取数据
df = pd.read_csv('Results_21Mar2022.csv')

# 简化 diet_group
def simplify_diet(diet):
    if diet == 'vegan':
        return 'Vegan'
    elif diet == 'veggie':
        return 'Vegetarian'
    elif diet in ['meat', 'meat50', 'meat100']:
        return 'Meat-eater'
    elif diet == 'fish':
        return 'Fish-eater'
    else:
        return 'Other'

df['diet_simple'] = df['diet_group'].apply(simplify_diet)

# 只保留四大饮食组
df = df[df['diet_simple'].isin(['Vegan', 'Vegetarian', 'Fish-eater', 'Meat-eater'])]

# 选特征
features = [
    'mean_ghgs',
    'mean_land',
    'mean_watscar',
    'mean_eut',
    'mean_bio',
    'mean_watuse',
    'mean_acid'
]

# 人性化标签
feature_labels = [
    'GHG Emissions',
    'Land Use',
    'Water Scarcity',
    'Eutrophication Potential',
    'Biodiversity Impact',
    'Water Usage',
    'Acidification Potential'
]

# 按 diet_simple 分组求均值
grouped = df.groupby('diet_simple')[features].mean()

# 正确归一化（第一张图用）：对每列单独归一化
grouped_normalized = grouped.apply(lambda x: (x - x.min()) / (x.max() - x.min()), axis=0)

# 配色
colors = {
    'Vegan': '#4E9231',        # 绿色
    'Vegetarian': '#246068',   # 蓝色
    'Fish-eater': '#AA7339',   # 橙色
    'Meat-eater': '#AA3C39'    # 红色
}

# ========== 第一张图：四组对比 ==========

labels = feature_labels
num_vars = len(labels)
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angles += angles[:1]

fig1, ax1 = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))

for diet in ['Vegan', 'Vegetarian', 'Fish-eater', 'Meat-eater']:
    values = grouped_normalized.loc[diet].tolist()
    values += values[:1]
    ax1.plot(angles, values, label=diet, color=colors[diet], linewidth=2.5)
    ax1.fill(angles, values, alpha=0.2, color=colors[diet])
    ax1.scatter(angles, values, color=colors[diet], s=60, edgecolors='black', zorder=10)

ax1.set_theta_offset(np.pi / 2)
ax1.set_theta_direction(-1)
ax1.set_thetagrids(np.degrees(angles[:-1]), labels, fontsize=12)

ax1.set_rlabel_position(0)
ax1.yaxis.set_tick_params(labelsize=10)
plt.yticks([0.2, 0.4, 0.6, 0.8], ["0.2", "0.4", "0.6", "0.8"])
plt.ylim(0, 1)

legend = plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), title='Diet Group', fontsize=12, title_fontsize='13')
for text, diet in zip(legend.get_texts(), ['Vegan', 'Vegetarian', 'Fish-eater', 'Meat-eater']):
    text.set_color(colors[diet])

plt.title('Environmental Impact by Diet Group', size=22, y=1.15)
plt.tight_layout()

# 保存图
fig1.savefig('Radar_Chart_All_Diets.svg', format='svg', dpi=300, bbox_inches='tight')
fig1.savefig('Radar_Chart_All_Diets.png', format='png', dpi=300, bbox_inches='tight')
