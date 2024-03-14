import requests
from flask import Flask, render_template, request

app = Flask(__name__,
            static_folder='web/static',
            template_folder='web/templates')


# OUR POKEMON PAGE!
@app.route('/')
def pokemon_page():
  return render_template("index.html")


POKEMON_API = "https://api.pokemon.project.projectrexa.dedyn.io/pokeapi/{query}?authorization=622BEB8354BCDC1C94E1B5B414C66"

@app.route("/search", methods=["GET", "POST"])
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



tasks = ["task1", "task2", "task3", "task4"]
# TODO APP
@app.route('/todo')
def todo_app():
  return render_template("todo.html", tasks=tasks)

if __name__ == "__main__":
  app.run()