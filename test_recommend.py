from recommend import *
from pprint import pprint as pprint
import time

def test_data_files_are_present():
    with open("datasets/ml-100k/u.data") as file:
        assert file.readline()
    with open("datasets/ml-100k/u.item") as file:
        assert file.readline()
    with open("datasets/ml-100k/u.user") as file:
        assert file.readline()

def test_user_creation():
    user = User(user_id='1', age='24', gender='M', job='technician', zipcode='85711')
    assert isinstance(user, User)
    assert user.zipcode == '85711'

def test_load_users():
    users = User.load_users('datasets/ml-100k/uhead.user')
    print(users)
    assert users['1'].job == 'technician'
    assert users['10'].zipcode == '90703'

def test_load_user_ratings():
    # cat u.data ',' egrep "^[1-9]\t" > uhead.data
    users = User.load_users('datasets/ml-100k/uhead.user')
    users = User.load_ratings('datasets/ml-100k/uhead.data', users)
    assert len(users['1'].ratings) == 272
    assert users['1'].ratings['113'] == '5'

def test_user_movies_property():
    users = User.load_users('datasets/ml-100k/uhead.user')
    users = User.load_ratings('datasets/ml-100k/uhead.data', users)
    for item_id in ['236', '180', '17']:
        assert item_id in users['1'].movies

def test_movie_creation():
    fieldnames = Movie.item_fieldnames
    values = ['1','Toy Story (1995)','01-Jan-1995','','http://us.imdb.com/M/title-exact?Toy%20Story%20(1995)','0','0','0','1','1','1','0','0','0','0','0','0','0','0','0','0','0','0','0']
    kwargs = dict(zip(fieldnames, values))
    movie = Movie(**kwargs)
    assert isinstance(movie, Movie)
    print(dir(movie))
    assert movie.movie_id == '1'
    assert movie.Animation == '1'
    assert movie.movie_title == 'Toy Story (1995)'
    assert movie.Western == '0'

def test_load_movies():
    movies = Movie.load_movies('datasets/ml-100k/uhead.item')
    pprint(movies)
    assert movies['1'].movie_title == 'Toy Story (1995)'
    assert movies['1'].Animation == '1'

def test_load_movie_ratings():
    movies = Movie.load_movies('datasets/ml-100k/uhead.item')
    movies = Movie.load_ratings('datasets/ml-100k/uhead.data', movies)
    assert len(movies['7'].ratings) == 5
    pprint(movies['7'].ratings)
    assert movies['7'].ratings['9'] == '4'
    #pprint(movies)
    assert movies['127'].ratings['7'] == '5'

def test_movies_users_property():
    movies = Movie.load_movies('datasets/ml-100k/uhead.item')
    movies = Movie.load_ratings('datasets/ml-100k/uhead.data', movies)
    for user_id in ['2', '6', '5', '1']:
        assert user_id in movies['1'].users

def test_movies_num_ratings():
    movies = Movie.load_movies('datasets/ml-100k/uhead.item')
    movies = Movie.load_ratings('datasets/ml-100k/uhead.data', movies)
    assert movies['1'].num_ratings == 4

def test_movies_avg_rating():
    movies = Movie.load_movies('datasets/ml-100k/uhead.item')
    movies = Movie.load_ratings('datasets/ml-100k/uhead.data', movies)
    assert movies['7'].avg_rating == 3.6

def load_files(users_file='datasets/ml-100k/uhead.user',
               movies_file='datasets/ml-100k/uhead.item',
               ratings_file='datasets/ml-100k/uhead.data'):
#     users = User.load_users('datasets/ml-100k/uhead.user')
#     users = User.load_ratings('datasets/ml-100k/uhead.data', users)
#     movies = Movie.load_movies('datasets/ml-100k/uhead.item')
#     movies = Movie.load_ratings('datasets/ml-100k/uhead.data', movies)
#     return users, movies
    db = DataBase(users_file=users_file,
                  movies_file=movies_file,
                  ratings_file=ratings_file)
    return db

def test_db_creation():
    db = load_files()
    assert db.users['1'].ratings['113'] == '5'
    assert db.movies['7'].avg_rating == 3.6
    assert db.movies['1'].movie_title == 'Toy Story (1995)'

# def test_db_avgs():
#     db = load_files()
#     for i in [('581', 5.0), ('313', 5.0), ('109', 5.0)]:
#         assert i in db.averages


def test_top_n():
    db = load_files()
    assert db.top_n(n=20, min_n=2, user=None)[0][1] == 5.0
    assert db.top_n(n=20, min_n=20, user=None) == []
    assert len(db.top_n(n=20, min_n=2, user=None)) == 20
    assert len(db.top_n(n=20, min_n=5, user=None)) == 14
    rankings = db.top_n(n=10, min_n=3, user=None)
    last = 5
    for i in rankings:
        assert last >= i[1]
        last = i[1]
    ### Debug display:
    for (movie_id, rating) in (db.top_n()):
        print("{}\t\tAvg Rating: {}".format(db.get_title(movie_id), rating))
    assert True

def test_top_n_user():
    db = load_files()
    unfiltered = db.top_n(n=20, min_n=5, user=None)
    tup_list = db.users['1'].movies
    m_list = [m[0] for m in tup_list]
    #print(m_list)
    filtered = db.top_n(n=20, min_n=5, user='1')
    assert len(unfiltered) > len(filtered)
    for (mov, avg) in filtered:
        assert mov not in db.users['1'].movies

    ### Debug display:
    for (movie_id, rating) in (db.top_n(user='1')):
        print("{}\t\tAvg Rating: {}".format(db.get_title(movie_id), rating))
    print('User 1 has seen: {}'.format(sorted(db.users['1'].movies, key=int)))
    assert True

