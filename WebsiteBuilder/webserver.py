from flask import Flask, render_template_string, request, jsonify
from flask_cors import CORS
from werkzeug.debug import get_pin_and_cookie_name

webserver = Flask(__name__)
CORS(webserver)  

pages = {}

PAGE_HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{{ title }}</title>
</head>
<body>
  {{ content|safe }}
</body>
</html>
"""

@webserver.route('/')
def home():
    return "Webserver is active! Use `/dashboard` to manage pages."

@webserver.route('/<path:route>')
def serve_page(route):
    route = '/' + route.lstrip('/')
    page = pages.get(route)
    if page:
        return render_template_string(PAGE_HTML, title=page['title'], content=page['html'])
    else:
        return "Page not found", 404

@webserver.route('/add_page', methods=['POST'])
def add_page():
    data = request.get_json()
    route = '/' + data['route'].lstrip('/')

    if route in ["", "/"]:
        return jsonify({"error": "Invalid route!"}), 400

    if route in pages:
        return jsonify({"error": "Route already exists!"}), 400

    pages[route] = {'title': data['title'], 'html': data['html']}
    return jsonify({"message": "Page successfully added"}), 200

@webserver.route('/update_page', methods=['PUT'])
def update_page():
    data = request.get_json()
    route = '/' + data['route'].lstrip('/')

    if route in pages:
        pages[route] = {'title': data['title'], 'html': data['html']}
        return jsonify({"message": "Page successfully updated"}), 200
    
    return jsonify({"error": "Page not found"}), 404

@webserver.route('/delete_page', methods=['DELETE'])
def delete_page():
    data = request.get_json()
    route = '/' + data['route'].lstrip('/')

    if route in pages:
        del pages[route]
        return jsonify({"message": "Page successfully deleted"}), 200

    return jsonify({"error": "Page not found"}), 404

if __name__ == '__main__':
    webserver.run(debug=True, port=5001)
