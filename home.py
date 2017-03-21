from flask import Flask, request, render_template
from busca import busca

app = Flask("lenhador", static_url_path = "", static_folder = "static")

@app.route('/')
def index():
    return render_template("index.html"), 200

@app.route('/resut', methods=["GET"])
def result():
    if request.method == "GET":
        form = request.form.to_dict()
        site_query = form['site_query']
        where = form['where']
        results = busca(site_query, where)
        return render_template('result.html', results=results)
    else:
        return 500

app.run()
