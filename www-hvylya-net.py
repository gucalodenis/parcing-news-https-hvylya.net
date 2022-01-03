import json
import requests
from bs4 import BeautifulSoup

url = 'https://hvylya.net/news'


def get_links():  # news list
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0 Win64x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
        'accert' 'text/html,application/xhtml+xml,application/xml;q = 0.9,image/avif,image/webp,image/apng,*/*;q = 0.8,application/signed-exchange;v = b3;q = 0.9'
    }
    r = requests.get(url, headers=header)
    soup = BeautifulSoup(r.content, 'html.parser')

    # find all links to news
    url_news = soup.findAll('div', class_='b-card')
    news_one = []  # create an empty list

    for item in url_news:  # we get each news separately and add it to the list
        news_one.append(item.a['href'])

    return news_one  # return the list of news


def get_page_content(link):  # data list for news
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')

    # news heading
    title_one = soup.find('div', class_='b-card--text')
    title_end = title_one.text.rstrip()

    # link to image
    img_one = soup.find('div', 'b-card--image').img['data-src']

    body_one = soup.find('div', class_='article-body')
    # since the text of the news is divided into several paragraphs, first we find them all
    body_group = []  # create an empty list to add all paragraphs
    for item_body in body_one:
        body_group.append(item_body.text.strip())
    # add paragraphs to the list
    body_end = ''.join(body_group)  # create a line file

    date_time = soup.find('time')
    # since the date and time in the news are in one line, we break them separately through the line index

    page_info = {'url': link, 'title': title_end, 'img': img_one, 'body': body_end,
                 'date': date_time.text[0:10], 'time': date_time.text[10:]}

    return page_info  # return a dictionary with news data


def main():  # compilation of link to news and data, and creation of json file
    links = get_links()  # link to news
    top_news = []  # empty list for links to news and their data

    for link in links:  # add data on it to each news
        print(f'Обрабатывается {link}')
        info = get_page_content(link)
        top_news.append(info)

    with open("www-hvylya-net.json", "wt", encoding='utf-8') as f:  # creation of json file
        json.dump(top_news, f, ensure_ascii=False)
    print("Работа завершена")


# Main function
if __name__ == "__main__":
    main()
