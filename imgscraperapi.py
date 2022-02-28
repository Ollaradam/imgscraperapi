from flask import Flask, render_template
import wikipedia, requests, json


app = Flask(__name__)
# The below forces the wiki api to render only the main image of the requested page
WIKI_REQUEST = 'http://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles='


# Home page filler to test activity. Place index.html to "templates" folder in same file as this
# to use same syntax.
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/imageresult', methods=["POST", "GET"])
def noreq():
    return "Please enter a search paramater after /imageresult/"


# localhost:5000/imageresult/*What you want to search here*/
@app.route('/imageresult/<imagereq>/', methods=["POST", "GET"])
def get_wiki_image(imagereq):
    try:
        result = wikipedia.search(imagereq, results = 1)
        wikipedia.set_lang('en')
        wkpage = wikipedia.WikipediaPage(title = result[0])
        title = wkpage.title
        response  = requests.get(WIKI_REQUEST+title)
        json_data = json.loads(response.text)
        img_link = list(json_data['query']['pages'].values())[0]['original']['source']
        return img_link
        # This returns ONLY the image link. It is possible to return the actual image but it is a bit overkill
        # since you can place the link within your code to reveal the image.
    except:
        return "Primary image not found"
        # If fail


if __name__ == '__main__':
    app.run(debug=True)
    # Standard port=5000
