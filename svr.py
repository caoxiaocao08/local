#!/usr/bin/env python
# coding: utf-8

"""
作者：胖哥
微信公众号：胖哥真不错
"""

import numpy as np
import pandas as pd
import seaborn as sns
from numpy import sqrt
from sklearn import metrics
import matplotlib.pyplot as plt
import matplotlib
from sklearn import svm

# 读取数据
df = pd.read_excel('data.xlsx')

# 数据预处理
# 用Pandas工具查看数据

print('*************df.head()*****************')
print(df.head())

# 查看数据的形状
print('*************df.shape*****************')
print(df.shape)

# 变量的空值情况判断
print('*************df.isnull().sum()*****************')
print(df.isnull().sum())

# 数据描述性统计分析
print('*************df.describe().round(2)*****************')
print(df.describe().round(2))

# 数据摘要信息查看
print('*************df.info()*****************')
print(df.info())

# 删除和重命名数据项
df = df.drop(['Unnamed: 0'], axis=1)

df['Date'] = pd.to_datetime(df.Date)
df.sort_values(by=['Date'], inplace=True, ascending=True)

print('*************df.head()*****************')
print(df.head())

# 随时间推移的Conventional Avocados的平均价格

mask = df['type'] == 'conventional'
plt.rc('figure', titlesize=50)
fig = plt.figure(figsize=(26, 7))
fig.suptitle('Average Price of Conventional Avocados Over Time', fontsize=25)
ax = fig.add_subplot(111)
fig.subplots_adjust(top=0.93)

dates = df[mask]['Date'].tolist()
avgPrices = df[mask]['AveragePrice'].tolist()

plt.scatter(dates, avgPrices, c=avgPrices, cmap='plasma')
ax.set_xlabel('Date', fontsize=15)
ax.set_ylabel('Average Price (USD)', fontsize=15)
plt.show()

# 随时间推移的Organic Avocados的平均价格

mask = df['type'] == 'organic'
plt.rc('figure', titlesize=50)
fig = plt.figure(figsize=(26, 7))
fig.suptitle('Average Price of Organic Avocados Over Time', fontsize=25)
ax = fig.add_subplot(111)
fig.subplots_adjust(top=0.93)

dates = df[mask]['Date'].tolist()
avgPrices = df[mask]['AveragePrice'].tolist()

plt.scatter(dates, avgPrices, c=avgPrices, cmap='plasma')
ax.set_xlabel('Date', fontsize=15)
ax.set_ylabel('Average Price (USD)', fontsize=15)
plt.show()

# 创建只有2个数据项的数据集：Date  AveragePrice

df2 = df[['Date', 'AveragePrice']]
df2 = df2.set_index('Date')

weekly_df = df2.resample('W').mean()
w_df = weekly_df.reset_index().dropna()

w_df.sort_values(by=['Date'])
print('*************w_df.head()*****************')
print(w_df.head())

# 按月画出每周的平均价格

import matplotlib.dates as mdates

fig = plt.figure(figsize=(27, 7))
ax = plt.axes()
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
plt.plot(w_df['Date'], w_df['AveragePrice'], color='b', linewidth=1, label='AveragePrice')
plt.xlabel("2015-2018")
plt.ylabel("Avocado Price USD")
plt.legend()
plt.show()

# 删掉日期字段
df = df.drop(['Date'], axis=1)

# 检查样本集是否均衡
print('*************df.groupby("region").size()*****************')
print(df.groupby('region').size())

print('*************len(df.region.unique())*****************')
print(len(df.region.unique()))

print('*************df.region.unique()*****************')
print(df.region.unique())

regionsToRemove = ['California', 'GreatLakes', 'Midsouth', 'NewYork', 'Northeast', 'SouthCarolina', 'Plains',
                   'SouthCentral', 'Southeast', 'TotalUS', 'West']
df = df[~df.region.isin(regionsToRemove)]
print('*************len(df.region.unique())*****************')
print(len(df.region.unique()))

# 按地区进行平均价格展示

plt.figure(figsize=(10, 11))
plt.title("Avg.Price of Avocado by Region")
Av = sns.barplot(x="AveragePrice", y="region", data=df)
plt.show()
type_counts = df.groupby('type').size()
print('*************type_counts*****************')
print(type_counts)

# 按类型进行平均价格展示

plt.figure(figsize=(5, 7))
plt.title("Avg.Price of Avocados by Type")
Av1 = sns.barplot(x="type", y="AveragePrice", data=df)
plt.show()

# 相关性分析
df_tmp = df[["Small Hass", "Large Hass", "XLarge Hass", 'Small Bags', 'Large Bags', 'XLarge Bags', 'Total Volume',
             'Total Bags']]

plt.figure(figsize=(12, 6))
sns.heatmap(df_tmp.corr(), cmap='coolwarm', annot=True)
plt.show()

df_V = df.drop(['AveragePrice', 'Total Volume', 'Total Bags'], axis=1).groupby('year').agg('sum')
print('*************df_V*****************')
print(df_V.head())

