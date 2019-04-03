

from flask import jsonify, Flask, request
from datavalidation.datavalidation import request_validate_bike_geometry


application = Flask(__name__)


@application.route('/validation', methods=['POST'])
def json_handler():
		content = request.get_json(force=True)
		valid_bike = request_validate_bike_geometry(content)

		return jsonify(valid_bike)


if __name__ == '__main__':
	application.run(debug=True, host='0.0.0.0')
