# Wiki and Region API

Mata Kuliah II3160 - Teknologi Sistem Terintegrasi\
Alfian Maulana Ibrahim - 18217038\
\
Deployed API: [https://wiki-region-api.herokuapp.com/{route}](https://wiki-region-api.herokuapp.com)\
Documentation: https://app.swaggerhub.com/apis-docs/alfinm01/TST_WikiRegionAPI/1.0.0

## List Endpoints

``` bash
GET '/' = Redirect to API documentation
GET '/token/<nim>' = Get access token (use STI ITB student NIM) [temporary disabled]
GET '/wiki' = Get desired wiki data crawled from Wikipedia <query = name, language>*
GET '/wiki/raw' = Get desired wiki raw html data crawled from Wikipedia <query = name, language>*
GET '/id/province' = Get Indonesian provinces data*
GET '/id/city/<province_id>' = Get Indonesian cities data*
GET '/id/district/<city_id>' = Get Indonesian districts data*
GET '/id/village/<district_id>' = Get Indonesian villages data*
*Access token needed [temporary disabled]
```

## Setup (on Windows example)

``` bash
# install environments
$ py -3 -m venv venv
$ venv\Scripts\activate
(venv) $ pip install -r requirements.txt
```

## Running locally (on Windows example)

``` bash
# serve at default https://localhost:5000
$ venv\Scripts\activate
(venv) $ py main.py

# to leave venv
(venv) $ deactivate
```
