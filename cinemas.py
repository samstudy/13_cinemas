import requests
import re
import itertools
from bs4 import BeautifulSoup


def parse_afisha_page():
    inf_from_url = requests.get('https://www.afisha.ru/msk/schedule_cinema/')
    soup = BeautifulSoup(inf_from_url.content, 'lxml')
    raw_afisha_inf = soup.find_all('div',{'class':'object s-votes-hover-area collapsed'})
    return raw_afisha_inf


def get_movie_name_cinema_count():
    movie_name_cinema_count = []
    movies = parse_afisha_page()
    for movie in movies:
        movie_store = {
            'movie_name': movie.find('h3',{'class':'usetags'}).findNext('a').text,
            'count_of_cinema': len(movie.find_all('tr'))}
        movie_name_cinema_count.append(movie_store )
    return movie_name_cinema_count


def get_rating_and_counting_ball(movie):
    payload = {'kp_query':movie, 'first':'yes'}
    movie_html = requests.get('https://www.kinopoisk.ru/index.php', params=payload)
    soup = BeautifulSoup(movie_html.content, 'lxml')
    movie_kpi = {
        'movie_rating': get_movie_rating(soup),
        'movie_votes': get_movie_votes(soup)
    }
    return movie_kpi


def get_movie_rating(movie):
    rating = movie.find('span',{'class':'rating_ball'})
    return float(rating.text) if rating else 0


def get_movie_votes(movie):
    votes = movie.find('span',{'class':'ratingCount'})
    return int(re.sub('\s+','',votes.text)) if votes else 0


def collect_movie_information():
    movies_store = []
    movies = get_movie_name_cinema_count()
    for movie in movies:
        movie_rate = get_rating_and_counting_ball(movie['movie_name'])
        movies_store.append({
            'title': movie['movie_name'],
            'cinema_count': movie['count_of_cinema'],
            'rating': movie_rate['movie_rating'],
            'votes': movie_rate['movie_votes']
        })
    return movies_store


def show_to_console(movie_information):
    _best_kpi = 10
    sorted_movies = sorted(movie_information, key=lambda elem: elem['rating'], reverse=True)[:_best_kpi]
    for movie in sorted_movies:
        for attribute,value in movie.items():
            print('{} : {}'.format(attribute, value))


if __name__ == '__main__':
    movie_information = collect_movie_information()
    show_to_console(movie_information)