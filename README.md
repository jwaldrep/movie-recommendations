#Movie Recommender (Flask) [![Build Status](https://travis-ci.org/jwaldrep/movie-recommendations.svg?branch=code_refresh)](https://travis-ci.org/jwaldrep/movie-recommendations)

##Description:
This is a very simple web app built in Flask, which uses the MoveLens dataset
of 100k user ratings of popular movies in order to make recommendations on
what movies a given user may want to watch. It was a quick(ish) weekend
experiment to make a web-driven interface to explore pure Python objects,
with no database on the backend. As a result, it will take a couple minutes
to load the first time, in order to build the network of recommendations.

##Requirements:
- Python 3 (3.4 recommended)
- [MovieLens](http://grouplens.org/datasets/movielens/)
  100k dataset (`ml-100k.zip`), unzipped into `./datasets/ml-100k`
- [Flask](http://flask.pocoo.org/)
    - Install via `pip3 install -r requirements.txt`

##Instructions:
1. Download/clone all files from this repo to your machine
2. Download and unzip the required dataset, described above
3. Run on the command line: "python3 ui.py"*
4. Open http://127.0.0.1:5000/ in a web browser window
5. Explore the site to find ratings for movies, movie rankings, and recommendations for each user based on their previous ratings

######* Note: This application is under development, and uses debug mode and as such, should not be used in a production environment!


####Acknowledgements:
The [MovieLens](http://grouplens.org/datasets/movielens/) data sets used for 
this project were collected by the [GroupLens Research Project]
(http://grouplens.org) at the University of Minnesota.

This work is neither endorsed nor sponsored by the University of Minnesota nor 
the GroupLens Research Group.

This project and the provided data are for non-commercial research purposes.
