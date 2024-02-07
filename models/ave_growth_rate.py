from project_PricesPredict import unique_types, data

""" 使用平均增长率的简单方法 """

def calculate_average_growth_rate(series):
    # 计算一个系列的平均增长率
    growth_rates = series.pct_change().dropna()
    average_growth_rate = growth_rates.mean()
    return average_growth_rate


# 计算每种类型的平均增长率并预测未来价格
def predict_green_certificate_prices(year):
    predictions = {}
    for green_type in unique_types:
        # 过滤当前类型的数据
        type_data = data[data['绿证类型'] == green_type].sort_values(by='年份')

        # 仅使用'年份'和'平均价格（元/个）'列
        series = type_data.set_index('年份')['平均价格（元/个）']

        # 计算平均增长率
        avg_growth_rate = calculate_average_growth_rate(series)

        # 计算预测价格
        last_price = series.iloc[-1]
        years_to_predict = year - series.index[-1]
        predicted_price = last_price * ((1 + avg_growth_rate) ** years_to_predict)

        # 确保预测价格不为负数
        predictions[green_type] = max(0, round(predicted_price, 2))

    return predictions


# 预测价格
ave_prices = predict_green_certificate_prices(2024)