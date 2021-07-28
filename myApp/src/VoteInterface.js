import './myStyles.scss';
import './VoteInterface.scss';
import { get_pub_key } from './API'
import { get_voting_token } from './CommitInterface'
import { LOCAL_SERVER, STARK_SERVER } from './constants';
import { useState } from 'react';
const axios = require('axios');
let pubKey;
let voting_token;

function callEndVotingPhase(resultat) {
  pubKey = get_pub_key();
  axios({
    method: 'post',
    url: `${STARK_SERVER}/api/end_voting_phase`,
    data: {
      message: "vitalik<3"
    }
  }).then((response) => {
    console.log(response);
    if (response.status !== 200)
      console.log("ERROR");
  })
    .catch((error) => {
      console.log("catch ERROR");
    })
}

function callResultat(resultat) {
  axios({
    method: 'get',
    url: `${LOCAL_SERVER}/api/get_result`
  }).then((response) => {
    console.log(response);
    console.log(response.num_yes)
    console.log(response.num_no)
    if (response.status !== 200)
      console.log("ERROR");
    // setErrorMessage("ERROR");
  })
    .catch((error) => {
      // setErrorMessage("catch ERROR");
      console.log("catch ERROR");
    })
}

function callVote(resultat) {
  pubKey = get_pub_key();
  voting_token = get_voting_token();
  console.log(pubKey)
  if (!resultat || !voting_token || !pubKey) {
    console.log("pb variable vide")
    return 300;
  }
  axios({
    method: 'post',
    url: `${STARK_SERVER}/api/vote`,
    data: {
      vote: resultat,
      voting_token: voting_token,
      public_key: pubKey
    }
  }).then((response) => {
    console.log(response);
    if (response.status !== 200)
      console.log("ERROR");
  })
    .catch((error) => {
      console.log("catch ERROR");
    })
}

function ChoiceButton({ value, vote, setVote }) {
  let style = 'btn-grad';
  if (value === vote) style += ' selected-vote';
  return (
    <button
      className={style}
      onClick={() => setVote(value)}>
      {value}
    </button>);
}

function ToggleGroup() {
  const [vote, setVote] = useState(null);
  return <div>
    <ChoiceButton value={'Yes'} vote={vote} setVote={setVote} />
    <ChoiceButton value={'No'} vote={vote} setVote={setVote} />
    <button onClick={() => callVote(vote)}>Send vote</button>
  </div>
}

function VoteInterface({ state }) {
  return (
    <div className="App">
      <header className="App-header">
        {state && state.question && <p>{state.question}</p>}
        <ToggleGroup />
      </header>
    </div>
  );
}

export default VoteInterface;
