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
      url: 'http://192.168.106.112:5000/api/end_voting_phase',
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
      url: 'http://192.168.106.112:4242/api/get_result'
    }).then((response) => {
          console.log(response);
          console.log(response.yes)
          console.log(response.no)
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
      url: 'http://192.168.106.112:5000/api/vote',
      data: {
        vote : resultat,
        commit_token : commitToken,
      }
    }).then((response) => {
          console.log(response);
          alert("Number of yes : ", response.yes);
          alert("Number of no : ", response.no);
          if (response.status != 200)
          console.log("ERROR");
            // setErrorMessage("ERROR");
      })
      .catch((error) => {
          // setErrorMessage("catch ERROR");
          console.log("catch ERROR");
      })
}

const types = ['OUI', 'NON'];

function ToggleGroup() {
  const [active, setActive]= useState('');
  return <div>
    <button className={'btn-grad2'} onClick={ () => callVote('Yes')}>YES</button>
    <button className={'btn-grad2'} onClick={ () => callVote('No')}>NO</button>
    <button onClick={callEndVotingPhase}>END VOTING PHASE</button>
    <button onClick={callResultat}>CALL RESULTAT</button>
    </div>
}

function VoteInterface() {
  return (
    <div className="App">
      <header className="App-header">
        SHOULD CARLOS MATOS PRESIDE THE ETHEREUM FOUNDATION ?
        <ToggleGroup/>
      </header>
    </div>
  );
}

export default VoteInterface;
