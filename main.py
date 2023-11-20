import requests
import selectorlib
import os
import smtplib
import ssl

url = "https://programmer100.pythonanywhere.com/tours/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/39.0.2171.95 Safari/537.36'}


def scrape(url):
    """scrape the page source from the url"""
    response = requests.get(url, headers)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def send_email(message):
    host = "smtp.gmail.com"
    port = 465
    username = "acaldezuniga@gmail.com"
    password = os.getenv("PASSWORD")
    receiver = "acaldezuniga@gmail.com"
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)


def store(extracted):
    with open("data.txt", 'a') as file:
        file.write(extracted + '\n')


def read(extracted):
    with open("data.txt", 'r') as file:
        return file.read()


if __name__ == "__main__":
    scraped = scrape(url)
    extracted = extract(scraped)
    print(extracted)
    content = read(extracted)
    if extracted != "No upcoming tours":
        if extracted not in content:
            store(extracted)
            send_email(message="Hey, new event was found!")

