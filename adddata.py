import requests
import pymysql

def fetch_anime_data():
    url = f"https://api.jikan.moe/v4/top/anime"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['data']
    else:
        return None

def fetch_anime_data2(id):
    url = f"https://api.jikan.moe/v4/anime/{id}/full"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['data']
    else:
        return None

def insert_anime_data_to_db(anime_data, db_cursor):
    # Example: Inserting into the 'animes' table
    query = """
    INSERT INTO animes (title, atype, episodes, status, duration, rating, score, scoredBy, arank, popularity, favorites, members, synopsis) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    db_cursor.execute(query, (
        anime_data['title'], 
        anime_data['type'], 
        anime_data['episodes'], 
        anime_data['status'], 
        anime_data['duration'], 
        anime_data['rating'], 
        anime_data['score'], 
        anime_data['scored_by'], 
        anime_data['rank'], 
        anime_data['popularity'], 
        anime_data['favorites'], 
        anime_data['members'], 
        anime_data['synopsis']
    ))
def insert_image_data(anime_data, cursor, counter):
    # Insert into 'images' table
    images = anime_data['images']['jpg']
    query = "INSERT INTO images (image_url, small_image_url, large_image_url, anime_id) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (images['image_url'], images['small_image_url'], images['large_image_url'], counter))

def insert_other_titles(anime_data, cursor, counter):
    # Insert into 'otherTitles' table
    for title in anime_data['titles']:
        query = "INSERT INTO otherTitles (ttype, title, anime_id) VALUES (%s, %s, %s)"
        cursor.execute(query, (title['type'], title['title'], counter))

def insert_producers(anime_data, cursor, counter):
    # Insert into 'producers' table
    for producer in anime_data['producers']:
        query = "INSERT INTO producers (ptype, name, anime_id) VALUES (%s, %s, %s)"
        cursor.execute(query, (producer['type'], producer['name'], counter))
        
def insert_studios(anime_data, cursor, counter):
    for studio in anime_data['studios']:
        query = "INSERT INTO studios (stype, name, anime_id) VALUES (%s, %s, %s)"
        cursor.execute(query, (studio['type'], studio['name'], counter))

def insert_genres(anime_data, cursor, counter):
    # Collect all genre-related items
    genre_items = []
    genre_items.extend(anime_data['genres'])
    genre_items.extend(anime_data['explicit_genres'])
    genre_items.extend(anime_data['themes'])
    genre_items.extend(anime_data['demographics'])
    # Prepare and execute the insertion query for each item
    query = "INSERT INTO genres (gtype, name, anime_id) VALUES (%s, %s, %s)"
    for item in genre_items:
        cursor.execute(query, (item['type'], item['name'], counter))

def insert_aired_dates(anime_data, cursor, counter):
    aired = anime_data['aired']
    query = "INSERT INTO airedDates (from_date, to_date, anime_id) VALUES (%s, %s, %s)"
    cursor.execute(query, (aired['from'], aired['to'], counter))

def insert_relations(anime_data, cursor, counter):
    for relation in anime_data['relations']:
        for entry in relation['entry']:
            query = "INSERT INTO relations (relation_type, mal_id, related_type, name, url, anime_id) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (relation['relation'], entry['mal_id'], entry['type'], entry['name'], entry['url'], counter))


def main():
    # Database connection
    db_conn = pymysql.connect(host='127.0.0.1', user='root', password='root', db='anime')
    cursor = db_conn.cursor()
    anime_data = fetch_anime_data()
    for a_data in anime_data:
        cursor.execute("SELECT id FROM animes WHERE id = %s", (a_data['mal_id'],))
        existing_anime = cursor.fetchone()

        if existing_anime is None:
            real_data = fetch_anime_data2(a_data['mal_id'])
            if real_data is not None:
                print('asd')
                insert_anime_data_to_db(real_data, cursor)
                last_inserted_id = cursor.lastrowid
                insert_image_data(real_data, cursor, last_inserted_id)
                insert_other_titles(real_data, cursor, last_inserted_id)
                insert_producers(real_data, cursor, last_inserted_id)
                insert_studios(real_data, cursor, last_inserted_id)
                insert_genres(real_data, cursor, last_inserted_id)
                insert_aired_dates(real_data, cursor, last_inserted_id)
                insert_relations(real_data, cursor, last_inserted_id)
                db_conn.commit()
        else:   
            pass

    cursor.close()
    db_conn.close()

if __name__ == "__main__":
    main()
