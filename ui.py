from flask import Flask, url_for, render_template
import recommend as r

app = Flask(__name__)

db = r.DataBase(users_file='datasets/ml-100k/u.user',
                movies_file='datasets/ml-100k/u.item',
                ratings_file='datasets/ml-100k/u.data')
db.calculate_similarities()
users = sorted([i for i in db.users], key=int)

# @app.route('/')
# def hello_world():
#     return 'Hello World! ' + url_for('hello')


@app.route('/')
def index():
    """Display landing page"""
    user = '1'
    top_n = db.top_n(n=20, min_n=5, user=None)
    return render_template('index.html', user=user, db=db, users=users,
                           top_n=top_n)


# @app.route('/hello')
# def hello():
#     return 'Hello World'

@app.route('/user/<user>')
def show_user_profile(user):  # db=db):
    """Show the user profile for user"""
    db.users[user].sort_ratings()
    pop = db.recommend(user, n=20, mode='dumb', num_users=5)
    rec = db.recommend(user, n=20, mode='simple', num_users=5)
    # print('Your favorite movies:\n', '*'*40)
    favs = db.users[user].my_favorites(
        n=500)  # db.translate(db.users[user].my_favorites(n=500), fn=db.get_title)
    # print('Your recommended movies:\n', '*'*40)
    recs = rec  # recs = db.translate(rec, fn=db.get_title) # TODO: Add decorator for translate?
    sim = db.similar(user, n=10, min_matches=3)

    return render_template('user.html', user=user, db=db, favs=favs, pop=pop,
                           recs=recs, users=users, sim=sim)


@app.route('/movie/<movie>')
def show_movie(movie):  # db=db):
    """Show the movie profile movie"""

    return render_template('movie.html', db=db, movie=movie)

# @app.route('/post/<int:post_id>')
# def show_post(post_id):
#     # show the post with the given id, the id is an integer
#     return 'Post %d' % post_id
#
# @app.route('/bla')
# def blabla():
#     bla = 'blah..blah...'
#     return render_template('template.html', bla=bla)


if __name__ == '__main__':
    app.run(debug=True)
