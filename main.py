from flask import Flask, render_template, request
from youtubesearchpython import VideosSearch
import pandas
from waitress import serve

app = Flask('app')
def get_movie_trailer(movie_name):
    movie_name = str(movie_name) + ("trailer")
    vs = (VideosSearch(movie_name, limit = 1))
    vs = vs.result()
    return (vs['result'][0]['link'])
def format_date(date):
    date = date.replace('-', '/')
    date = date.split('/')
    date = [date[1], date[2], date[0]]
    date = '/'.join(date)
    return date


def Generate_Movie(Rating, Genre, Year, Language):
    filename = "mymoviedb.csv"
    df = pandas.read_csv(filename, lineterminator='\n')

    #Changing Variables
    Year = str(Year)
    Rating = float(Rating)
    lan_abr = {'english': 'en', 'hindi': 'hi', 'spanish': 'es', 'arabic': 'ar', 'bengali': 'bn', 'catalan': 'ca', 'chinese': 'zh', 'czech': 'cs', 'danish': 'da', 'german': 'de', 'greek': 'el', 'estonian': 'et', 'basque': 'eu', 'farsi': 'fa', 'finnish': 'fi', 'french': 'fr', 'hebrew': 'he', 'hungarian': 'hu', 'indonesian': 'id', 'icelandic': 'is', 'italian': 'it', 'japanese': 'ja', 'korean': 'ko', 'latin': 'la', 'latvian': 'lv', 'malayalam': 'ml', 'malay': 'ms', 'norwegian': 'no', 'dutch': 'nl', 'polish': 'pl', 'portuguese': 'pt', 'romanian': 'ro', 'russian': 'ru', 'serbian': 'sr', 'swedish': 'sv', 'tamil': 'ta', 'telugu': 'te', 'tagalog': 'tl', 'turkish': 'tr', 'ukrainian': 'uk'}
    Language = lan_abr[Language]
    #Sorting Rating
    def filter_rating(s, ch):
        return [i for i, ltr in enumerate(s) if ltr >= ch]
    sort_rating = ((df['Vote_Average']).where((df['Vote_Average']>=Rating)))

    #Sorting Genre
    def genre_conv(series):
        return (Genre) in (str(series))
    def filter_genre(s):
        return [i for i, ltr in enumerate(s) if (Genre) in (str(ltr))]
    sort_genre = ((df['Genre']).where(((df['Genre'].apply(genre_conv)))))

    #Sorting Year
    def year_conv(series):
        return ((str(series).split("-")[0]) == Year)
    def filter_year(s):
        return [i for i, ltr in enumerate(s) if (str(ltr)).split("-")[0] == Year]
    sort_year = ((df['Release_Date']).where(((df['Release_Date'].apply(year_conv)))))

    #Sorting Year
    def lang_conv(series):
        return (str(series) == Language)
    def filter_lang(s):
        return [i for i, ltr in enumerate(s) if (str(ltr) == Language)]
    sort_lang = ((df['Original_Language']).where(((df['Original_Language'].apply(lang_conv)))))



    try:
        #Filtering Data
        index_genre = set(filter_genre(sort_genre.to_list()))
        index_rating = set(filter_rating(sort_rating.to_list(), Rating))
        index_year = set(filter_year(sort_year.to_list()))
        index_lang = set(filter_lang(sort_lang.to_list()))

        #Finding Common Filtered Data in all Categories
        common_index = index_genre.intersection(index_rating)
        common_index = common_index.intersection(index_year)
        common_index = common_index.intersection(index_lang)
        final_indices = list(common_index)
        RESULTS = []
        #Adding the Dict type data to Results List
        for item in final_indices:
            RESULTS.append(df.loc[item].to_dict())
        return RESULTS

    except Exception:
        #Returning None if any error occurs
        RESULTS = None
        return None
      
@app.route('/generate', methods = ['POST', 'GET'])
def Generate_Formatted():
  if request.method == "POST":
    Rating = request.form['rating']
    print(Rating)
    Genre = request.form['genre']
    print(Genre)
    Year = request.form['year']
    print(Year)
    Language = request.form['language']
    print(Language)
    movies = Generate_Movie(Rating, Genre, Year, Language)
    names = []
    years_released = []
    descriptions = []
    genres = []
    ratings = []
    links = []
    # rating_percentages = []
    cover_art = []
    for i in range(len(movies)):
      names.append(movies[i]['Title'])
      years_released.append(movies[i]['Release_Date'])
      descriptions.append(movies[i]['Overview'])
      genres.append(movies[i]['Genre'])
      ratings.append(movies[i]['Vote_Average'])
      cover_art.append(movies[i]['Poster_Url'])
      links.append(get_movie_trailer(movies[i]['Title']))    
    if names == []:
      return render_template('nonefound.html')
    else:
      for i in range(0, len(years_released)):
        years_released[i] = format_date(years_released[i])
      return render_template('results.html', names=names, years_released=years_released, descriptions=descriptions, genres=genres, ratings=ratings, coverart=cover_art, num=len(movies), links=links)



@app.route('/', methods = ['POST', 'GET'])
def index():
  genrelist = ["Action", "Adventure", "Animation", "Comedy", "Crime", "Drama", "Family", "Fantasy", "History", "Horror", "Music", "Mystery", "Romance", "Science Fiction", "Thriller", "TV Movie", "War", "Western"]
  languages = {
    'en':'English',
    'hi':'Hindi',
    'es':'Spanish', 
    'ar':'Arabic', 
    'bn':'Bengali', 
    'ca':'Catalan',
    'cn':'Chinese',
    'cs':'Czech',
    'da':'Danish',
    'de':'German', 
    'el':'Greek', 
    'et':'Estonian', 
    'eu':'Basque', 
    'fa':'Farsi', 
    'fi':'Finnish', 
    'fr':'French', 
    'he':'Hebrew',
    'hu':'Hungarian', 
    'id':'Indonesian', 
    'is':'Icelandic', 
    'it':'Italian', 
    'ja':'Japanese', 
    'ko':'Korean', 
    'la':'Latin', 
    'lv':'Latvian', 
    'ml':'Malayalam', 
    'ms':'Malay', 
    'nb':'Norwegian', 
    'nl':'Dutch', 
    'no':'Norwegian', 
    'pl':'Polish', 
    'pt':'Portuguese', 
    'ro':'Romanian', 
    'ru':'Russian', 
    'sr':'Serbian', 
    'sv':'Swedish', 
    'ta':'Tamil', 
    'te':'Telugu', 
    'th':'Tagalog', 
    'tl':'Tagalog', 
    'tr':'Turkish', 
    'uk':'Ukrainian', 
    'zh':'Chinese'
  }

  keys = list(languages.keys())
  langs = list(languages.values())
  return render_template("index.html", genrelist = genrelist, keys=keys, langs=langs)

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('e404.html'), 404

@app.route('/about')
def about():
  return render_template('about.html')


serve(app, host='0.0.0.0', port=8080)