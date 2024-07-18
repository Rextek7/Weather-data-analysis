import requests  # Импортируем библиотеку requests для выполнения HTTP-запросов
from bs4 import BeautifulSoup  # Импортируем BeautifulSoup для парсинга HTML
import datetime  # Импортируем модуль datetime для работы с датами


def get_soup(url):
    """
    Выполняет HTTP-запрос к указанному URL и возвращает объект BeautifulSoup для парсинга HTML.
    """
    doc = requests.get(url, verify=False, headers={
        "User-Agent": "Chrome/124.0.0.0 Safari/537.36"})  # Выполняем GET-запрос с поддельным User-Agent
    soup = BeautifulSoup(doc.text, "html.parser")  # Парсим ответ с помощью BeautifulSoup
    return soup


def get_dates():
    """
    Возвращает список дат в формате 'dd.mm.yyyy' начиная с сегодняшнего дня и на следующие 14 дней.
    """
    today = datetime.date.today()  # Получаем сегодняшнюю дату
    dates = []
    for i in range(14):
        next_day = today + datetime.timedelta(days=i)  # Получаем следующую дату
        formatted_date = next_day.strftime('%d.%m.%Y')  # Форматируем дату
        dates.append(formatted_date)  # Добавляем дату в список
    return dates


def get_temps(day_temp):
    """
    Разделяет список температур на дневные и ночные, и расширяет их до длины 14, если необходимо.
    """
    days_temps = [day_temp[i].text if day_temp[i] is not None else None for i in
                  range(0, len(day_temp), 2)]  # Извлекаем дневные температуры
    nights_temps = [day_temp[i + 1].text if day_temp[i + 1] is not None else None for i in
                    range(0, len(day_temp), 2)]  # Извлекаем ночные температуры

    # Расширяем списки до длины 14
    if len(days_temps) < 14:
        days_temps = extend_to_length(days_temps, 14)
    if len(nights_temps) < 14:
        nights_temps = extend_to_length(nights_temps, 14)

    return days_temps, nights_temps


def get_data_list(data):
    """
    Преобразует список элементов HTML в список чисел, расширяет его до длины 14, если необходимо.
    """
    # Преобразование строк в числа, при этом учитываем возможные десятичные разделители
    data_list = [float(element.replace(',', '.')) if ',' in element else int(element) for element in
                 [data[i].text for i in range(len(data))]]

    # Расширяем список до длины 14
    if len(data_list) < 14:
        data_list = extend_to_length(data_list, 14)

    return data_list


def extend_to_length(arr, length):
    """
    Расширяет массив до указанной длины, добавляя последние элементы.
    """
    while len(arr) < length:
        arr.append(
            arr[-1])  # Добавляем последний элемент массива до тех пор, пока длина массива не станет равной заданной
    return arr


def get_pressure(max_pressure, min_pressure):
    """
    Извлекает и преобразует максимальное и минимальное давление, расширяет списки до длины 14, если необходимо.
    """
    days_max = [max_pressure[i].text[:3] for i in
                range(len(max_pressure))]  # Извлекаем первые три символа текста для максимального давления
    days_min = [min_pressure[i].text[:3] for i in
                range(len(min_pressure))]  # Извлекаем первые три символа текста для минимального давления

    # Преобразуем строки в числа
    days_max = [int(pressure) for pressure in days_max]
    days_min = [int(pressure) for pressure in days_min]

    # Расширяем массивы до длины 14
    if len(days_max) < 14:
        days_max = extend_to_length(days_max, 14)
    if len(days_min) < 14:
        days_min = extend_to_length(days_min, 14)

    return days_max, days_min


def get_weather_data(city):
    """
    Извлекает и возвращает данные о погоде для указанного города за 14 дней.
    """
    url = f'https://www.gismeteo.ru/weather-{city}/2-weeks/'  # Формируем URL для запроса
    soup = get_soup(url)  # Получаем объект BeautifulSoup для парсинга HTML

    dates = get_dates()  # Получаем список дат

    # Парсинг данных о температуре
    day_temp = soup.find('div', {'class': 'chart ten-days'}).find_all('span', {'class': 'unit unit_temperature_c'})
    days_temps, nights_temps = get_temps(day_temp)

    # Парсинг данных об осадках
    precipitation = soup.find('div', {'class': 'widget-row widget-row-precipitation-bars row-with-caption'}).find_all(
        'div', {'class': 'row-item'})
    precip = get_data_list(precipitation)

    # Парсинг данных о скорости ветра
    wind_m_s = soup.find('div', {'class': 'widget-row widget-row-wind-gust row-with-caption'}).find_all('span', {
        'class': 'wind-unit unit unit_wind_m_s'})
    wind = get_data_list(wind_m_s)

    # Парсинг данных о давлении
    max_pressure = soup.find('div', {'data-row': 'pressure'}).find('div', {'class': 'chart ten-days'}).find_all('div', {
        'class': 'maxt'})
    min_pressure = soup.find('div', {'data-row': 'pressure'}).find('div', {'class': 'chart ten-days'}).find_all('div', {
        'class': 'mint'})
    days_max, days_min = get_pressure(max_pressure, min_pressure)

    # Возвращаем словарь с данными о погоде
    return {
        'date': dates,
        'day_temp': days_temps,
        'night_temp': nights_temps,
        'precipitation': precip,
        'wind_m_s': wind,
        'max_pressure': days_max,
        'min_pressure': days_min
    }
