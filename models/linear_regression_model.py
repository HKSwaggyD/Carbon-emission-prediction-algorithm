from project_PricesPredict import unique_types, data
from sklearn.linear_model import LinearRegression
import numpy as np

""" 使用线性回归模型 """

# 初始化一个字典来保存每种类型的模型
models = {}

for green_type in unique_types:
    # 过滤当前类型的数据
    type_data = data[data['绿证类型'] == green_type]

    # 重塑年份数据以进行模型训练（sklearn 需要二维数组作为特征）
    X = type_data['年份'].values.reshape(-1, 1)
    y = type_data['平均价格（元/个）'].values

    # 创建并训练线性回归模型
    model = LinearRegression()
    model.fit(X, y)

    # 存储模型
    models[green_type] = model


# 定义一个函数来预测给定年份每种类型绿色证书的平均价格
def predict_green_certificate_prices(year):
    predictions = {}
    for green_type, model in models.items():
        # 预测并存储结果
        predicted_price = model.predict(np.array([[year]]))[0]
        predictions[green_type] = round(predicted_price, 2)

    return predictions


# 预测价格
lr_prices = predict_green_certificate_prices(2024)