import os
import random
import shutil

import graphviz as gv
import moviepy.video.io.ImageSequenceClip


def validateInput(startState, finalStates, transitionfn, msg):

    transition_table = []
    for key, val in transitionfn.items():
        row = key.split("-")
        row.append(val)
        transition_table.append(row)
        row = []

    # print("transition table", transition_table)

    dot = gv.Digraph("DFA", comment="DFA")
    dot.attr("node", shape="circle")

    # Deifne invisible node for starting point
    dot.node("", style="invis")

    # final nodes
    for node in finalStates:
        dot.node(node, shape="doublecircle")

    # define edges
    # define starting point
    dot.edge("", startState)

    if os.path.exists("src/static/img"):
        shutil.rmtree("src/static/img")

    if os.path.exists("src/static/video"):
        for file in os.listdir("src/static/video"):
            os.remove("src/static/video/" + file)

    currentState = startState
    nextState = startState
    for index, char in enumerate(msg):
        nextState = transitionfn[f"{currentState}-{char}"]
        currentState = nextState

    color = "red"
    if nextState in finalStates:
        color = "green"

    currentState = startState
    nextState = startState
    for index, char in enumerate(msg):
        nextState = transitionfn[f"{currentState}-{char}"]
        # if([currentState,char,nextState] not in traversed):
        createDFAImg(
            transitionfn,
            startState,
            finalStates,
            currentState,
            nextState,
            char,
            index,
            color,
        )
        # print(currentState, char, nextState)

        currentState = nextState

    for current_state, input_symbol, next_state in transition_table:
        dot.edge(current_state, next_state, input_symbol)

    dot.node(nextState, color=color)

    dot.render(
        directory="src/static/img",
        view=False,
        format="png",
        engine="circo",
        filename=f"img{len(msg)}",
    )

    temp_rn = random.randint(1000000, 9999999)
    current_file_dir = os.path.dirname(__file__)
    output_video_folder = "static/video"
    if not os.path.exists(os.path.join(current_file_dir, output_video_folder)):
        os.mkdir(os.path.join(current_file_dir, output_video_folder))
    output_video_file_name = f"video-{temp_rn}.mp4"
    image_folder = "src/static/img"

    image_files = [
        os.path.join(image_folder, img)
        for img in os.listdir(image_folder)
        if img.endswith(".png")
    ]

    image_files.insert(0, "src/static/DFA.gv.png")
    # print(image_files)
    clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=1)
    clip.write_videofile("src/static/video/" + output_video_file_name)
    return "/static/video/" + output_video_file_name


def createDFAImg(
    data, startnode, finalnodes, currentState, nextState, currentSymbol, index, color
):
    # preprocessing
    transition_table = []
    for key, val in data.items():
        row = key.split("-")
        row.append(val)
        transition_table.append(row)
        row = []

    # print("transition table", transition_table)

    dot = gv.Digraph("DFA", comment="DFA")
    dot.attr("node", shape="circle")

    # Define invisible node for starting point
    dot.node("", style="invis")

    # final nodes
    for node in finalnodes:
        dot.node(node, shape="doublecircle")

    # define edges
    # define starting point
    dot.edge("", startnode)

    for current_state, input_symbol, next_state in transition_table:
        if current_state == currentState:
            dot.node(currentState, color=color)
        if next_state == nextState:
            dot.node(nextState, color=color)
        if (
            input_symbol == currentSymbol
            and nextState == next_state
            and currentState == current_state
        ):

            dot.edge(current_state, next_state, input_symbol, color=color)
        else:
            dot.edge(current_state, next_state, input_symbol)

    # print(dot.source)

    dot.render(
        directory="src/static/img",
        view=False,
        format="png",
        engine="circo",
        filename=f"img{index}",
    )


def createDFA(data, startnode, finalnodes, output_dir):
    # preprocessing
    transition_table = []
    for key, val in data.items():
        row = key.split("-")
        row.append(val)
        transition_table.append(row)
        row = []

    # print("transition table", transition_table)

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

    dot.render(
        directory=output_dir,
        view=False,
        format="png",
        engine="circo",
    )


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
