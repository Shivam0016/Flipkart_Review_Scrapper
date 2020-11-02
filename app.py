"""importing required libraries"""
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, render_template

"""Name given in Procfile"""
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        try:
            search_term = request.form['content'].replace(" ", "")
            html_code = requests.get("https://www.flipkart.com/search?q=" + search_term)
            parsed_html = BeautifulSoup(html_code.text, "html.parser")
            variants = parsed_html.find_all('a', {"class": "_31qSD5"})
            variant_list = list()
            for i in variants:
                variant_list.append("https://www.flipkart.com" + i['href'])

            variant_1 = requests.get(variant_list[0])
            main_html = BeautifulSoup(variant_1.text, "html.parser")
            print(variant_list[0])
            temp = main_html.find("div", {"class": "col _39LH-M"})
            print(temp)
            p = temp.findChildren('a', recursive=False)

            review_page = "https://www.flipkart.com" + p[0]['href']

            final_html = requests.get(review_page)
            print(review_page)
            temp_parsed = BeautifulSoup(final_html.text, "html.parser")

            final_parsed = temp_parsed.find_all("div", {"class": "col _390CkK _1gY8H-"})

            rating_lst = list()
            title_lst = list()
            comment_lst = list()
            user_list = list()

            for each_tag in final_parsed:
                rating_lst.append(each_tag.div.div.text)
                title = each_tag.div.findChildren('p')
                for i in title:
                    title_lst.append(i.text)
            for comment in temp_parsed.find_all('div', {'class': 'qwjRop'}):
                comment_lst.append(comment.div.div.text)
            for comment in temp_parsed.find_all('p', {'class': '_3LYOAd _3sxSiS'}):
                user_list.append(comment.text)
            for comment in temp_parsed.find_all('p', {'class': '_3LYOAd'}):
                user_list.append(comment.text)

            zipped = zip(rating_lst, title_lst, comment_lst, user_list)
        except Exception:
            return render_template("exception.html")
        else:
            return render_template("result.html", zipped=zipped)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
