document.getElementById("alphabetBtn").addEventListener("click", function(e){
  e.preventDefault();
  const stateTable = document.getElementById("stateTable");
  var alpha = document.getElementById("alphabets").value;
  var alphabets = alpha.split(",");
  // alphabets.unshift("States")
  const tr = document.createElement("tr");
  const st = document.createElement("td");
  st.textContent = "States";
  tr.appendChild(st)
  for (element of alphabets) {
    const td = document.createElement('td');
    td.textContent = element;
    tr.appendChild(td);
  }
  stateTable.appendChild(tr);
  // document.getElementById("confirmedAlphabet").textContent = alphabets;

  document.getElementById("alphabetContainer").style.display = "none";
  genrateTransitionTable(alphabets,0);
})

let states = [];
let newStates = ["q0"];

function genrateTransitionTable(alphabets,noOfStates) {

  const tr = document.createElement("tr");


  if(newStates.length == 0) {
    div = document.createElement("div");
    subBtn = document.createElement('button');
    subBtn.type = 'submit';
    subBtn.textContent = 'Submit';
    document.getElementById("statesInput").appendChild(div);
    
    cbContainer = document.createElement("fieldset");
    legend = document.createElement("legend");
    legend.textContent = "Final States";

    cbContainer.appendChild(legend);
    
    for (let index = 0; index < states.length; index++) {
      label = document.createElement("label");
      label.textContent = `${states[index]}`;
      cb = document.createElement('input');
      cb.type = 'checkbox';    
      cb.name = "finalstate-"+index;
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
  const tdSt = document.createElement('td');
  // div = document.createElement('div');
  p = document.createElement('p');
  p.textContent = `${state}`;
  tdSt.appendChild(p);
  tr.appendChild(tdSt);
  for(let i = 0; i < alphabets.length; i++){
    const tdIn = document.createElement('td');
    let inp = document.createElement('input');
    inp.placeholder = "Enter next state";
    inp.type = "text"
    inp.name = `${state}-${alphabets[i]}`
    tdIn.appendChild(inp);
    tr.appendChild(tdIn);
  }
  const proceedBtn = document.createElement("button");
  proceedBtn.type = "button";
  proceedBtn.textContent = "Proceed";

  const tdBtn = document.createElement('td');
  tdBtn.appendChild(proceedBtn);


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
  tr.appendChild(tdBtn);
  // document.getElementById("statesInput").appendChild(div);
  document.getElementById("stateTable").appendChild(tr)

}