from flask import Flask, render_template, request
from titlecase import titlecase
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
scores = pickle.load(open('scores.pkl', 'rb'))
app = Flask(__name__)

@app.route('/')

def index():
    return render_template('index.html',
                           book_name = (list(popular_df['Book-Title'].values)),
                           auth_name = (list(popular_df['Book-Author'].values)),
                           imgs      = (list(popular_df['Image-URL-M'].values)),
                           votes     = (list(popular_df['num_ratings'].values)),
                           ratings   = (list(popular_df['avg_ratings'].values))
                          )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['post'])
def recommend():
    user_input = titlecase(request.form.get('uip').lower())

    #fetch the exact index of the book
    index_fetch = np.where(pt.index == user_input)[0][0]
    sim_items = sorted(list(enumerate(scores[index_fetch])), key = lambda x:x[1], reverse = True)[1:6]
    
    data = []

    for i in sim_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    return render_template('recommend.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
