from load_9mois_tables import *
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

# Update French Stop Words in Meilisearch dictionary
def update_stopwords(language="french"):

    with open("stopwords-fr.json") as file_stop_words:
        stop_words = json.load(file_stop_words)
    return stop_words

stop_words = update_stopwords()

# Create vector

vector = {}
vector_class = {'food': [], 'recipes': [],'articles': [], 'questions': []}
score = {}
score_similarity = {'food': [], 'recipes': [],'articles': [], 'questions': []}

def vectorize (query):
# Récupérer l'ensemble des données et les enregistrer dans des variables
    data = {}
    for table in tables:
        table_name = tables[table]['table_name']
        fields = tables[table]['fields']
        data[table_name] = table_to_json(table_name, fields)
        data[table_name] = json.loads(data[table_name])
# Vectorize results
    for table in data:
        for row in data[table]:
            vector = {}
            score = {}
            # Create vectorizer
            vectorizer = TfidfVectorizer(stop_words=stop_words, token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z_-]+\b")
            if 'id' in row:
                id = row['id']
            else:
                id = row['code']
            line = ' '.join(field for field in row.values() if field is not None)
            vector[id] = vectorizer.fit_transform([line])
            # vector_class[table].append(vector)
            vector_query = vectorizer.transform([query])
            similarity = np.dot(vector[id], vector_query.T).toarray()[0][0]
            score[id] = similarity
            score_similarity[table].append(score)
    return score_similarity

def search_table(table_name, id, fields='*'):
    cursor = conn.cursor()
    if table_name == 'food':
        query = f"SELECT {fields} FROM {table_name} WHERE code = '{id}'"
    else:
        query = f"SELECT {fields} FROM {table_name} WHERE id = '{id}' "
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows

def requests_search(query):
    score_similarity = vectorize(query)
    return_search = []
    for table in score_similarity:
        for score in score_similarity[table]:
            for id in score:
                if score[id] > 0.3:                   
                  return_search.append(search_table(table, id=id))
    return return_search
            
        