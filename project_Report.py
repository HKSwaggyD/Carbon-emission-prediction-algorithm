import math

import project_ElectricalPrice as ep
import project_PricesPredict as pp

# 假设的电价数据
data = ep.electricity_data

# 已提供的电力成本计算函数
def calculate_electricity_cost(region, consumption, category, data):
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

# 假设的企业电量消耗数据
input_consumption = ep.input_consumption

# 假设的绿色证书预测购买价格
pp_future_forecast = pp.future_forecast

# 假设的企业所在地区
region = ep.region_example
category = '一般工商业'

# 计算不同类型电力的成本
costs = {type: calculate_electricity_cost(region, consumption, category, data)
         for type, consumption in input_consumption.items()}

# 打印初步计算结果，用于检查程序逻辑
print("各类型电力成本", costs)
print("\n--------------------------------------------------\n")

# 更新函数：计算包括绿色证书在内的电力总成本，并确保绿证数量为正整数
def calculate_total_cost(costs, pp_future_forecast, input_consumption):
    total_cost = 0
    advice_report = ""
    advice_greem_certs_amount = {}
    advice_total_prices = {}
    advice_after_discount = {}

    for type, cost in costs.items():
        if type in pp_future_forecast:
            # 计算绿色证书的成本（数量向上取整）
            green_certs = math.ceil(input_consumption[type] / 1000)  # 向上取整至最近的整数
            green_cert_cost = green_certs * pp_future_forecast[type]
            discounted_cost = cost - green_cert_cost

            # 添加建议信息
            advice_report += f"{type}：预测绿证价格 {pp_future_forecast[type]}元/个，"
            advice_report += f"需要购买 {green_certs} 个绿证，总费用 {green_cert_cost}元，"
            advice_greem_certs_amount[type] = green_certs
            advice_total_prices[type] = green_cert_cost
            advice_report += f"优惠后电力成本 {discounted_cost}元。\n"
            advice_after_discount[type] = discounted_cost

            # 更新总成本
            total_cost += max(discounted_cost, 0)  # 防止成本成为负数
        else:
            # 对于没有绿证的电力类型
            advice_report += f"{type}：无需购买绿证，电力成本 {cost}元。\n"
            total_cost += cost

    return total_cost, advice_report, advice_greem_certs_amount, advice_total_prices, advice_after_discount

# 再次运行更新后的程序以计算总成本和生成建议报告
total_cost, advice_report, advice_greem_certs_amount, advice_total_prices, advice_after_discount = calculate_total_cost(costs, pp_future_forecast, input_consumption)

print("优惠后电力成本：", total_cost, "元")
print(advice_report)
print("------------------------------------------------------\n")
print("需要购买绿证数量：\n", advice_greem_certs_amount)
print("各类绿证总费用：\n", advice_total_prices)
print("优惠后各类电力成本：\n", advice_after_discount)

# report = advice_report.split("\n")
# report.pop(-1)
# report_list = []
# for s in report:
#     item = s.split("：")[1]
#     report_list.append(item)
#
#
# print(report_list)


