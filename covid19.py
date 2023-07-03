from flask import Flask, render_template
import requests
import bs4
import schedule
import time

app = Flask(__name__)
result = {}

def fetch_data():
    global result
    country_name = 'Nepal'
    res = requests.get("https://www.worldometers.info/coronavirus/#countries")
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    index = -1
    data = soup.select('tr td')
    for i in range(len(data)):
        if data[i].text.lower() == country_name.lower():
            index = i
            break
    
    result = {}
    for i in range(7):
        if i == 0:
            result['Country name'] = data[i + index].text
        elif i == 1:
            result['Total cases'] = data[i + index].text
        elif i == 2:
            result['New cases'] = data[i + index].text if data[i + index].text else '0'
        elif i == 3:
            result['Total deaths'] = data[i + index].text
        elif i == 4:
            result['New deaths'] = data[i + index].text if data[i + index].text else '0'
        elif i == 5:
            result['Total recovered'] = data[i + index].text
        elif i == 6:
            result['Active cases'] = data[i + index].text

def update_data():
    schedule.every(1).hours.do(fetch_data)

@app.route('/')
def covid19():
    return render_template('index.html', result=result)

if __name__ == '__main__':
    fetch_data()  # Fetch initial data
    update_data()  # Schedule data update
    app.run()
    while True:
        schedule.run_pending()
        time.sleep(1)
