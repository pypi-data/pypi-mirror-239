import urllib.request
from bs4 import BeautifulSoup


def main():
    path = "./data.txt"
    url = "http://172.18.12.202/forum.php?mod=viewthread&tid="
    askurl(url,path)

min_tid = 0
max_tid = 5846

########判断url是否合法，是否可连通，HTTP状态码是否为200
def get_url_content(url):
    response = urllib.request.urlopen(url)
    html = response.read().decode("utf-8")
    if response.getcode() == 200:
        if "抱歉，指定的主题不存在或已被删除或正在被审核" in html:
            return False
        else:
            # 如果可以连通返回网页源码
            return html
    else:
        return False

# # 定义方法解析html_text
def pare_post_data(html,tid):
    bs = BeautifulSoup(html, "html.parser")

    authors = bs.select("div > .authi > .xw1")
    # print("这是作者列表"+str(authors))
    author = authors[0].text

    titles = bs.select("#thread_subject")
    title = titles[0].text

    scores = bs.select("td > p > .xi2")
    score = scores[0].text

    grades = bs.select("p > em > a")
    grade = grades[0].text

    contents = bs.select("tr > .t_f")
    content1 = contents[0].text
    content1 = content1.replace("\r","")
    content2 = content1.split("\n")

    post_content_info = {
        "tid":tid,
        "author":author,
        "score":score,
        "grade":grade,
        "title":title,
        "content":content2[1],
    }
    return post_content_info



#爬取所有网页并处理数据
def askurl(url,path):
    f = open(path, "a+", encoding='utf-8')
    for i in range(min_tid,max_tid):
        html = get_url_content(url + str(i))
        if html != False:
            tid = str(i)
            pare_post_data1 = pare_post_data(html,tid)
            get_tid = pare_post_data1.get("tid")
            get_author = pare_post_data1.get("author")
            get_score = pare_post_data1.get("score")
            get_grade = pare_post_data1.get("grade")
            get_title = pare_post_data1.get("title")
            get_content = pare_post_data1.get("content")
            print(get_tid+","+get_author+","+get_score+","+get_grade+","+get_title+","+get_content.strip())
            f.write(get_tid+","+get_author+","+get_score+","+get_grade+","+get_title+","+get_content.strip() + '\n')
    f.close()

if __name__ == "__main__":
    print("tid"+","+"author"+","+"score"+","+"grade"+","+"title"+","+"content")
    main()
    print("爬取完毕！！！")