import pandas as pd
import pprint
import datetime as dt

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

print("Столбец даты:\n", data['Date_dt'])
print("DateFrame:\n", df)

df.columns = ['Date_str', "Hour"]

data = pd.concat([data, df], axis=1)
'''
--->
17  Date_dt   12352 non-null  datetime64[ns]
18  Date_str  12352 non-null  object        
19  Hour      12352 non-null  object    
'''

# Найдем все личные дела по дате (пример)
print('----------------------------------')
print(data[data['Date_str'] == '26/06/19'])

pr.pprint(dictionary)
print(data.info())
