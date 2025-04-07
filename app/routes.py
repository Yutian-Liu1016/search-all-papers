from flask import Blueprint, render_template, request, render_template_string
import requests
from bs4 import BeautifulSoup


bp = Blueprint('main', __name__)

def get_papers(url):
    response = requests.get(url)
    papers = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        for span in soup.find_all('span', class_='title', itemprop='name'):
            papers.append(span.text)
    return papers

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/submit', methods=['POST'])
def submit():
    user_input = request.form.get('user_input')
    # user_input = render_template_string(user_input)
    search_url = f"https://dblp.org/search?q={user_input}"
    response = requests.get(search_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
                # 提取搜索结果中的标题和 URL
        results = []
        for result in soup.find_all('a', href=True):  # 定位到包含标题的 <a> 标签并确保有 href 属性
            url = result['href']  # 提取 href 的 URL
            if url.startswith("https://dblp.org/pid"):
                results.append(url)
        papers = get_papers(results[0])
    else:
        papers = []
    return render_template('index.html', result=user_input, papers=papers)