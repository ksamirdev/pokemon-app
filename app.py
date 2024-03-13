import requests
from flask import Flask, render_template, request
from flask_caching import Cache

# https://flask-caching.readthedocs.io/en/latest
config = {
    "DEBUG": True,                # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}

app = Flask(__name__,
            static_folder='web/static',
            template_folder='web/templates')

app.config.from_mapping(config);
cache = Cache(app)


# OUR POKEMON PAGE!
@app.route('/')
@cache.cached()
def pokemon_page():
  return render_template("index.html")


POKEMON_API = "https://api.pokemon.project.projectrexa.dedyn.io/pokeapi/{query}?authorization=622BEB8354BCDC1C94E1B5B414C66"

@app.route("/search", methods=["GET", "POST"])
@cache.cached()
def search_pokemon(): 
  query = request.form.get('query') or request.args.get('query')
  if query == None or len(query) <= 0:
    return render_template("index.html", success=False, message="Please provide me pokemon name or their id")
  
  resp = requests.get(POKEMON_API.format(query=query))
  if resp.status_code != 200:
    clean_message = resp.text.strip('"\n');
    return render_template("index.html", success=False, message=clean_message)

  data = resp.json()
  data['name'] = data['name'].title()

  return render_template("index.html", success=True, data=data)