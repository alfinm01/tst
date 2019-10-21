from flask import Flask, Response, redirect, request, jsonify
from bs4 import BeautifulSoup
import requests
import codecs
import config


app = Flask(__name__)
wikipedia = 'wikipedia.org/wiki/'
default_language = 'id' # supported on en (not all language supported)
region_api = 'http://dev.farizdotid.com/api/daerahindonesia/'


#
# Generating JSON responses
#
def generate_json_response(status_code, response_object):
	try:
		pass
	except Exception as e:
		raise e

#
# Authentication token checking
#
def auth_check(token):
	try:
		token = codecs.decode(token, 'hex').decode('utf-8')
		if token.endswith(config.SECRET_KEY):
			if token <= 0 or token >= 100000:
				return Response('Unauthorized', 401)
			pass
		else:
			return Response('Unauthorized', 401)

	except Exception as e:
		raise e

#
# Redirect to API documentation
# <NOT YET DOCUMENTED>
#
@app.route('/')
def documentation():
	return redirect('https://app.swaggerhub.com/apis-docs/alfinm01/TST_NationRegionAPI/1.0.0', code = 303)

#
# Get access token
# Simple NIM encryption (only for STI ITB student)
#
@app.route('/token/<nim>')
def get_token(nim):
	try:
		_nim = int(nim)
		_nim_check = _nim - 18200000
		if _nim_check > 0 and _nim_check < 100000:
			_nim = b'str(_nim).join(config.SECRET_KEY)'
			return codecs.encode(_nim, 'hex')
		else:
			return Response('Forbidden to access (Invalid NIM)', 403)

	except Exception as e:
		raise e

#
# Get desired nation data from Wikipedia
#
@app.route('/nation')
def nation():
	try:
		# Authentication check
		token = request.headers.get('token')
		auth_check(token)

		# Get Wikipedia content
		_nation = request.args.get('name')
		if _nation is None:
			return Response('Must include nation query', 400)
		_language = request.args.get('language')
		if _language:
			_result = requests.get('https://' + _language + '.' + wikipedia + _nation)
		else:
			_result = requests.get('https://' + default_language + '.' + wikipedia + _nation)
		_soup = BeautifulSoup(_result.text, 'html.parser')

		# Wiki not found
		_not_found = _soup.find('div', attrs = {'class' : 'noarticletext'})
		if _not_found:
			return Response('Nation not found', 404)
		
		# Parsing from HTML to JSON
		_table = _soup.find('table', attrs = {'class' : 'infobox'})
		
		# Wrong nation query
		if _table == None:
			return Response('Nation query is wrong', 404)

		# Iterate every tr
		_tbody = _table.find('tbody')
		_data = {}
		_counter = 0
		for _tr in _tbody.find_all('tr'):

			# Continue to next iterate
			if _tr.find('th', attrs = {'scope' : 'row'}) == None:
				continue

			# Parsing dictionary key
			if _tr.find('a'):
				_key = _tr.find('a').string
			else:
				if _tr.find('b'):
					_key = _tr.find('b').string
				else:
					if _tr.find('div'):
						_key = _tr.find('div').string
					else:
						_key = 'uncrawled object ' + str(_counter)

			# Parsing dictionary value
			if _tr.find('td'):
				_value = _tr.find('td').text
			else:
				_value = 'uncrawled object ' + str(_counter)

			# Append dictionary
			_data[_key] = _value
			_counter += 1

		return jsonify(_data)

	except Exception as e:
		raise e


# Route below is using direct method (without database storage)
# Possibility of change in the future

#
# Get Indonesian provinces data
#
@app.route('/id/province')
def province():
	try:
		# Authentication check
		token = request.headers.get('token')
		auth_check(token)

		# Reformat JSON data
		_result = requests.get(region_api + 'provinsi').json()
		print(_result)
		_data = _result['semuaprovinsi']
		return jsonify(_data)

	except Exception as e:
		raise e

#
# Get Indonesian cities data
#
@app.route('/id/city/<province_id>')
def city(province_id):
	try:
		# Authentication check
		token = request.headers.get('token')
		auth_check(token)

		# Reformat JSON data
		_result = requests.get(region_api + 'provinsi/' + province_id + '/kabupaten').json()
		_data = _result['kabupatens']
		return jsonify(_data)

	except Exception as e:
		raise e

#
# Get Indonesian districts data
#
@app.route('/id/district/<city_id>')
def district(city_id):
	try:
		# Authentication check
		token = request.headers.get('token')
		auth_check(token)

		# Reformat JSON data
		_result = requests.get(region_api + 'provinsi/kabupaten/' + city_id + '/kecamatan').json()
		_data = _result['kecamatans']
		return jsonify(_data)

	except Exception as e:
		raise e

#
# Get Indonesian villages data
#
@app.route('/id/village/<district_id>')
def village(district_id):
	try:
		# Authentication check
		token = request.headers.get('token')
		auth_check(token)

		# Reformat JSON data
		_result = requests.get(region_api + 'provinsi/kabupaten/kecamatan/' + district_id + '/desa').json()
		_data = _result['desas']
		return jsonify(_data)

	except Exception as e:
		raise e


if __name__ == '__main__':
    app.run(ssl_context = ('cert.pem', 'key.pem'))
    #app.run(debug = True)