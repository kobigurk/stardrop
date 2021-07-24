import './App.css';
import react, { useState } from "react";
import styled from 'styled-components'

function clickMe() {
  alert("you click here")
}

const ButtonOui = styled.button`
background-color: green;
color: white;
padding: 30px 90px;
border-radius: 15px;
outline: 0;
cursor: pointer;

`
const ButtonNon = styled.button`
background-color: red;
color: white;
padding: 30px 90px;
border-radius: 15px;
cursor: pointer;
`
const ButtonSubmit = styled.button`
background-color: blue;
color: white;
padding: 30px 90px;
border-radius: 15px;
cursor: pointer;
margin: 50px 0px;
`
const types = ['OUI', 'NON'];

function ToggleGroup() {
  const [active, setActive]= useState(types[0]);
  return <div>
    <ButtonOui>
      YES
    </ButtonOui>
    <ButtonNon>
      NO
    </ButtonNon>
  </div>
}

function VoteInterface() {
  return (
    <div className="App">
      <header className="App-header">
        SHOULD CARLOS MATOS PRESIDE THE ETHEREUM FONDATION ?
        {/* <img src={logo} className="App-logo" alt="logo" /> */}
        <p>
          {/* Edit <code>src/App.js</code> and save to reload. */}
        </p>
        {/* <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a> */}
          <ButtonSubmit onClick={clickMe}>
          SUBMIT
        </ButtonSubmit>
        <ToggleGroup/>
      </header>
    </div>
  );
}

export default VoteInterface;

