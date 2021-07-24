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
margin: 20px 0px;

`
const ButtonNon = styled.button`
background-color: red;
color: white;
padding: 30px 90px;
border-radius: 15px;
cursor: pointer;
margin: 20px 0px;
`
const ButtonSubmit = styled.button`
background-color: blue;
color: white;
padding: 30px 90px;
border-radius: 15px;
cursor: pointer;
margin: 0px 0px;
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
        <ToggleGroup/>
        <ButtonSubmit onClick={clickMe}>
          SUBMIT
        </ButtonSubmit>
      </header>
    </div>
  );
}

export default VoteInterface;

