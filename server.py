from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'anime'
print("hello")
mysql = MySQL(app)

def add_user():
    username = request.form['username']
    password = request.form['password']
    job = request.form['job']

    cursor = mysql.connection.cursor()
    query = "INSERT INTO users (username, password, job) VALUES (%s, %s, %s)"
    cursor.execute(query, (username, password, job))
    mysql.connection.commit()
    cursor.close()

    return {'success': True}

def get_user(id):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM users WHERE id = %s"
    cursor.execute(query, (id,))
    user = cursor.fetchone()
    cursor.close()

    return user or 404

def add_image(image_url, small_image_url, large_image_url):
    cursor = mysql.connection.cursor()
    query = "INSERT INTO images (image_url, small_image_url, large_image_url) VALUES (%s, %s, %s)"
    cursor.execute(query, (image_url, small_image_url, large_image_url))
    mysql.connection.commit()
    cursor.close()

def get_image(id):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM images WHERE id = %s"
    cursor.execute(query, (id,))
    image = cursor.fetchone()
    cursor.close()
    return image


def add_other_title(ttype, title):
    cursor = mysql.connection.cursor()
    query = "INSERT INTO otherTitles (ttype, title) VALUES (%s, %s)"
    cursor.execute(query, (ttype, title))
    mysql.connection.commit()
    cursor.close()
    
def get_other_title(id):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM otherTitles WHERE id = %s"
    cursor.execute(query, (id,))
    user = cursor.fetchone()
    cursor.close()
    return user


def add_aired_date(from_date, to_date):
    cursor = mysql.connection.cursor()
    query = "INSERT INTO airedDates (from_date, to_date) VALUES (%s, %s)"
    cursor.execute(query, (from_date, to_date))
    mysql.connection.commit()
    cursor.close()

def get_aired_date(id):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM airedDates WHERE id = %s"
    cursor.execute(query, (id,))
    aired_date = cursor.fetchone()
    cursor.close()
    return aired_date

def add_producer(ptype, name):
    cursor = mysql.connection.cursor()
    query = "INSERT INTO producers (ptype, name) VALUES (%s, %s)"
    cursor.execute(query, (ptype, name))
    mysql.connection.commit()
    cursor.close()

def get_producer(id):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM producers WHERE id = %s"
    cursor.execute(query, (id,))
    producer = cursor.fetchone()
    cursor.close()
    return producer


def add_studio(stype, name):
    cursor = mysql.connection.cursor()
    query = "INSERT INTO studios (stype, name) VALUES (%s, %s)"
    cursor.execute(query, (stype, name))
    mysql.connection.commit()
    cursor.close()

def get_studio(id):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM studios WHERE id = %s"
    cursor.execute(query, (id,))
    studio = cursor.fetchone()
    cursor.close()
    return studio

def add_genre(gtype, name):
    cursor = mysql.connection.cursor()
    query = "INSERT INTO genres (gtype, name) VALUES (%s, %s)"
    cursor.execute(query, (gtype, name))
    mysql.connection.commit()
    cursor.close()

def get_genre(id):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM genres WHERE id = %s"
    cursor.execute(query, (id,))
    genre = cursor.fetchone()
    cursor.close()
    return genre

def add_anime_relation(relation_type, mal_id, related_type, name, url):
    cursor = mysql.connection.cursor()
    query = """
    INSERT INTO relations (relation_type, mal_id, related_type, name, url) 
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (relation_type, mal_id, related_type, name, url))
    mysql.connection.commit()
    cursor.close()
    
def get_anime_relation(id):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM relations WHERE id = %s"
    cursor.execute(query, (id,))
    relation = cursor.fetchone()
    cursor.close()
    return relation

def add_anime(title, atype, episodes, status, duration, rating, score, scoredBy, rank, popularity, favorites, members, synopsis):
    cursor = mysql.connection.cursor()
    query = """
    INSERT INTO animes (title, atype, episodes, status, duration, rating, score, scoredBy, rank, popularity, favorites, members, synopsis) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (title, atype, episodes, status, duration, rating, score, scoredBy, rank, popularity, favorites, members, synopsis))
    mysql.connection.commit()
    cursor.close()

def get_anime(id):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM animes WHERE id = %s"
    cursor.execute(query, (id,))
    anime = cursor.fetchone()
    cursor.close()
    return anime

