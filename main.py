import pandas as pd
import pprint

def edit(x):
    return float(str(x).replace(',', '.'))


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

data['F'] = data['F'].apply(edit)
print(data['F'])
pr.pprint(dictionary)
print(data.info())
