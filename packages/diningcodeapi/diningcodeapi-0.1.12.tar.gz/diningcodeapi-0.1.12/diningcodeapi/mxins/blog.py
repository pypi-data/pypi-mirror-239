import requests
from bs4 import BeautifulSoup

from diningcodeapi.config import HEADERS, API_VERSION_V1


class BlogMixin:
    def get_blogs(self, store_code:str, page_no:int, proxy=None):
        url = f"https://www.diningcode.com/2018/ajax/blog.php"
        data = {
            "mode": "LIST",
            "v_rid": store_code,
            "page": page_no

        }
        response = requests.post(url, data=data, headers=HEADERS, proxies=proxy)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        blog_tags = soup.find_all("li")

        blogs = []
        for i, blog_tag in enumerate(blog_tags):
            title = blog_tag.find("span", class_='btxt').get_text()
            content = blog_tag.find("span", class_='stxt').get_text()
            author_name = blog_tag.find("span", class_="person").get_text()
            date = blog_tag.find("span", class_="date").get_text()

            blogs.append({
                "_id":f'{store_code}_{page_no}_{i}',
                "title": title,
                "content": content,
                "author_name": author_name,
                "date": date,
                "api-version":API_VERSION_V1
            })

        return blogs