from youtubesearchpython import VideosSearch
def get_movie_trailer(movie_name):
    movie_name = str(movie_name) + ("trailer")
    vs = (VideosSearch(movie_name, limit = 1))
    vs = vs.result()
    return (vs['result'][0]['link'])
links = []
movies = ["Dune", "Jumanji", "Avengers: Endgame"]
for i in range(len(movies)):
  links.append(get_movie_trailer(movies[i]))
print(links)