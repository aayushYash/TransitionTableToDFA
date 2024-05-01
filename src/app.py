from flask import Flask, render_template, request
import DFA
import pandas as pd

app = Flask(__name__)


@app.route("/")
def homepage():
    return render_template("index.html")


finalstates = []
alphabets = []
data = {}
dataframe = {"states": []}


@app.route("/validateString", methods=["POST"])
def validateString():
    print(dataframe)
    print(request.form)
    inputString = request.form["inputString"]
    df = pd.DataFrame(dataframe)
    table = df.to_html()
    rv = ""
    for k in inputString:
      if k not in alphabets:
        return render_template(
            "dfa.html",
            table=table,
            src="/static/DFA.gv.png",
          error_message="bad inputs"
        )
      
    rv = DFA.validateInput("q0", finalstates, data, inputString)
    # try:
    #   pass
    # except Exception as e:
    #   print(e)
    # global data
    data1 = {
      'alphabets': ','.join(alphabets),
      'states': ','.join(dataframe['states']),
      'finalStates': ','.join(finalstates),
      'inputString': inputString,
      'transitionfn': data,
      'initialState': 'q0',
    }
    return render_template(
        "dfa.html",
        table=table,
        src="/static/DFA.gv.png",
        video=rv.lstrip("src"),
        data= data1,
    )


# transition fn
@app.route("/transitionTable", methods=["POST"])
def transitionTable():
    global finalstates
    finalstates = []
    global alphabets
    alphabets = []
    global data
    data = {}
    global dataframe
    dataframe = {"states": []}
    print(request.form)  # request
    for key, val in request.form.items():
        print(key, val)
        if "finalstate" in key:
            finalstates.append(val)
            continue
        if key == "alphabets":
            # global alphabets
            alphabets = val.split(",")
            continue
        data[key] = val
    # print(data)

    for i in alphabets:
        dataframe[i] = []

    # transition_table = []
    for key, val in data.items():
        row = key.split("-")
        if row[0] not in dataframe["states"]:
            if "->q0" not in dataframe["states"]:
                dataframe["states"].append(f"->{row[0]}")
            elif row[0] == "q0":
                pass
            else:
                dataframe["states"].append(row[0])

        tval = val
        if val in finalstates:
            tval = f"*{val}"

        dataframe[row[1]].append(tval)

        row = []

    # print(dataframe)
    df = pd.DataFrame(dataframe)
    table = df.to_html()

    DFA.createDFA(data, "q0", finalstates, "./src/static")
    # try:
    # except Exception as e:
    #   print(e)
    # global data
    data1 = {
      'alphabets': ','.join(alphabets),
      'states': ','.join(dataframe['states']),
      'finalStates': ','.join(finalstates),
      # 'inputString': inputString,
      'transitionfn': data,
      'initialState': 'q0',
    }

    return render_template("dfa.html", src="/static/DFA.gv.png", table=table,data=data1)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        debug=True,
    )