# 绘制饼图
indexes = ['Small Hass', 'Large Hass', 'XLarge Hass', 'Small Bags', 'Large Bags', 'XLarge Bags']
series = pd.DataFrame({'2015': df_V.loc[[2015], :].values.tolist()[0],
                       '2016': df_V.loc[[2016], :].values.tolist()[0],
                       '2017': df_V.loc[[2017], :].values.tolist()[0],
                       '2018': df_V.loc[[2018], :].values.tolist()[0]}, index=indexes)
series.plot.pie(y='2015', figsize=(9, 9), autopct='%1.1f%%',
                colors=['silver', 'pink', 'orange', 'palegreen', 'aqua', 'blue'], fontsize=18, legend=False,
                title='2015 Volume Distribution').set_ylabel('')
plt.show()
series.plot.pie(y='2016', figsize=(9, 9), autopct='%1.1f%%',
                colors=['silver', 'pink', 'orange', 'palegreen', 'aqua', 'blue'], fontsize=18, legend=False,
                title='2016 Volume Distribution').set_ylabel('')
plt.show()
series.plot.pie(y='2017', figsize=(9, 9), autopct='%1.1f%%',
                colors=['silver', 'pink', 'orange', 'palegreen', 'aqua', 'blue'], fontsize=18, legend=False,
                title='2017 Volume Distribution').set_ylabel('')
plt.show()
series.plot.pie(y='2018', figsize=(9, 9), autopct='%1.1f%%',
                colors=['silver', 'pink', 'orange', 'palegreen', 'aqua', 'blue'], fontsize=18, legend=False,
                title='2018 Volume Distribution').set_ylabel('')
plt.show()

# Total Bags = Small Bags + Large Bags + XLarge Bags

df = df.drop(['Total Bags'], axis=1)

df = df.drop(['Total Volume'], axis=1)

print('*************df.info()*****************')
print(df.info())

# 查看数据预处理后的数据相关性
pd.set_option('display.width', 100)
pd.set_option('precision', 3)
correlations = df.corr(method='pearson')
print('*************correlations*****************')
print(correlations)  # 查看相关性

# 数据标准化

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
df.loc[:, 'Small Hass':'XLarge Bags'] = scaler.fit_transform(df.loc[:, 'Small Hass':'XLarge Bags'])
print('*************df.head()*****************')
print(df.head())

# 建立特征数据和标签数据

X = df.drop(['AveragePrice'], axis=1)
y = df['AveragePrice']
y = np.log1p(y)

# 哑特征处理

Xcat = pd.get_dummies(X[["type", "region"]], drop_first=True)

Xnum = X[["Small Hass", "Large Hass", "XLarge Hass", "Small Bags", "Large Bags", "XLarge Bags"]]

X = pd.concat([Xcat, Xnum], axis=1)
print('*************X.shape*****************')
print(X.shape)

F_DF = pd.concat([y, X], axis=1)
print('*************F_DF.head(2)*****************')
print(F_DF.head(2))

# 可视化与平均价格变量高度相关的变量

import seaborn as sns

sns.set(color_codes=True)
sns.jointplot(x="Small Hass", y="AveragePrice", data=F_DF, kind="reg")
plt.show()
sns.jointplot(x="Small Bags", y="AveragePrice", data=F_DF, kind="reg")
plt.show()
sns.jointplot(x="Large Bags", y="AveragePrice", data=F_DF, kind="reg")
plt.show()

sns.lmplot(x="Small Hass", y="AveragePrice", col="type_organic", data=F_DF, col_wrap=2)
plt.show()

# 数据集拆分


X_train = X[0:10172]
y_train = y[0:10172]
X_test = X[10172:]
y_test = y[10172:]

# 构建SVR回归模型

from sklearn.svm import SVR

# 通过for循环来选择最好的核函数

for k in ['linear', 'poly', 'rbf', 'sigmoid']:
    clf = svm.SVR(kernel=k)
    clf.fit(X_train, y_train)
    confidence = clf.score(X_train, y_train)
    print('*************k, confidence*****************')
    print(k, confidence)

# 建模
Svr = SVR(kernel='rbf', C=1, gamma=0.5)

Svr.fit(X_train, y_train)  # 拟合

y_pred = Svr.predict(X_test)  # 预测

# 模型评估
print('分数：', Svr.score(X_train, y_train))  # 分数

error = sqrt(metrics.mean_squared_error(y_test, y_pred))  # 计算 rmse
print('均方根误差RMSE: ', error)

print('均方误差MSE：{}'.format(
    round(metrics.mean_squared_error(y_test, y_pred), 2)))  # 打印模型的均方误差数值
print('解释方差分：{}'.format(
    round(metrics.explained_variance_score(y_test, y_pred), 2)))  # 打印模型的解释性方差数值
print('R平方得分：{}'.format(
    round(metrics.r2_score(y_test, y_pred), 2)))  # 打印模型的R平方数值

# 真实值与测试值比对图
x = np.arange(0, 120, 1)
y1 = y_pred[0:120]
y2 = y_test[0:120]
plt.figure()
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 指定中文字体
plt.plot(x, y1, color='blue', linewidth='1.0', label='预测数据')
plt.plot(x, y2, color='red', linewidth='1.0', linestyle='--', label='测试数据')
plt.xlabel('序号')
plt.ylabel('标签数据')
plt.legend()
plt.show()
