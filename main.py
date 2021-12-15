from PyPDF2.pdf import setRectangle
from bs4 import BeautifulSoup
import requests
import io
import PyPDF2
from googlesearch import search
query = "esg sector :pdf"
import requests, lxml
from bs4 import BeautifulSoup
from boilerpipe.extract import Extractor

URL='https://www.beautypackaging.com/contents/view_breaking-news/2021-12-13/geka-earns-b-from-cdp-for-reducing-its-environmental-impact/'

extractor = Extractor(extractor='ArticleExtractor', url=URL)

print(extractor.getText())
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
headers = {
    "User-Agent": "Chrome/70.0.3538.102"
}

params = {
    "q": "gta 5",
    "hl": "en",
    "tbm": "nws",
    "num": 100
    
}

response = requests.get("https://www.google.com/search", params=params)
soup = BeautifulSoup(response.text, 'lxml')

# for result in soup.select('.dbsr'):
#     title = result.select_one('.nDgy9d').text
#     link = result.a['href']
#     source = result.select_one('.WF4CUc').text
#     snippet = result.select_one('.Y3v8qd').text
#     date_published = result.select_one('.WG9SHc span').text
#     print(f'{title}\n{link}\n{snippet}\n{date_published}\n{source}\n')

# search_result = []
# for j in search(query, num=10, stop=10, pause=2):
#     search_result.append(j)
# # html_page = requests.get(search_result[1])
# html_page = requests.get("https://fortune.com/2021/12/08/methane-emissions-food-additives-cattle-farming/").text
# # print(search_result[1])
# soup = BeautifulSoup(html_page,"html.parser")
# # print(soup.prettify)
# with open("test.html", mode="w+") as f:
#     # pdf = PyPDF2.PdfFileReader(io.BytesIO(html_page.content))
#     f.write(soup.prettify())
#     # f.write(pdf.getPage(0))
# f.close()
# url = requests.get("https://google.com/url?q=https://www.spglobal.com/_media/documents/ratingsdirect_theesgriskatlassectorandregionalrationalesandscores_41534468_may-15-2019.pdf&sa=U&ved=2ahUKEwjioYy1uuD0AhV3qpUCHfTZDTUQFnoECAoQAg&usg=AOvVaw0iX4i7KuYPn42gGFHQ6eJG").url
# pdf = PyPDF2.PdfFileReader(io.BytesIO(r.content))
# print(r.history[2].url)
main_div = soup.find("div", id="main")