def test_intersection():
    db = load_files()
    intersection = db.intersection('1', '2')
    for movie in intersection:
        assert movie in db.users['1'].movies
        assert movie in db.users['2'].movies

def test_euclidean_distance():
    db = load_files()
    dist = db.euclidean_distance('1', '2')
    print(dist)
    assert dist['dist'] - 0.1613 < 0.01

def test_num_items_test_files():
    db = load_files()
    assert len(db.users) == 10
    assert len(db.users['1'].ratings) == 272
    assert len(db.movies) == 691

def test_calculate_similarities():
    db = load_files()
    #pairings = db.calculate_similarities()
    #print(pairings, '\n Length: ', len(pairings))
    db.calculate_similarities()
    pprint(db.similarities)
    try:
        assert db.similarities[('9','8')]['dist'] - 0.1907 < 0.01
        assert db.similarities[('9','8')]['num_shared'] == 4
    except:
        assert db.similarities[('8','9')]['dist'] - 0.1907 < 0.01
        assert db.similarities[('8','9')]['num_shared'] == 4

def test_similar_users():
    db = load_files()
    db.calculate_similarities()
    assert (db.similar('2', n=5, min_matches=3))[0][0] == '5'
    print(db.similar('2'))
    assert True

def test_get_title():
    db = load_files()
    assert db.get_title('1') == 'Toy Story (1995)'

def test_sorted_ratings():
    db = load_files()
    srtd_ratings = db.users['1'].sort_ratings()
    print(srtd_ratings)
    assert True

def test_recommend_simple():
    db = load_files(movies_file='datasets/ml-100k/u.item')
    db.calculate_similarities()
    kml = db.recommend('1', n=20, mode='simple')
    pprint(kml)
    # assert len(kml) == 20
    # my_titles = [db.get_title(mid) for mid in db.users['1'].movies]
    my_movies = db.users['1'].movies
    # print('User 1 has seen {}'.format(sorted(my_movies, key=int)))
    for mid, score in kml:
        assert mid not in my_movies
    # assert False
    # User '1' has ratings for movies from 1 to 273

def test_recommend_simple_5_users():
    db = load_files(movies_file='datasets/ml-100k/u.item')
    db.calculate_similarities()
    kml = db.recommend('1', n=20, mode='simple', num_users=5)
    pprint(db.translate(data=kml, fn=db.get_title))
    # assert len(kml) == 20
    my_movies = db.users['1'].movies
    for mid, score in kml:
        assert mid not in my_movies


def test_recommend_simple_5_users_removes_dupes():
    db = load_files(movies_file='datasets/ml-100k/u.item')
    db.calculate_similarities()
    rec = db.recommend('5', n=20, mode='simple', num_users=5)
    movie_ids = [i[0] for i in rec]
    my_movies = db.users['5'].movies
    #pprint(movie_ids)
    assert len(list(set(movie_ids))) == len(movie_ids)
    for movie in movie_ids:
        assert movie not in my_movies
    pprint(db.translate(data=rec, fn=db.get_title))


def test_sanity_check():
    db = load_files(movies_file='datasets/ml-100k/u.item')
    db.calculate_similarities()
    user = '1'
    db.users[user].sort_ratings()
    rec = db.recommend(user, n=20, mode='simple', num_users=5)
    #pprint(vars(db.users['5']))
    print('Your favorite movies:\n', '*'*40)
    pprint(db.translate(db.users[user].my_favorites(n=20), fn=db.get_title))
    print('Your recommending movies:\n', '*'*40)
    pprint(db.translate(rec, fn=db.get_title)) # TODO: Add decorator for translate?
    assert True

"""
def test_full_data_set():
    # elapsed time for each function as of 5/16/2015:
    # load_files: 0.9330952167510986
    # calculate_similarities: 38.40591812133789
    # sort_ratings: 38.406957149505615
    # db.recommend: 38.493452072143555
    start = time.time()
    db = load_files(users_file='datasets/ml-100k/u.user',
                    movies_file='datasets/ml-100k/u.item',
                    ratings_file='datasets/ml-100k/u.data')
    print('load_files:', time.time() - start)
    db.calculate_similarities()
    print('calculate_similarities:', time.time() - start)
    user = '1'
    db.users[user].sort_ratings()
    print('sort_ratings:', time.time() - start)
    rec = db.recommend(user, n=20, mode='simple', num_users=5)
    print('db.recommend:', time.time() - start)
    print('Your favorite movies:\n', '*'*40)
    pprint(db.translate(db.users[user].my_favorites(n=20), fn=db.get_title))
    print('Your recommending movies:\n', '*'*40)
    pprint(db.translate(rec, fn=db.get_title)) # TODO: Add decorator for translate?
    print(time.time() - start)
    assert False
"""

def test_genres():
    db = load_files(movies_file='datasets/ml-100k/u.item')
    assert db.movies['100'].genres == ['Crime', 'Drama', 'Thriller']
#TODO: Add test that users[user_id].user_id == user_id

    #assert False
# def test_number_of_entries():
#     # Data from u.info
#     db = load_files()
#     assert len(db.users) == 943

"""
943 users
1682 items
100000 ratings
"""
##timeit test for db loading speed of full dataset
