import streamlit as st
import meilisearch
from config.config import MEILI_API_ADM_KEY, MEILI_SERVER

st.set_page_config(
    page_title="Main",
    page_icon="👋"
)

st.title('9 Mois à Croquer')
st.sidebar.markdown('# Main Page')

client = meilisearch.Client(f"http://{MEILI_API_ADM_KEY}", MEILI_SERVER)

search = st.text_input('Search')

if search:

    reponse = client.multi_search(
        [
            {'indexUid': 'recipes', 'q': search, 'limit': 5},
            {'indexUid': 'food', 'q': search, 'limit': 5},
            {'indexUid': 'articles', 'q': search},
            {'indexUid': 'questions', 'q': search}
        ]
    )

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

        list_of_values = reponse["results"][table]["hits"]

        if list_of_values:
            for values in list_of_values:
                for k, v in values.items():
                    if k not in ('id','code','img'):
                        st.write(f"## {k.capitalize()} ##")
                        st.write(v,unsafe_allow_html=True)                        

    # st.write(reponse)