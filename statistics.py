import pandas as pd
import statsmodels.api as sm

#  Импортируем csv файл
dataSet = pd.read_csv('dataset_Facebook.csv', ';', header=0)

#  Вычисление статистик для всего массива
Mean = []
Min = []
Max = []
Median = []
Mode = []

#  Метрики Type, Paid, Category, Post Month, Post Weekday, Post Hour являются категориальными, следовательно, вычислять
#  для них такие статистики, как среднее, медиана, максимальные и минимальные значения не имеет смысла, поэтому, для
#  них будем вычислять талько моду.
for i in dataSet.columns:
    if (i == 'Type') or \
            (i == 'Paid') or \
            (i == 'Category') or \
            (i == 'Post Month') or \
            (i == 'Post Weekday') or \
            (i == 'Post Hour'):
        Mode.append(dataSet[i].mode()[0])
        Mean.append('-')
        Min.append('-')
        Max.append('-')
        Median.append('-')
    else:
        Mean.append(float(dataSet[i].mean().round(2)))
        Min.append(float(dataSet[i].min().round(2)))
        Max.append(float(dataSet[i].max().round(2)))
        Median.append(float(dataSet[i].median()))
        Mode.append('-')

#  Чтобы результаты удобно было экспортировать, например, в csv - файл, создадим DataFrame
dataStats = pd.DataFrame({'Mean': Mean, 'Max': Max, 'Min': Min, 'Median': Median, 'Mode': Mode},
                         index=dataSet.columns)
#  Выводим результаты
print(dataStats.to_string())

#  Вычисление статистик для каждого типа контента
Mean_gb = []
Min_gb = []
Max_gb = []
Median_gb = []
Mode_gb = []
Index_gb = []

for name, group in dataSet.groupby('Type'):
    for i in group.columns:
        Index_gb.append(str(name))
        if (i == 'Type') or \
                (i == 'Paid') or \
                (i == 'Category') or \
                (i == 'Post Month') or \
                (i == 'Post Weekday') or \
                (i == 'Post Hour'):
            Mode_gb.append(group[i].mode()[0])
            Mean_gb.append('-')
            Min_gb.append('-')
            Max_gb.append('-')
            Median_gb.append('-')
        else:
            Mean_gb.append(group[i].mean().round(2))
            Min_gb.append(group[i].min().round(2))
            Max_gb.append(group[i].max().round(2))
            Median_gb.append(group[i].median())
            Mode_gb.append('-')

# Для удобства и наглядности результатов, создадим мультииндекс
tuples = list(zip(Index_gb, list(dataSet.columns)*4))

multiIndex = pd.MultiIndex.from_tuples(tuples, names=['Type', 'Metric'])

dataStats_gb = pd.DataFrame({'Mean': Mean_gb, 'Max': Max_gb, 'Min': Min_gb, 'Median': Median_gb, 'Mode': Mode_gb},
                            index=multiIndex)

#  Выводим результаты
print(dataStats_gb.to_string())

#  Чтобы определить самый популярный объект, построим линейную регрессию. В качестве объясняемой переменной возьмем
#  'Page total likes', остальные переменные будем исользовать в качестве объясняемых, за исключением категориальных.
#  Также, избавимся от пропущенных значений.
dataSet = dataSet.dropna()

y = dataSet.loc[:, "Page total likes"]
X = dataSet.loc[:, list(dataSet.columns[7:])]

model = sm.OLS(y, X)
result = model.fit()
print(result.summary())

#  На основании результатов можно сделать вывод, что наиболее значимой переменной является
# "Lifetime Post reach by people who like your Page". Следовательно, чтобы определить наиболее популярный объект,
#  необходимо отсортировать исходный массив по этой переменной

print(dataSet.sort_values(['Lifetime Post reach by people who like your Page'], ascending=[0]).head().to_string())