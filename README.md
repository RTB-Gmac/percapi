# percapi
A minimal (50 lines of code in the `perc.py` source) implementation of the document percolation functionality for keyword labelling written in python.

Just run test `test_percolation_performance()` and check performance.

It's possible to run API (on fastapi) from docker, load any amount of queries and percolate documents.

Solution is:
* **POC --> simple & basic**
* **language agnostic (check test `test_percolate_non_latin()`)**
* **supports minimum_match functionality**
* **single threaded**
* **lightweight (docker container take ~35MB without any queries, ~140MB with 5k queries)**
* **efficient (~1.2k [documents per second] with 10k queries in index where query has 120 terms an average)**
* **real case scenario with documents from GBQ and queries from CAI --> ~350 docs / sec.**


### install dependencies
for local environment setup call: 
```commandline
pip install -r requirements.txt
```

### run tests locally
to run test from per-capi-container call:
```commandline
pytest ./poc/tests.py -s
```
look for **"Performance: XXXX [docs / sec.]"** at commandline after tests.
```commandline
=================================================================================================== test session starts 
platform linux -- Python 3.11.8, pytest-8.3.5, pluggy-1.5.0
rootdir: /home/gmaciaszek/Documents/RTB_GH_Repos/percapi
plugins: anyio-4.9.0
collected 11 items                                                                                       

poc/tests.py ..............
Performance: 1184 [docs / sec.]
.

==================================================================================================== 11 passed in 1.33s
```

### build docker image
to build docker call:
```commandline
docker build -t per-capi ./poc
```

### run per-capi API
to run per-capi API from docker image call
```commandline
docker run -d -p 8800:8800 --name per-capi-container per-capi
```
The application will be available at: http://localhost:8800 and swagger at: http://localhost:8800/docs#/

### erase container
to delete container call
```commandline
docker rm -f per-capi-container
```

### check resource stats
to monitor resources used by per-capi-container call:
```commandline
docker stats per-capi-container
```

## API
This is a FastAPI-based perc-api that match documents against queries.

#### Endpoints

### **Add Query**
`POST /add_query`

Adds a new query to the Percolator.

**Request Body (JSON):**
```json
{
  "query": ["example", "text"],
  "category": "news",
  "minimum_match": 1,
  "unique_term_count": true
}
```

**Response:**
```json
{
  "message": "Query added successfully"
}
```

---

### **Finalize Queries**
`GET /finalize`

Finalizes added queries – **this endpoint must be called after adding all queries**.

**Response:**
```json
{
  "automation made / finalized"
}
```

---

### **Percolate Document**
`POST /percolate`

Checks which queries match the provided document.

**Request Body (JSON):**
```json
{
  "document": "This is an example document."
}
```

**Response:**
```json
{
  "matches": ["news"]
}
```

## Important Information
After adding all queries, **make sure to call the `/finalize` endpoint** so that the Percolator can process them properly.



