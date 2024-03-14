import requests
from flask import Flask, render_template, request, redirect, session


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


app.config['SECRET_KEY'] = 'secret_key'

# TODO APP
@app.route('/todo')
def todo_app():
  if "tasks" not in session:
    session['tasks'] = []

  return render_template("todo.html", tasks=session['tasks'])

@app.route('/todo/add', methods=["POST"])
def add_todo():
  todo = request.form.get('todo')
  if todo == None or len(todo.strip()) <= 0:
    return redirect('/todo?error=Please provide a task', code=302)

  session["tasks"] += [todo.strip()]
  return redirect("/todo", code=302)


@app.route("/todo/delete", methods=["POST"])
def remove_todo():
  index = request.form.get('todo-index')
  if index == None:
    return redirect('/todo?error=Please provide a index to delete a task', code=302)
  
  # https://stackoverflow.com/questions/627435/how-to-remove-an-element-from-a-list-by-index
  del session['tasks'][int(index)]

  session['tasks'] = session['tasks'];
  return redirect("/todo", code=302)