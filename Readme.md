
# API 9 MOIS À CROQUER

This API was created to read a MySQL database and convert it in a Meilisearch indexed structure.

## Installation

### Install Meilisearch Server:
You must install meilisearch server to expose you indexed database in a REST API format.

https://www.meilisearch.com/docs/learn/getting_started/installation

 ### Generate API KEY:
 Once the server installed and configurated, you must create you API KEY that will be required to execute the solution.

curl -X GET 'http://localhost:7700/keys' -H 'Authorization: Bearer <YOUR MASTER KEY>'

__Example:__
```json
curl -X GET 'http://localhost:7700/keys' -H 'Authorization: Bearer WppGRZZFQIO6T1mBUliZCA05Rx3gCFXwjrf5W3ao26Q'

{"results":[
    {
        "name":"Default Search API Key","description":"Use it to search from the frontend",      
        "key":"7c492c796ca5b5dd7beb7d28dd0944972186a6629acf5384c09848b0b16e6935",
        "uid":"eaadd161-9c9c-43fc-b3bc-862407a9a1b2",
        "actions":["search"],"indexes":["*"],"expiresAt":null,
        "createdAt":"2023-12-19T11:04:38.009813332Z",
        "updatedAt":"2023-12-19T11:04:38.009813332Z"
    },
    {
        "name":"Default Admin API Key",
        "description":"Use it for anything that is not a search operation. Caution! Do not expose it on a public frontend",
        "key":"f96cad69ae8eff3974c9b28607288aa9b1a43f8846aca1f5586bafe670930a8d","uid":"7afc830a-7a44-4d90-871e-2dd8bbb100a5","actions":["*"],
        "indexes":["*"],"expiresAt":null,
        "createdAt":"2023-12-19T11:04:37.976440872Z",
        "updatedAt":"2023-12-19T11:04:37.976440872Z"
    }
    ],
    "offset":0,
    "limit":20,"total":2
}
```

__READ ONLY:__

```
"Use it to search from the frontend",
"key":"7c492c796ca5b5dd7beb7d28dd0944972186a6629acf5384c09848b0b16e6935"
```

__ADMIN:__

```
"Default Admin API Key","description":"Use it for anything that is not a search operation. Caution! Do not expose it on a public frontend",
"key":"f96cad69ae8eff3974c9b28607288aa9b1a43f8846aca1f5586bafe670930a8d"
```

### Required Python Libraries

```pip install -r requirements.txt```

### Configuration Files

Modify the configuration file located in __config/config.py__ with your database and meili server informations.


## Functionalities

### load_9mois_tables.py
- table_to_json(): Convert the selected table and its fields in a JSON format.
- json_to_meilisearch(): Load the database in a JSON format into Meilisearch index structure.

This script must be execute after every time that a new data is inseted in your database. You can configure it in a crontab like schedule.
## Deploy

Once everything installed and configurated.

```python
  python load_9mois_tables.py
```


## License

[MIT](https://choosealicense.com/licenses/mit/)

