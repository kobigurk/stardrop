import './myStyles.css';
import react, { useState } from "react";
import styled from 'styled-components'
import { get_pub_key } from './API'
import { get_commit_token } from './CommitInterface'
const axios = require('axios');
let pubKey;



function callEndVotingPhase(resultat) {
  const commitToken = get_commit_token();
  pubKey = get_pub_key();
  axios({
      method: 'post',
      url: 'http://192.168.43.218:5000/api/end_voting_phase',
      data: {
        message: "vitalik<3"
      }
    }).then((response) => {
          console.log(response);
          if (response.status != 200) 
          console.log("ERROR");
      })
      .catch((error) => {
          console.log("catch ERROR");
      })
}

function callResultat(resultat) {
  axios({
      method: 'get',
      url: 'http://192.168.43.218:4242/api/get_result'
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

function callVote(resultat) {
  const commitToken = get_commit_token();
  pubKey = get_pub_key();
  console.log(pubKey)
  if (!resultat || !commitToken) {
    console.log("pb variable vide")
    return 300;
  }
  axios({
      method: 'post',
      url: 'http://192.168.43.218:5000/api/vote',
      data: {
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

const types = ['OUI', 'NON'];

function ToggleGroup() {
  const [active, setActive]= useState(types[0]);
  return <div>
    <ButtonOui onClick={() => callVote('Yes')}>
      YES
    </ButtonOui>
    <ButtonNon onClick={() => callVote('No')}>
      NO
    </ButtonNon>
    <button onClick={callEndVotingPhase}>END VOTING PHASE</button>
    <button onClick={callResultat}>CALL RESULTAT</button>
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

