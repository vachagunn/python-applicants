import pandas as pd
import pprint
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', None)

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
data['F'] = data['F'].apply(lambda value: float(str(value).replace(',', '.')))

# Дата создания
data['Date_dt'] = pd.to_datetime(data['Q'], format="%d.%m.%Y %H:%M")
df = data['Date_dt'].dt.strftime('%d/%m/%y %H:%M').str.split(" ", expand=True)
df.columns = ['Date_str', "Hour"]
data = pd.concat([data, df], axis=1)
data['Date'] = pd.to_datetime(data['Date_str'], format="%d/%m/%y")

df = data.groupby(['Date', 'H'])[['B', 'F']].agg({'B': 'count', 'F': ['min', 'mean', 'max']})
pt = data.pivot_table(index='Date', columns='H', values='B', aggfunc='count')

# График 1
fig = plt.figure(figsize=(8, 4))
x = df.index.get_level_values(0)
y = df['B']
plt.plot(x, y, "c4--")
plt.xticks(rotation=90)
plt.suptitle('Приемная компания 2019', color='#ff0000', font='Times New Roman')
plt.title('Ход подачи заявлений')

# График 2
fig2 = plt.figure()
x = pt.index
y1 = pt['очная'].cumsum()
y2 = pt['заочная'].cumsum()
y3 = pt['очно-заочная'].cumsum()
plt.stackplot(x, y1, y2, y3)
