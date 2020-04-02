"""
https://www.divi.de/register/kartenansicht

https://docs.python-guide.org/scenarios/scrape/

https://towardsdatascience.com/web-scraping-html-tables-with-python-c9baba21059

"""
from lxml.cssselect import CSSSelector
from lxml import html
import requests

# pip install cssselect
page = requests.get('https://www.divi.de/register/kartenansicht')
tree = html.fromstring(page.content)


t1 = tree.xpath(
    'table/tbody/tr'
)
# t2 = tree.cssselect('table_wrapper > div > div.dataTables_scrollBody')


# t2 = tree.xpath('//tr/td//text()')
t2 = tree.xpath('//tr/td')

t3 = tree.xpath('//tr')

for i in range(len(t3)):
    T = t3[i]
    for t in T.iterchildren():
        data = t.text_content()
1

for item in t3:
    for item2 in item:
        print(item2.text_content())

# t2 = CSSSelector('#table').get
1


#table_wrapper > div > div.dataTables_scrollBody
