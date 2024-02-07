from project_PricesPredict import unique_types, data
from statsmodels.tsa.holtwinters import SimpleExpSmoothing

""" 使用指数平滑模型 """

# 初始化一个字典，保存每种绿证的模型
exp_smoothing_models = {}

for green_type in unique_types:
    # 过滤当前类型的数据
    type_data = data[data['绿证类型'] == green_type].sort_values(by='年份')

    # 仅使用'年份'和'平均价格（元/个）'列
    series = type_data.set_index('年份')['平均价格（元/个）']

    # 拟合简单指数平滑模型
    try:
        model = SimpleExpSmoothing(series, initialization_method="estimated")
        fitted_model = model.fit()
        exp_smoothing_models[green_type] = fitted_model
    except:
        exp_smoothing_models[green_type] = None

# 使用指数平滑模型进行预测的函数
def predict_green_certificate_prices(year):
    predictions = {}
    for green_type, model in exp_smoothing_models.items():
        if model:
            # 预测
            forecast_years = list(range(data['年份'].max() + 1, year + 1))
            forecast = model.forecast(len(forecast_years))
            predicted_price = forecast[-1]
            predictions[green_type] = max(0, round(predicted_price, 2))  # 确保价格不为负数
        else:
            predictions[green_type] = "Model not available"

    return predictions

# 预测价格
exp_prices = predict_green_certificate_prices(2024)