import requests
import selectorlib

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

def send_email():
    print("Email was sent!")


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
    store(extracted)
    content = read(extracted)
    if extracted != "No upcoming tours":
        if extracted not in content:
            send_email()

