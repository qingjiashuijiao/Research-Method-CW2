import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

# 只保留四大组
df = df[df['diet_simple'].isin(['Vegan', 'Vegetarian', 'Fish-eater', 'Meat-eater'])]

# 颜色
colors = {
    'Vegan': '#4E9231',
    'Vegetarian': '#246068',
    'Fish-eater': '#AA7339',
    'Meat-eater': '#AA3C39'
}

# 要画的指标和标签
features = [
    ('mean_ghgs', 'GHG Emissions (kg)'),
    ('mean_land', 'Land Use (m²)'),
    ('mean_watscar', 'Water Scarcity'),
    ('mean_eut', 'Eutrophication Potential (g PO₄e)'),
    ('mean_bio', 'Biodiversity Impact'),
    ('mean_watuse', 'Water Usage (m³)'),
    ('mean_acid', 'Acidification Potential')
]

# 创建子图 (3行3列)
fig, axes = plt.subplots(3, 3, figsize=(18, 15))
axes = axes.flatten()

# 绘制每个箱线图
for i, (feature, label) in enumerate(features):
    sns.boxplot(
        x='diet_simple',
        y=feature,
        data=df,
        palette=colors,
        order=['Vegan', 'Vegetarian', 'Fish-eater', 'Meat-eater'],
        ax=axes[i]
    )
    axes[i].set_title(label, fontsize=14)
    axes[i].set_xlabel('')
    axes[i].set_ylabel('')

    # 横坐标标签保持水平
    axes[i].tick_params(axis='x', labelrotation=0, labelsize=10)
    axes[i].tick_params(axis='y', labelsize=10)

    # 保存每张单独小图
    single_fig, single_ax = plt.subplots(figsize=(6, 5))
    sns.boxplot(
        x='diet_simple',
        y=feature,
        data=df,
        palette=colors,
        order=['Vegan', 'Vegetarian', 'Fish-eater', 'Meat-eater'],
        ax=single_ax
    )
    single_ax.set_title(label, fontsize=14)
    single_ax.set_xlabel('')
    single_ax.set_ylabel('')
    single_ax.tick_params(axis='x', labelrotation=0, labelsize=10)
    single_ax.tick_params(axis='y', labelsize=10)
    plt.tight_layout()

    # 构建保存文件名
    safe_label = label.replace(" ", "_").replace("(", "").replace(")", "").replace("₄", "4").replace("₃", "3")
    single_fig.savefig(f'Boxplot_{safe_label}.svg', format='svg', dpi=300, bbox_inches='tight')
    single_fig.savefig(f'Boxplot_{safe_label}.png', format='png', dpi=300, bbox_inches='tight')
    plt.close(single_fig)  # 关闭小图，避免内存累积

# 删除空白子图
for j in range(len(features), len(axes)):
    fig.delaxes(axes[j])

# 全局标题
fig.suptitle('Environmental Impact Indicators by Diet Group', fontsize=24, y=1.02)

# 自动调整子图间距
plt.tight_layout()

# 保存大合成图
fig.savefig('Combined_Boxplots_Diet_Groups.svg', format='svg', dpi=300, bbox_inches='tight')
fig.savefig('Combined_Boxplots_Diet_Groups.png', format='png', dpi=300, bbox_inches='tight')

# 展示
plt.show()