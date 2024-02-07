import pandas as pd

# 加载Excel文件
file_path = '各省电价信息.xlsx'
electricity_data = pd.read_excel(file_path)

# 显示数据的前几行以了解其结构
print(electricity_data.head())

# 从后端接收的json输入数据，有地区和不同类型的用电量（单位：千瓦时）
input_consumption = {   #get_json_data(url)
    "地区": "湖南",
    "水电": 5000,
    "生物质": 3000,
    "光伏": 2000,
    "天然气": 4000,
    "火电": 10000,
    "风电": 2500
}

input_region = input_consumption["地区"]
input_consumption.pop("地区")
consumption = sum(input_consumption.values())

def calculate_electricity_cost(region, consumption, category, data):
    """
    考虑使用类别，计算给定区域的电力成本。

    :param region: 计算成本的区域。
    :param consumption: 消耗的电量（单位：千瓦时）。
    :param category: 使用类别（'大工业' 或 '一般工商业'）。
    :param data: 包含电价信息的DataFrame。
    :return: 指定区域和类别中给定消耗的电费。
    考虑使用类别，计算给定区域的电力成本。
    """
    if region in data['地区'].values:
        if category == '大工业':
            rate = data[data['地区'] == region]['大工业（元/千瓦时）'].iloc[0]
        elif category == '一般工商业':
            rate = data[data['地区'] == region]['一般工商业（元/千瓦时）'].iloc[0]
        else:
            return "未知的电价类型。"

        return rate * consumption
    else:
        return "未找到指定地区的电价信息。"

# 用法示例
region_example = input_region
consumption_example = consumption
category_example = "一般工商业"

prices = calculate_electricity_cost(region_example, consumption_example, category_example, electricity_data)
print("总用电成本：", prices, "元")