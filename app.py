from flask import Flask, render_template, request
from bs4 import BeautifulSoup
from datetime import datetime
import requests

app = Flask(__name__)

headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 YaBrowser/25.2.0.0 Safari/537.36'
}

def oilworld(param):
    result = []
    try:
        url = f'https://oilworld.ru/search/?searchstring={param}'
        url_main = 'https://oilworld.ru'
        req = requests.get(url, headers=headers, timeout=10).text
        soup = BeautifulSoup(req, 'html.parser')
        news = soup.find_all('div', class_='left-line')
        for i in news:
            hour_ = i.find('span').text
            if len(hour_) == 5:
                title = i.find('a').text.strip()
                link = url_main + i.find('a').get('href')
                result.append((title, link))
    except Exception as e:
        result.append((f"Ошибка Oilworld: {e}", "#"))
    return result

def apk_inform(param):
    result = []
    try:
        url = f'https://www.apk-inform.com/ru/search?query={param}'
        url_main = 'https://www.apk-inform.com'
        req = requests.get(url, headers=headers, timeout=10).text
        soup = BeautifulSoup(req, 'html.parser')
        news = soup.find_all('div', class_='content-result-search')
        for i in news:
            hour_ = i.find('span').text
            if len(hour_) == 9:
                title = i.find('a', class_='text').text.strip()
                link = url_main + i.find('a', class_='text').get('href')
                result.append((title, link))
    except Exception as e:
        result.append((f"Ошибка APK-Inform: {e}", "#"))
    return result

def oleoscope():
    result = []
    try:
        url_main = 'https://oleoscope.com/'
        req = requests.get(url_main, timeout=10).text
        soup = BeautifulSoup(req, 'html.parser')
        news = soup.find_all('article', class_='news-feed__item')
        for i in news:
            try:
                date = datetime.strptime(i.find('div', class_='news-feed__date').text, '%d.%m.%Y').date()
                if date == datetime.now().date():
                    title = i.find('a', class_='news-feed__title').text.strip()
                    link = i.find('a', class_='news-feed__title').get('href')
                    result.append((title, link))
            except:
                continue
    except Exception as e:
        result.append((f"Ошибка Oleoscope: {e}", "#"))
    return result

def agrotrend(param):
    result = []
    try:
        url = f'https://agrotrend.ru/?s={param}'
        req = requests.get(url, timeout=10).text
        soup = BeautifulSoup(req, 'html.parser')
        news = soup.find_all('a', class_='announce-list__item')
        for i in news:
            try:
                date = datetime.strptime(i.find('div', class_='announce-list__date').text, '%d.%m.%Y').date()
                if date == datetime.now().date():
                    title = i.find('div', class_='announce-list__title').text.strip()
                    link = i.get('href')
                    result.append((title, link))
            except:
                continue
    except Exception as e:
        result.append((f"Ошибка Agrotrend: {e}", "#"))
    return result

def agroexpert():
    result = []
    try:
        url = 'https://agroexpert.press/eksport-import/'
        req = requests.get(url, timeout=10).text
        soup = BeautifulSoup(req, 'html.parser')
        news = soup.find_all('div', class_='article-item__text')
        for i in news:
            hour_ = i.find('div', class_='article-time').text.split(',')
            if len(hour_) < 3:
                title = i.find('a', class_='subtitle-16 article-item__link').text.strip()
                link = i.find('a', class_='subtitle-16 article-item__link').get('href')
                result.append((title, link))
            else:
                break
    except Exception as e:
        result.append((f"Ошибка Agroexpert: {e}", "#"))
    return result

@app.route('/', methods=['GET', 'POST'])
def index():
    results = {}
    keyword = ""
    if request.method == 'POST':
        keyword = request.form.get('keyword', '').strip()
        if keyword:
            results = {
                "Oilworld": oilworld(keyword),
                "APK-Inform": apk_inform(keyword),
                "Oleoscope (сегодня)": oleoscope(),
                "Agrotrend (сегодня)": agrotrend(keyword),
                "Agroexpert": agroexpert()
            }
    return render_template('index.html', results=results, keyword=keyword)

if __name__ == '__main__':
    app.run(debug=True)
