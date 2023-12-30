#/home/jcaldeira/Dev/9mois# ./meilisearch --master-key ZViEJIa3iKUeBLdEem4n74O4rKID8TjwXns7We9Mqmg
import meilisearch
import json
import mysql.connector
import re
from config.config import DATABASE_HOST, DATABASE_NAME, DATABASE_PASSWORD, DATABASE_USERNAME

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
            res = re.sub(pattern_1, '', str(row[i]))
            res = re.sub(pattern_2, '', res)
            d[col[0]] = str(res).replace('\n', '').replace('\\', '').replace('*', '')
        result.append(d)
    
    json_result = json.dumps(result)
    return json_result


tables = {
    0:{
         'table_name': 'food',
         'fields': 'code, name, img',
         'primary_key': 'code'
      },
    1:{
         'table_name': 'recipes',
         'fields': 'id, name, time, difficulty, budget, review, nb_portions, side_food, steps, food',
         'primary_key': 'id'
    },
    2:{
         'table_name': 'articles',
         'fields': 'id, title, content',
         'primary_key': 'id'
    },
    3:{
         'table_name': 'questions',
         'fields': 'id, question, answer, state, url_article',
         'primary_key': 'id'
    }
}


# Retirer les balises
pattern_1 = re.compile('<.*?>')
pattern_2 = re.compile('\(.*?\)')
pattern_3 = re.compile('\[.*?\]')

for table in tables:
    table_name = tables[table]['table_name']
    fields = tables[table]['fields']
