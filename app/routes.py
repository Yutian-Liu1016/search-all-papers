import sys
import requests
from bs4 import BeautifulSoup
from flask import Blueprint, render_template, request

sys.stdout.reconfigure(encoding='utf-8')

class DblpScraper:

    BASE_URL = "https://dblp.uni-trier.de"

    def _make_request(self, url):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'
            return BeautifulSoup(response.content, 'html.parser')
        except requests.exceptions.RequestException as e:
            print(f"请求错误: {e} for URL: {url}")
            return None

    def search_author(self, query):
        search_url = f"{self.BASE_URL}/search/author?q={query}"
        soup = self._make_request(search_url)
        if not soup:
            return None, None

        main_div = soup.find('div', id='main')
        if not main_div:
            return [], []

        parent_div = main_div.find('div', id='completesearch-authors', class_='section hideable')
        affiliations_list = []

        if parent_div:
            parent_div_2 = parent_div.find('div', class_='body hide-body')
            match_type = parent_div_2.find('p')
            match_type_text = match_type.text.strip()
            if match_type_text != "Exact matches":
                return None, None 
            result_list = parent_div_2.find('ul', class_='result-list') if parent_div_2 else None
            if result_list:
                for result in result_list.find_all('li'):
                    a_tag = result.find('a')
                    small_tag = result.find('small')
                    if a_tag and 'href' in a_tag.attrs:
                        url = a_tag['href']
                        affiliation_text = small_tag.text.strip() if small_tag else "N/A"
                        if url.startswith(f"{self.BASE_URL}/pid"):
                            affiliations_list.append({'url': url, 'affiliation': affiliation_text})
            return affiliations_list, None
        else:
            header_div = main_div.find('header', id='headline')
            if header_div and 'data-pid' in header_div.attrs:
                data_pid = header_div['data-pid']
                author_url = f"{self.BASE_URL}/pid/{data_pid}"
                return None, author_url
            else:
                return [], None

    def get_author_details(self, author_url):
        soup = self._make_request(author_url)
        if not soup:
            return [], [],

        papers = []
        affiliations = []
        name = "未知"

        name_tag = soup.find('span', class_='name primary', itemprop='name')
        if name_tag:
            name = name_tag.text.strip()

        for aff_li in soup.find_all('li', itemprop='affiliation'):
            span = aff_li.find('span', itemprop='name')
            if span:
                affiliations.append(span.text.strip())

        for title_span in soup.find_all('span', class_='title', itemprop='name', limit=100):
            papers.append(title_span.text.strip())

        return papers, affiliations, name


class FlaskRoutes:

    def __init__(self, scraper):
        self.scraper = scraper
        self.bp = Blueprint('main', __name__)
        self._register_routes()

    def _register_routes(self):
        self.bp.add_url_rule('/', view_func=self.index)
        self.bp.add_url_rule('/submit', view_func=self.submit, methods=['POST'])
        self.bp.add_url_rule('/get_papers', view_func=self.get_papers_route, methods=['GET'])

    def index(self):
        return render_template('index.html')

    def submit(self):
        user_input = request.form.get('user_input', '').strip()

        if not user_input:
            return render_template('index.html', error="请输入作者名称")

        affiliations_list, author_url = self.scraper.search_author(user_input)

        if affiliations_list is None and author_url is None:
             return render_template('index.html', result=user_input, error="请输入完整准确的作者名称")

        if author_url:
            papers, affs, name = self.scraper.get_author_details(author_url)
            return render_template('get_papers.html', papers=papers, affs=affs, name=name)
        elif affiliations_list:
            return render_template('index.html', result=user_input, affiliations=affiliations_list)
        else:
             return render_template('index.html', result=user_input, affiliations=[])


    def get_papers_route(self):
        author_url = request.args.get('url')

        if not author_url:
            return "未提供 URL", 400

        papers, affs, name = self.scraper.get_author_details(author_url)
        return render_template('get_papers.html', papers=papers, affs=affs, name=name)