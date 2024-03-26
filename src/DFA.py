import graphviz as gv


def createDFA(data, startnode, finalnodes, output_dir):
    # preprocessing
    transition_table = []
    for key, val in data.items():
        row = key.split("-")
        row.append(val)
        transition_table.append(row)
        row = []

    print("transition table", transition_table)

    dot = gv.Digraph("DFA", comment="DFA")
    dot.attr("node", shape="circle")

    # Deifne invisible node for starting point
    dot.node("", style="invis")

    # final nodes
    for node in finalnodes:
        dot.node(node, shape="doublecircle")

    # define edges
    # define starting point
    dot.edge("", startnode)
    for current_state, input_symbol, next_state in transition_table:
        dot.edge(current_state, next_state, input_symbol)
    print(dot.source)

    dot.render(directory=output_dir, view=False, format="png", engine="circo")


# startnode = "0"
# currentState, inputSymbol, nextstate
# data = {
#     ("0-0"): "1", 
#     ("0-1"): "2",
#     ("1-0"): "1",
#     ("1-1"): "0",
#     ("2-0"): "2",
#     ("2-1"): "3",
#     ("3-0"): "1",
#     ("3-1"): "0",
# }
# finalnodes = ["1", "2"]

# createDFA(data, startnode, finalnodes)
