from flask import Flask, render_template_string, request, redirect
import requests
from werkzeug.debug import get_pin_and_cookie_name

# Initialize Flask
dashboard = Flask(__name__)

WEB_SERVER_URL = "http://127.0.0.1:5001"

# Store pages in memory (temporary)
pages = {}

# HTML Template for Dashboard
DASHBOARD_HTML = r"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>WebsiteBuilder Dashboard</title>
  <style>
    .page-item { border: 1px solid #ddd; padding: 10px; margin: 5px 0; background-color: #f9f9f9; }
    .page-item:hover { background-color: #e0e0e0; }
    .web, .edit { color: blue; text-decoration: none; }
    .delete { color: red; text-decoration: none; }
  </style>
</head>
<body>
  <h1>WebsiteBuilder - Dashboard</h1>

  <!-- Display success/failure messages -->
  {% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
      <div>
        {% for category, message in messages %}
          <p style="color: {% if category == 'success' %}green{% else %}red{% endif %};">
            {{ message }}
          </p>
        {% endfor %}
      </div>
    {% endif %}
  {% endwith %}

  <!-- Page Creation Form -->
  <form method="post" action="/create" onsubmit="return validateForm()">
    <label for="route">Route:</label>
    <input autocomplete="off" type="text" id="route" name="route" required>
    <br><br>
    
    <label for="title">Page Title:</label>
    <input autocomplete="off" type="text" id="title" name="title" required>
    <br><br>
    
    <label for="html_code">HTML Code:</label><br>
    <textarea id="html_code" name="html_code" rows="5" cols="50" required></textarea>
    <input type="file" id="fileInput" accept=".html">
    <br><br>
    
    <button type="submit">Create Page</button>
  </form>

  <!-- Page Search -->
  <h2>Created Pages</h2>
  <label for="search">Search Page:</label>
  <input autocomplete="off" type="text" id="search" onkeyup="filterPages()" placeholder="Search pages...">

  <div id="pages_list">
    {% for route, info in pages.items() %}
      <div class="page-item">
        <strong>{{ info.title }}</strong> ({{ route }}) 
        - <a class="web" href="{{ web_server }}{{ route }}" target="_blank">View</a>
        - <a class="edit" href="/edit/_/{{ route }}">Edit</a>
        - <a class="delete" href="/delete/_/{{ route }}" onclick="return confirm('Are you sure you want to delete this page?')">Delete</a>
      </div>
    {% else %}
      <p>No pages created yet.</p>
    {% endfor %}
  </div>

  <!-- JavaScript for validation & search filter -->
  <script>
    function validateForm() {
      let route = document.getElementById("route").value.trim();
      let title = document.getElementById("title").value.trim();
      let html_code = document.getElementById("html_code").value.trim();

      let invalidChars = /[^a-zA-Z0-9-_\/]/;

      if (route === "" || route === "/" || invalidChars.test(route)) {
        alert("Invalid route! Use letters, numbers, -, or _.");
        return false;
      }
      if (title === "") {
        alert("Title cannot be empty!");
        return false;
      }
      if (html_code === "") {
        alert("HTML code cannot be empty!");
        return false;
      }
      return true;
    }

    document.getElementById("fileInput").addEventListener("change", function(event) {
      const file = event.target.files[0]; 
      if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
          document.getElementById("html_code").value = e.target.result; 
        };
        reader.readAsText(file);
      }
    });

    function filterPages() {
      let input = document.getElementById("search").value.toLowerCase();
      let items = document.getElementsByClassName("page-item");

      for (let i = 0; i < items.length; i++) {
        let title = items[i].getElementsByTagName("strong")[0].innerText.toLowerCase();
        let route = items[i].innerText.toLowerCase();

        if (title.includes(input) || route.includes(input)) {
          items[i].style.display = "";
        } else {
          items[i].style.display = "none";
        }
      }
    }
  </script>
</body>
</html>
"""

@dashboard.route('/dashboard')
def dashboard_home():
    return render_template_string(DASHBOARD_HTML, pages=pages, web_server=WEB_SERVER_URL)

@dashboard.route('/create', methods=['POST'])
def create_page():
    route = request.form['route'].strip()
    title = request.form['title']
    html_code = request.form['html_code']

    if not route.startswith('/'):
        route = '/' + route

    if route not in pages:
        pages[route] = {'title': title, 'html': html_code}
        requests.post(WEB_SERVER_URL + "/add_page", json={'route': route, 'title': title, 'html': html_code})

    return redirect('/dashboard')

@dashboard.route('/edit/_/<route>', methods=["GET", "POST"]) 
def edit_page(route):
    route = '/' + route.lstrip('/')
    
    if route not in pages:
        return "Page not found", 404

    if request.method == 'POST':
        new_title = request.form['title']
        new_html = request.form['html_code']
        pages[route] = {'title': new_title, 'html': new_html}
        requests.put(WEB_SERVER_URL + "/update_page", json={'route': route, 'title': new_title, 'html': new_html})
        return redirect('/dashboard')

    return f"""
    <form method="post">
      <label>Page Title:</label>
      <input autocomplete="off" type="text" name="title" value="{pages[route]['title']}" required><br><br>
      <label>HTML Code:</label><br>
      <textarea name="html_code" rows="5" cols="50" required>{pages[route]['html']}</textarea><br><br>
      <button type="submit">Save</button>
      <a href="/dashboard"><button type="button">Cancel</button></a>
    </form>
    """

@dashboard.route('/delete/_/<route>') 
def delete_page(route):
    route = '/' + route.lstrip('/')
    
    if route in pages:
        del pages[route]
        requests.delete(WEB_SERVER_URL + "/delete_page", json={'route': route})

    return redirect('/dashboard')

@dashboard.route("/routes")
def see_routes():
    return pages

@dashboard.route("/")
def index():
    return redirect("/dashboard")

if __name__ == '__main__':
    dashboard.run(debug=True, port=5000)
