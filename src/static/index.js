document.getElementById("test").textContent = "testing"




document.getElementById("alphabetBtn").addEventListener("click", function(e){
  e.preventDefault();

  var alpha = document.getElementById("alphabets").value;
  var alphabets = alpha.split(",");

  document.getElementById("confirmedAlphabet").textContent = alphabets;

  document.getElementById("alphabetContainer").style.display = "none";
  genrateTransitionTable(alphabets,0);
})

let states = [];
let newStates = ["q0"];

function genrateTransitionTable(alphabets,noOfStates) {
  // let newStates = ['q1'];
  // let noOfStates = 0;
  // let it = 0;

  if(newStates.length == 0) {
    div = document.createElement("div");
    subBtn = document.createElement('button');
    subBtn.type = 'submit';
    subBtn.textContent = 'Submit';
    document.getElementById("statesInput").appendChild(div);
    
    cbContainer = document.createElement("fielset");
    legend = document.createElement("legend");
    legend.textContent = "Final States";
    
    for (let index = 0; index < states.length; index++) {
      label = document.createElement("label");
      label.textContent = `${states[index]}`;
      cb = document.createElement('input');
      cb.type = 'checkbox';
      cb.name = "finalstate";
      cb.value = states[index];
      label.appendChild(cb);
      cbContainer.appendChild(label);
    }

    div.appendChild(cbContainer);
    div.appendChild(subBtn);
    
    return;
  }

  let state = newStates.shift();
  states.push(state);
  let nextStates = [];

  div = document.createElement('div');
  p = document.createElement('p');
  p.textContent = `${state}`;
  div.appendChild(p);
  for(let i = 0; i < alphabets.length; i++){
    let inp = document.createElement('input');
    inp.type = "text"
    inp.name = `${state}-${alphabets[i]}`
    div.appendChild(inp);
  }
  const proceedBtn = document.createElement("button");
  proceedBtn.type = "button";
  proceedBtn.textContent = "Proceed";


  proceedBtn.addEventListener("click", function (e) {
    // fetch the input values and add them to the nextStates array
    for(let i = 0; i < alphabets.length; i++) {
      let inp = document.getElementsByName(`${state}-${alphabets[i]}`);
      console.log()
      nextStates.push(inp[0].value);
      // inp.remove();
    }
    proceedBtn.remove();
    console.log(`next states: ${nextStates}`);
    // check if any new state is encountered
    nextStates.forEach(state => {
      if(! (states.includes(state) || newStates.includes(state)) ){
        newStates.push(state);
      }
    })
    nextStates = [];

    console.log(`states: ${states}`);
    console.log(`new states: ${newStates}`);

    genrateTransitionTable(alphabets,states.length);

  });
  div.appendChild(proceedBtn);
  document.getElementById("statesInput").appendChild(div);

}