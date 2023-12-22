#/home/jcaldeira/Dev/9mois# ./meilisearch --master-key ZViEJIa3iKUeBLdEem4n74O4rKID8TjwXns7We9Mqmg
import meilisearch
import json
import mysql.connector
from config.config import DATABASE_HOST, DATABASE_NAME, DATABASE_PASSWORD, DATABASE_USERNAME, MEILI_API_ADM_KEY, MEILI_SERVER

# Connect to the database
conn = mysql.connector.connect(
    host=DATABASE_HOST,
    user=DATABASE_USERNAME,
    password=DATABASE_PASSWORD,
    database=DATABASE_NAME
)

# Transform SQL to JSON
def table_to_json(table_name, fields='*'):
    cursor = conn.cursor()
    query = f"SELECT {fields} FROM {table_name}"
    cursor.execute(query)

    rows = cursor.fetchall()
    result = []
    for row in rows:
        d = {}
        for i, col in enumerate(cursor.description):
            d[col[0]] = str(row[i]).replace('\n', '<br>')
        result.append(d)
    
    json_result = json.dumps(result)
    return json_result

# Import JSON to meilisearch
def json_to_meilisearch(table_name, fields='*', primary_key='id'):
    client.index(table_name).delete()
    json_result = table_to_json(table_name=table_name, fields=fields)
    client.index(table_name).update_documents(primary_key=primary_key,documents=json.loads(json_result))

client = meilisearch.Client(f"http://{MEILI_SERVER}", MEILI_API_ADM_KEY)

tables = {
    0:{
         'table_name': 'food',
         'fields': 'code, name, img',
         'primary_key': 'code'
      },
    1:{
         'table_name': 'recipes',
         'fields': 'id, name, time, difficulty, budget, img, review, nb_portions, side_food, steps, food',
         'primary_key': 'id'
    },
    2:{
         'table_name': 'articles',
         'fields': 'id, title, content, img',
         'primary_key': 'id'
    },
    3:{
         'table_name': 'questions',
         'fields': 'id, question, answer, state, url_article',
         'primary_key': 'id'
    }
}

for table in tables:
    table_name = tables[table]['table_name']
    fields = tables[table]['fields']
    primary_key = tables[table]['primary_key']
    json_to_meilisearch(table_name, fields, primary_key)