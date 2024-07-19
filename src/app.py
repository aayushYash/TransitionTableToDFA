import pandas as pd
from flask import Flask, render_template, request

import DFA

app = Flask(__name__)

data = {}
alphabets = []
final_states = []
dataframe = {}


@app.route("/")
def homepage():
    """
    render Home page.
    """
    return render_template("index.html")


# transition fn
@app.route("/transitionTable", methods=["POST"])
def transition_table():
    """
    Get the input(alphabets , states, final states ) from the user.
    Also generate the transition table and DFA.
    """
    global dataframe, alphabets, data, final_states
    dataframe.clear()
    alphabets.clear()
    data.clear()
    final_states.clear()

    # Extract data from form input
    for key, val in request.form.items():
        key = key.strip().replace(" ", "")
        val = val.strip()
        if "finalstate" in key:
            final_states.append(val.strip())
            continue
        if key == "alphabets":
            alphabets = list(map(str.strip, val.split(",")))
            continue
        data[key] = val.strip()
    # print(data)

    # Generate Transition table
    dataframe = {"states": []}
    for i in alphabets:
        dataframe[i] = []

    for key, val in data.items():
        key = key.strip().replace(" ", "")
        val = val.strip()
        row = list(map(str.strip, key.split("-")))
        if row[0] not in dataframe["states"]:
            if "->q0" not in dataframe["states"]:
                dataframe["states"].append(f"->{row[0]}")
            elif row[0] == "q0":
                pass
            else:
                dataframe["states"].append(row[0])

        tval = val
        if val in final_states:
            tval = f"*{val}"

        dataframe[row[1]].append(tval)
        row = []

    df = pd.DataFrame(dataframe)
    table = df.to_html()

    # Generate DFA
    print(data)
    DFA.createDFA(data, "q0", final_states, "./src/static")
    context = {
        "alphabets": ",".join(alphabets),
        "states": ",".join(dataframe["states"]),
        "final_states": ",".join(final_states),
        "transitionfn": data,
        "initialState": "q0",
        "src": "/static/DFA.gv.png",
        "table": table,
    }

    return render_template("dfa.html", context=context)


@app.route("/validateString", methods=["POST"])
def validate_string():
    """
    Sanitize and validate input from user.
    """
    global dataframe, alphabets, data, final_states

    print(request.form)
    input_string = request.form["input_string"]
    df = pd.DataFrame(dataframe)
    table = df.to_html()
    context = {
        "alphabets": ",".join(alphabets),
        "states": ",".join(dataframe["states"]),
        "final_states": ",".join(final_states),
        "input_string": input_string,
        "src": "/static/DFA.gv.png",
        "table": table,
        "transitionfn": data,
        "initialState": "q0",
    }

    for k in map(str.strip, input_string.strip()):
        if not k in alphabets:
            context["error_message"] = "Bad Input(Possible cause: invalid alphabets)"
            print("Error: Bad Inputs")
            return render_template("dfa.html", context=context)

    result_video_path = DFA.validateInput("q0", final_states, data, input_string)
    print(result_video_path)
    context["video"] = result_video_path.lstrip("src")

    return render_template(
        "dfa.html",
        context=context,
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        debug=True,
    )
