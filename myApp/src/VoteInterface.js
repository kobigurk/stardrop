import './App.css';
import react, { useState } from "react";
import styled from 'styled-components'
import { get_commit_token } from './API'
import { get_pub_key } from './API'
const axios = require('axios');
let pubKey;
function clickMe() {
  alert("you click here")
}

function callVote(resultat) {
  const commitToken = get_commit_token();
  pubKey = get_pub_key();
  axios({
      method: 'post',
      url: 'http://192.168.0.44:4242/api/vote',
      data: {
        ppublic_key : pubKey,
        vote : resultat,
        commit_token : commitToken
      }
    }).then((response) => {
          console.log(response);
          if (response.status != 200) 
          console.log("ERROR");
            // setErrorMessage("ERROR");
      })
      .catch((error) => {
          // setErrorMessage("catch ERROR");
          console.log("catch ERROR");
      })
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
// const ButtonSubmit = styled.button`
// background-color: blue;
// color: white;
// padding: 30px 90px;
// border-radius: 15px;
// cursor: pointer;
// margin: 0px 0px;
// `
const types = ['OUI', 'NON'];

function ToggleGroup() {
  const [active, setActive]= useState(types[0]);
  return <div>
    <ButtonOui onClick={callVote("Y")}>
      YES
    </ButtonOui>
    <ButtonNon onClick={callVote("N")}>
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
      </header>
    </div>
  );
}

export default VoteInterface;

