from project_PricesPredict import unique_types, data
from statsmodels.tsa.arima.model import ARIMA
import warnings

""" 使用ARIMA模型 """

# 由于 ARIMA 模型拟合会生成大量警告，为了清楚起见，我们将抑制它们
warnings.filterwarnings("ignore")

# 检查平稳性并在需要时应用差分的函数
def make_stationary(series):
    from statsmodels.tsa.stattools import adfuller
    result = adfuller(series)
    p_value = result[1]

    # 如果 p 值大于 0.05，可认为该序列是非平稳的
    if p_value > 0.05:
        # 应用差分
        series_diff = series.diff().dropna()
        return series_diff
    else:
        return series

# 初始化一个字典来保存每种类型的ARIMA模型
arima_models = {}

for green_type in unique_types:
    # 过滤当前类型的数据
    type_data = data[data['绿证类型'] == green_type].sort_values(by='年份')

    # 仅使用'年份'和'平均价格（元/个）'列
    series = type_data.set_index('年份')['平均价格（元/个）']

    # 如果需要，使序列平稳
    series_stationary = make_stationary(series)

    # 拟合ARIMA模型（使用自动ARIMA寻找最优参数）
    try:
        model = ARIMA(series_stationary, order=(1,1,1))
        arima_model = model.fit()
        arima_models[green_type] = arima_model
    except:
        arima_models[green_type] = None

# 使用ARIMA模型进行预测的函数
def predict_green_certificate_prices(year):
    predictions = {}
    for green_type, model in arima_models.items():
        if model:
            # 预测
            forecast = model.get_forecast(steps=year - data['年份'].max())
            predicted_price = forecast.predicted_mean[-1]
            predictions[green_type] = max(0, round(predicted_price, 2))  # 价格不能为负数
        else:
            predictions[green_type] = "Model not available"

    return predictions

# 预测价格
ari_prices = predict_green_certificate_prices(2024)