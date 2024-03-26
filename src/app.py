from flask import Flask, render_template, request
import DFA

app = app = Flask(__name__)


@app.route("/")
def homepage():
  return render_template("index.html")


@app.route("/transitionTable", methods=["post"])
def transitionTable():
  print(request.form) # request
  finalstates = [] 
  alphabets = [] 
  data = {} 
  for (key, val) in request.form.items():
    print(key, val)
    if key == "finalstate":
      finalstates.append(val)
      continue
    if key == "alphabets":
      alphabets = val.split(",")
      continue
    data[key] = val
  print(data)  
  try:
    DFA.createDFA(data, "q0", finalstates, "./src/static")
    pass
  except Exception as e:
    print(e)

  return render_template("index.html", src="/static/DFA.gv.png")


if __name__ == "__main__":
  app.run(
      host="0.0.0.0",
      debug=True,
  )