################################################################################################### iletisimler
@app.route('/api/users/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    cursor = mysql.connection.cursor()
    query = "SELECT id ,password, job FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    cursor.close()
    [strReturn, job] = [str(user[0]), user[2]]
    if user and user[0] and user[1] == password:
        return [strReturn, job]
        
    return 'n o'

@app.route('/api/users/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    confirmed_password = data['passwordConfirm']
    job = 'user'

    if password != confirmed_password:
        return jsonify({'error': 'Passwords do not match'}), 400
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        return jsonify({'error': 'Username already exists'}), 400

    query = "INSERT INTO users (username, password, job) VALUES (%s, %s, %s)"
    cursor.execute(query, (username, password, job))
    mysql.connection.commit()
    cursor.close()

    return 'hahahah'

def tuple_to_dict(keys, tuple_data):
    return {keys[i]: tuple_data[i] for i in range(len(keys))}

@app.route('/api/animes/<int:id>', methods=['GET'])
def get_animes_for_main_page(id):
    offset = (id - 1) * 101
    cursor = mysql.connection.cursor()
    query_animes = "SELECT * FROM Animes, Images WHERE Animes.id = Images.anime_id ORDER BY Animes.id LIMIT 101 OFFSET %s"
    cursor.execute(query_animes, (offset,))
    animes_tuples = cursor.fetchall()
    keys = [desc[0] for desc in cursor.description]  # Get column names

    animes = [tuple_to_dict(keys, anime) for anime in animes_tuples]

    # For each anime, fetch additional details from other tables
    for anime in animes:
        anime_id = anime['id']  # Adjust based on your column name

        # Fetch genres
        cursor.execute("SELECT name FROM genres WHERE anime_id = %s", (anime_id,))
        genres = cursor.fetchall()
        anime['genres'] = [genre[0] for genre in genres]

        # Fetch aired dates
        cursor.execute("SELECT from_date, to_date FROM airedDates WHERE anime_id = %s", (anime_id,))
        aired_dates = cursor.fetchall()
        anime['aired_dates'] = aired_dates

        # Fetch producers
        cursor.execute("SELECT name FROM producers WHERE anime_id = %s", (anime_id,))
        producers = cursor.fetchall()
        anime['producers'] = [producer[0] for producer in producers]

        # Fetch studios
        cursor.execute("SELECT name FROM studios WHERE anime_id = %s", (anime_id,))
        studios = cursor.fetchall()
        anime['studios'] = [studio[0] for studio in studios]

        # Similarly fetch other details as needed

    cursor.close()
    return jsonify(animes)


@app.route('/api/animes/popular/<int:id>', methods=['GET'])
def get_popular_animes(id):
    offset = (id - 1) * 101  
    cursor = mysql.connection.cursor()
    query_animes = "SELECT * FROM Animes, Images WHERE Animes.id = Images.Anime_ID ORDER BY Animes.popularity DESC LIMIT 101 OFFSET %s"
    cursor.execute(query_animes, (offset,))
    animes_tuples = cursor.fetchall()
    keys = [desc[0] for desc in cursor.description]  # Get column names

    animes = [tuple_to_dict(keys, anime) for anime in animes_tuples]

    # For each anime, fetch additional details from other tables
    for anime in animes:
        anime_id = anime['id']  # Adjust based on your column name

        # Fetch genres
        cursor.execute("SELECT name FROM genres WHERE anime_id = %s", (anime_id,))
        genres = cursor.fetchall()
        anime['genres'] = [genre[0] for genre in genres]

        # Fetch aired dates
        cursor.execute("SELECT from_date, to_date FROM airedDates WHERE anime_id = %s", (anime_id,))
        aired_dates = cursor.fetchall()
        anime['aired_dates'] = aired_dates

        # Fetch producers
        cursor.execute("SELECT name FROM producers WHERE anime_id = %s", (anime_id,))
        producers = cursor.fetchall()
        anime['producers'] = [producer[0] for producer in producers]

        # Fetch studios
        cursor.execute("SELECT name FROM studios WHERE anime_id = %s", (anime_id,))
        studios = cursor.fetchall()
        anime['studios'] = [studio[0] for studio in studios]

        # Similarly fetch other details as needed

    cursor.close()
    return jsonify(animes)


@app.route('/api/animes/most-liked/<int:id>', methods=['GET'])
def get_most_liked_animes(id):
    cursor = mysql.connection.cursor()
    offset = (id - 1) * 101  
    query_animes = "SELECT * FROM Animes, Images WHERE Animes.id = Images.Anime_ID ORDER BY Animes.scoredBy DESC LIMIT 101 OFFSET %s"
    cursor.execute(query_animes, (offset,))
    animes_tuples = cursor.fetchall()
    keys = [desc[0] for desc in cursor.description]  # Get column names

    animes = [tuple_to_dict(keys, anime) for anime in animes_tuples]

    # For each anime, fetch additional details from other tables
    for anime in animes:
        anime_id = anime['id']  # Adjust based on your column name

        # Fetch genres
        cursor.execute("SELECT name FROM genres WHERE anime_id = %s", (anime_id,))
        genres = cursor.fetchall()
        anime['genres'] = [genre[0] for genre in genres]

        # Fetch aired dates
        cursor.execute("SELECT from_date, to_date FROM airedDates WHERE anime_id = %s", (anime_id,))
        aired_dates = cursor.fetchall()
        anime['aired_dates'] = aired_dates

        # Fetch producers
        cursor.execute("SELECT name FROM producers WHERE anime_id = %s", (anime_id,))
        producers = cursor.fetchall()
        anime['producers'] = [producer[0] for producer in producers]

        # Fetch studios
        cursor.execute("SELECT name FROM studios WHERE anime_id = %s", (anime_id,))
        studios = cursor.fetchall()
        anime['studios'] = [studio[0] for studio in studios]

        # Similarly fetch other details as needed

    cursor.close()
    return jsonify(animes)

@app.route('/api/animes/most-watched/<int:id>', methods=['GET'])
def get_most_watched_animes(id):
    offset = (id - 1) * 101 
    cursor = mysql.connection.cursor()
    query_animes = "SELECT * FROM Animes, Images WHERE Animes.id = Images.anime_id ORDER BY Animes.members DESC LIMIT 101 OFFSET %s"
    cursor.execute(query_animes, (offset,))
    animes_tuples = cursor.fetchall()
    keys = [desc[0] for desc in cursor.description]  # Get column names

    animes = [tuple_to_dict(keys, anime) for anime in animes_tuples]

    # For each anime, fetch additional details from other tables
    for anime in animes:
        anime_id = anime['id']  # Adjust based on your column name

        # Fetch genres
        cursor.execute("SELECT name FROM genres WHERE anime_id = %s", (anime_id,))
        genres = cursor.fetchall()
        anime['genres'] = [genre[0] for genre in genres]

        # Fetch aired dates
        cursor.execute("SELECT from_date, to_date FROM airedDates WHERE anime_id = %s", (anime_id,))
        aired_dates = cursor.fetchall()
        anime['aired_dates'] = aired_dates

        # Fetch producers
        cursor.execute("SELECT name FROM producers WHERE anime_id = %s", (anime_id,))
        producers = cursor.fetchall()
        anime['producers'] = [producer[0] for producer in producers]

        # Fetch studios
        cursor.execute("SELECT name FROM studios WHERE anime_id = %s", (anime_id,))
        studios = cursor.fetchall()
        anime['studios'] = [studio[0] for studio in studios]

        # Similarly fetch other details as needed

    cursor.close()
    return jsonify(animes)


@app.route('/api/remove_anime/<int:anime_id>', methods=['DELETE'])
def remove_anime(anime_id):
    cursor = mysql.connection.cursor()
    query = "DELETE FROM Animes WHERE id = %s"
    cursor.execute(query, (anime_id,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'Anime removed successfully'})


@app.route('/api/admin/search_anime', methods=['POST'])
def search_anime():
    search_term = request.get_json()['searchTerm']
    cursor = mysql.connection.cursor()
    query = "SELECT id, title FROM Animes WHERE title LIKE %s"
    cursor.execute(query, ('%' + search_term + '%',))
    animes = cursor.fetchall()
    cursor.close()
    return jsonify(animes)

@app.route('/api/animes/genre/<string:genre>/<int:id>', methods=['GET'])
def get_animes_by_genre(genre, id):
    offset = (id - 1) * 101
    cursor = mysql.connection.cursor()
    
    query_animes = """
    SELECT Animes.*, Images.* FROM Animes
    JOIN Images ON Animes.id = Images.anime_id
    JOIN genres ON Animes.id = genres.anime_id
    WHERE genres.name LIKE %s
    LIMIT 101 OFFSET %s
    """
    
    cursor.execute(query_animes, ('%' + genre + '%', offset))
    animes_tuples = cursor.fetchall()
    keys = [desc[0] for desc in cursor.description]  # Get column names

    animes = [tuple_to_dict(keys, anime) for anime in animes_tuples]

    # For each anime, fetch additional details from other tables
    for anime in animes:
        anime_id = anime['id']  # Adjust based on your column name

        # Fetch genres
        cursor.execute("SELECT name FROM genres WHERE anime_id = %s", (anime_id,))
        genres = cursor.fetchall()
        anime['genres'] = [genre[0] for genre in genres]

        # Fetch aired dates
        cursor.execute("SELECT from_date, to_date FROM airedDates WHERE anime_id = %s", (anime_id,))
        aired_dates = cursor.fetchall()
        anime['aired_dates'] = aired_dates

        # Fetch producers
        cursor.execute("SELECT name FROM producers WHERE anime_id = %s", (anime_id,))
        producers = cursor.fetchall()
        anime['producers'] = [producer[0] for producer in producers]

        # Fetch studios
        cursor.execute("SELECT name FROM studios WHERE anime_id = %s", (anime_id,))
        studios = cursor.fetchall()
        anime['studios'] = [studio[0] for studio in studios]

        # Similarly fetch other details as needed

    cursor.close()
    return jsonify(animes)

@app.route('/api/animes/airing/<int:id>', methods=['GET'])
def get_airing_animes(id):
    offset = (id - 1) * 101 
    cursor = mysql.connection.cursor()
    query_animes = "SELECT * FROM Animes, Images WHERE Animes.id = Images.anime_id AND Animes.status = 'Currently Airing' LIMIT 101 OFFSET %s"
    cursor.execute(query_animes, (offset,))
    animes_tuples = cursor.fetchall()
    keys = [desc[0] for desc in cursor.description]  # Get column names

    animes = [tuple_to_dict(keys, anime) for anime in animes_tuples]

    # For each anime, fetch additional details from other tables
    for anime in animes:
        anime_id = anime['id']  # Adjust based on your column name

        # Fetch genres
        cursor.execute("SELECT name FROM genres WHERE anime_id = %s", (anime_id,))
        genres = cursor.fetchall()
        anime['genres'] = [genre[0] for genre in genres]

        # Fetch aired dates
        cursor.execute("SELECT from_date, to_date FROM airedDates WHERE anime_id = %s", (anime_id,))
        aired_dates = cursor.fetchall()
        anime['aired_dates'] = aired_dates

        # Fetch producers
        cursor.execute("SELECT name FROM producers WHERE anime_id = %s", (anime_id,))
        producers = cursor.fetchall()
        anime['producers'] = [producer[0] for producer in producers]

        # Fetch studios
        cursor.execute("SELECT name FROM studios WHERE anime_id = %s", (anime_id,))
        studios = cursor.fetchall()
        anime['studios'] = [studio[0] for studio in studios]

        # Similarly fetch other details as needed

    cursor.close()
    return jsonify(animes)

@app.route('/api/animes/search/<int:id>', methods=['POST'])
def get_animes_by_search(id):
    search = request.get_json()['searchTerm']
    offset = (id - 1) * 101 
    cursor = mysql.connection.cursor()
    query_animes = "SELECT * FROM Animes, Images WHERE Animes.id = Images.anime_id AND Animes.title LIKE %s LIMIT 101 OFFSET %s"
    cursor.execute(query_animes, ('%' + search + '%', offset))  # Combine parameters into one tuple
    animes_tuples = cursor.fetchall()
    keys = [desc[0] for desc in cursor.description]  # Get column names

    animes = [tuple_to_dict(keys, anime) for anime in animes_tuples]

    # For each anime, fetch additional details from other tables
    for anime in animes:
        anime_id = anime['id']  # Adjust based on your column name

        # Fetch genres
        cursor.execute("SELECT name FROM genres WHERE anime_id = %s", (anime_id,))
        genres = cursor.fetchall()
        anime['genres'] = [genre[0] for genre in genres]

        # Fetch aired dates
        cursor.execute("SELECT from_date, to_date FROM airedDates WHERE anime_id = %s", (anime_id,))
        aired_dates = cursor.fetchall()
        anime['aired_dates'] = aired_dates

        # Fetch producers
        cursor.execute("SELECT name FROM producers WHERE anime_id = %s", (anime_id,))
        producers = cursor.fetchall()
        anime['producers'] = [producer[0] for producer in producers]

        # Fetch studios
        cursor.execute("SELECT name FROM studios WHERE anime_id = %s", (anime_id,))
        studios = cursor.fetchall()
        anime['studios'] = [studio[0] for studio in studios]
        
    
    cursor.close()
    return jsonify(animes)

@app.route('/api/animes/search/<string:genre>/<int:id>', methods=['GET'])
def get_searched_animes_by_genre(search, genre):
    offset = (id - 1) * 101 
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM Animes, Images WHERE Animes.id = Images.anime_id AND Animes.title LIKE %s AND Animes.Genre LIKE %s LIMIT 101 OFFSET %s"
    cursor.execute(query, ('%' + search + '%', '%' + genre + '%',), (offset,))
    animes = cursor.fetchall()
    cursor.close()
    return jsonify(animes)

@app.route('/api/animes/<int:id>', methods=['GET'])
def add_rating():
    anime_id = request.form['anime_id']
    user_id = request.form['user_id']
    rating = request.form['rating']
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM Ratings WHERE Anime_ID = %s AND User_ID = %s"
    cursor.execute(query, (anime_id, user_id))
    if cursor.fetchone():
        query = "UPDATE Ratings SET Rating = %s WHERE Anime_ID = %s AND User_ID = %s"
        cursor.execute(query, (rating, anime_id, user_id))
        mysql.connection.commit()
        cursor.close()
        return 200
    query1 = "INSERT INTO Ratings (Anime_ID, User_ID, Rating) VALUES (%s, %s, %s)"
    cursor.execute(query, (anime_id, user_id, rating))
    mysql.connection.commit()
    cursor.close()
    return 200

@app.route('/api/genres/names', methods=['GET'])
def get_unique_genre_names():
    cursor = mysql.connection.cursor()
    query = "SELECT DISTINCT name FROM genres"
    cursor.execute(query)
    genres = cursor.fetchall()
    cursor.close()
    genre_names = [genre[0] for genre in genres]
    return jsonify(genre_names)

@app.route('/api/animes/count', methods=['GET'])
def get_anime_count():
    cursor = mysql.connection.cursor()
    query = "SELECT COUNT(*) FROM animes"
    cursor.execute(query)
    count = cursor.fetchone()[0]
    cursor.close()
    return jsonify({'anime_count': count})

@app.route('/api/animes/content/rate', methods=['POST'])
def rate_anime():
    
    data = request.get_json()
    anime_id = data['anime_id']
    user_id = data['user_id']
    rating = data['rating']
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM Ratings WHERE Anime_ID = %s AND User_ID = %s"
    cursor.execute(query, (anime_id, user_id))
    if cursor.fetchone():
        query = "UPDATE Ratings SET Rating = %s WHERE Anime_ID = %s AND User_ID = %s"
        cursor.execute(query, (rating, anime_id, user_id))
        mysql.connection.commit()
        cursor.close()
        return {'success': True}
    query1 = "INSERT INTO Ratings (Anime_ID, User_ID, Rating) VALUES (%s, %s, %s)"
    cursor.execute(query1, (anime_id, user_id, rating))  # Use query1 here
    mysql.connection.commit()
    cursor.close()
    return {'success': True}

@app.route('/api/animes/content/getrate', methods=['POST'])
def get_rating():
    data = request.get_json()
    anime_id = data['anime_id']
    user_id = data['user_id']
    print(user_id)
    cursor = mysql.connection.cursor()
    query = "SELECT Rating FROM Ratings WHERE Anime_ID = %s AND User_ID = %s"
    cursor.execute(query, (anime_id, user_id))
    rating = cursor.fetchone()
    cursor.close()
    if rating:
        return str(rating[0])
    return {'success': False}, 404

from flask import request, jsonify

@app.route('/add_anime', methods=['POST'])
def add_anime():
    # Extract data from request
    data = request.json
    title = data.get('title')
    atype = data.get('category')
    episodes = data.get('episodes')
    status = data.get('status')
    duration = data.get('duration')
    rating = data.get('rating')
    score = 0
    scoredBy = 0
    rank = 0
    popularity = 0
    favorites = 0
    members = data.get('members')
    synopsis = data.get('summary')
    
    animeTypes = data.get('animeType')
    producers = data.get('producers')
    otherTitles = data.get('otherTitles')
    image = data.get('imageLink')
    airedDates = [data.get('fromDate'), data.get('toDate')]
    studios = data.get('studios')

    cursor = mysql.connection.cursor()
    query_anime = """
    INSERT INTO animes (title, atype, episodes, status, duration, rating, score, scoredBy, arank, popularity, favorites, members, synopsis) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query_anime, (title, atype, episodes, status, duration, rating, score, scoredBy, rank, popularity, favorites, members, synopsis))
    anime_id = cursor.lastrowid  # Capture the last inserted id

    # Insert related data into other tables
    insert_genres(animeTypes, cursor, anime_id)
    insert_producers(producers, cursor, anime_id)
    insert_other_titles(otherTitles, cursor, anime_id)
    insert_image_data(image, cursor, anime_id)
    insert_aired_dates(airedDates, cursor, anime_id)
    insert_studios(studios, cursor, anime_id)

    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'Anime added successfully', 'anime_id': anime_id}), 201



def insert_genres(genre_data, cursor, anime_id):
    for genre_type in genre_data:
        query = "INSERT INTO genres (gtype, name, anime_id) VALUES (%s, %s, %s)"
        cursor.execute(query, ('anime', genre_type[0], anime_id))

def insert_producers(producer_data, cursor, anime_id):
    for producer in producer_data:
        query = "INSERT INTO producers (ptype, name, anime_id) VALUES (%s, %s, %s)"
        cursor.execute(query, ('anime', producer[0], anime_id))

def insert_other_titles(other_titles_data, cursor, anime_id):
    for other_title in other_titles_data:
        query = "INSERT INTO otherTitles (ttype, title, anime_id) VALUES (%s, %s, %s)"
        cursor.execute(query, (other_title[0], other_title[0], anime_id))

def insert_image_data(image_data, cursor, anime_id):
    query = "INSERT INTO images (image_url, small_image_url, large_image_url, anime_id) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (image_data, image_data, image_data, anime_id))

def insert_aired_dates(aired_dates_data, cursor, anime_id):
    query = "INSERT INTO airedDates (from_date, to_date, anime_id) VALUES (%s, %s, %s)"
    cursor.execute(query, (aired_dates_data[0], aired_dates_data[1], anime_id))

def insert_studios(studio_data, cursor, anime_id):
    for studio in studio_data:
        query = "INSERT INTO studios (stype, name, anime_id) VALUES (%s, %s, %s)"
        cursor.execute(query, ('anime', studio[0], anime_id))
        
@app.route('/api/animes/types', methods=['GET'])
def get_unique_anime_types():
    cursor = mysql.connection.cursor()
    query = "SELECT DISTINCT atype FROM animes"
    cursor.execute(query)
    anime_types = cursor.fetchall()
    cursor.close()
    return jsonify([atype[0] for atype in anime_types])

@app.route('/api/genres/types', methods=['GET'])
def get_unique_genre_types():
    cursor = mysql.connection.cursor()
    query = "SELECT DISTINCT name FROM genres"
    cursor.execute(query)
    genre_types = cursor.fetchall()
    cursor.close()
    return jsonify([gtype[0] for gtype in genre_types])

@app.route('/api/animes/ratings', methods=['GET'])
def get_unique_anime_ratings():
    cursor = mysql.connection.cursor()
    query = "SELECT DISTINCT rating FROM animes"
    cursor.execute(query)
    ratings = cursor.fetchall()
    cursor.close()
    return jsonify([rating[0] for rating in ratings])

@app.route('/api/animes/statuses', methods=['GET'])
def get_unique_anime_statuses():
    cursor = mysql.connection.cursor()
    query = "SELECT DISTINCT status FROM animes"
    cursor.execute(query)
    statuses = cursor.fetchall()
    cursor.close()
    return jsonify([status[0] for status in statuses])


if __name__ == '__main__':
    app.run()
