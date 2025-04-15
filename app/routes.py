import sys
sys.stdout.reconfigure(encoding='utf-8')
from flask import Blueprint, render_template, request, render_template_string
import requests
from bs4 import BeautifulSoup


bp = Blueprint('main', __name__)

def get_papers(url):
    response = requests.get(url)
    print("url", url)
    papers = []
    aff = []
    if response.status_code == 200:
        print(200)
        soup = BeautifulSoup(response.content, 'html.parser')
        for affs in soup.find_all('li', itemprop='affiliation'):
            span = affs.find('span', itemprop='name')
            aff.append(span.text)
        for span in soup.find_all('span', class_='title', itemprop='name')[:100]:
            papers.append(span.text)
    return papers, aff

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/submit', methods=['POST'])
def submit():
    print("submit")
    user_input = request.form.get('user_input')
    print("user_input:", user_input)
    # user_input = render_template_string(user_input)
    search_url = f"https://dblp.uni-trier.de/search/author?q={user_input}"
    response = requests.get(search_url)
    if response.status_code == 200:
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'html.parser')
        results = []
        # 提取搜索结果中的标题和 URL
        main_div = soup.find('div', id='main')
        
        parent_div = main_div.find('div', id='completesearch-authors', class_='section hideable')
        if parent_div:
            print("parent_div")
            parent_div_2 = parent_div.find('div', class_='body hide-body')
            result_list = parent_div_2.find('ul', class_='result-list')
            print("result:")
            for result in result_list.find_all('a', href=True):  # 定位到包含标题的 <a> 标签并确保有 href 属性
                url = result['href']  # 提取 href 的 URL
                print(url)
                if url.startswith("https://dblp.uni-trier.de/pid"):
                    results.append(url)
        else:
            print("parent_div not found")
            div = main_div.find('header' ,id='headline') # 定位到包含 data-pid 的元素
            data_pid = div.get('data-pid')
            if data_pid:
                url = f"https://dblp.uni-trier.de/pid/{data_pid}"
                print(url)
                results.append(url)
        papers,affs = get_papers(results[0])
        
    else:
        papers = []
    return render_template('index.html', result=user_input, papers=papers, affs=affs)