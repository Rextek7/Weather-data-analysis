from data import get_weather_data  # Импортируем функцию get_weather_data из модуля data
import pandas as pd  # Импортируем библиотеку pandas для работы с данными
import csv  # Импортируем модуль csv для работы с CSV файлами
import ast  # Импортируем модуль ast для безопасного выполнения строк как выражений Python
import re  # Импортируем модуль re для работы с регулярными выражениями

# Список городов, для которых будем получать данные о погоде
cities = ["moscow-4368", "sankt-peterburg-4079", "yalta-5002"]
data = []  # Создаем пустой список для хранения данных

# Получаем данные о погоде для каждого города
for city in cities:
    try:
        # Получаем данные о погоде с помощью функции get_weather_data
        weather = get_weather_data(city)
        # Добавляем название города в данные
        weather['city'] = city
        # Добавляем данные в список
        data.append(weather)
    except Exception as e:
        # Обрабатываем ошибки
        print(f"Не удалось получить данные для {city}: {e}")

# Сохраняем данные в DataFrame и записываем в CSV файл
df = pd.DataFrame(data)
# Сохраняем DataFrame в CSV файл, необходимо для перестраховки
df.to_csv('weather_data.csv', index=False)

# Загружаем данные из CSV файла
data = {}

# Открываем CSV файл
with open('weather_data.csv', newline='') as csvfile:
    # Создаем объект DictReader для чтения строк в виде словарей
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Получаем название города
        city = row['city']
        # Убираем числовую часть из названия города
        city = re.sub(r"-\d+", "", city)
        if city not in data:
            data[city] = {}
        # Преобразуем строку с датами в список
        date_list = ast.literal_eval(row['date'])
        data['date'] = date_list
        for key in ['day_temp', 'night_temp', 'precipitation', 'wind_m_s', 'max_pressure', 'min_pressure']:
            # Преобразуем строку с данными в список
            value_list = ast.literal_eval(row[key])
            if key == 'day_temp' or key == 'night_temp':
                # Преобразуем значения температур в числа
                value_list = [int(x.replace('+', '')) for x in value_list]
            # Сохраняем данные
            data[city][key] = value_list

        # Преобразуем данные в DataFrame
df_moscow = pd.DataFrame(data['moscow'])
df_sankt_peterburg = pd.DataFrame(data['sankt-peterburg'])
df_yalta = pd.DataFrame(data['yalta'])
df_dates = pd.DataFrame(data['date'], columns=['date'])

# Добавляем столбец с датами
df_moscow['date'] = df_dates
df_sankt_peterburg['date'] = df_dates
df_yalta['date'] = df_dates

# Конвертируем даты в формат datetime
df_moscow['date'] = pd.to_datetime(df_moscow['date'], format='%d.%m.%Y')
df_sankt_peterburg['date'] = pd.to_datetime(df_sankt_peterburg['date'], format='%d.%m.%Y')
df_yalta['date'] = pd.to_datetime(df_yalta['date'], format='%d.%m.%Y')
