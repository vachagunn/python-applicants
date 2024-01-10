import pandas as pd
import pprint
import datetime as dt

pd.set_option('display.max_rows', None)
pr = pprint.PrettyPrinter()

data = pd.read_csv('data_fake.csv', encoding='cp1251', sep=';', decimal=',')

ind = [
    'Период обучения', 'Срок обучения', 'Курс',
    'Тип док. об обр.', 'Серия', 'Номер', 'Награды',
    'Оригинал', 'Коментарии', 'Тех. секретарь', 'Unnamed: 27'
]

data = data.drop(ind, axis=1)

dictionary = {chr(ord('A') + i): data.columns[i] for i in range(data.shape[1])}
data.columns = dictionary.keys()

# Рейтинг
data['F'] = data['F'].apply(lambda x: float(str(x).replace(',', '.')))

# Дата (из string в Date)
data['Date_dt'] = pd.to_datetime(data['Q'], format="%d.%m.%Y %H:%M")
df = data['Date_dt'].dt.strftime('%d/%m/%y %H:%M').str.split(" ", expand=True)
df.columns = ['Date_str', "Hour"]
data = pd.concat([data, df], axis=1)
data['Date'] = pd.to_datetime(data['Date_str'], format="%d/%m/%y")

df = data.groupby(['Date', 'H'])[['B', 'F']].agg({'B': 'count', 'F': ['min', 'mean', 'max']})
print('--------Группировка---------------')
print(df)
print(df.index.get_level_values(1))

# Подготовка данных для графика
pt = data.pivot_table(index='Date', columns='H', values='B', aggfunc='count')
print('--------pivot---------------------')
print(pt)
'''
H           заочная  очная  очно-заочная  экстернат
Date                                               
2019-01-09      2.0    NaN           NaN        NaN
2019-01-10      3.0    NaN           NaN        NaN
'''

# Найдем все личные дела по дате (пример)
print('----------------------------------')
print(data[data['Date_str'] == '26/06/19'])

pr.pprint(dictionary)
print(data.info())
