import './myStyles.css';
import { get_pub_key } from './API'
import { get_voting_token } from './CommitInterface'
const axios = require('axios');
let pubKey;
let voting_token;

function callEndVotingPhase(resultat) {
  pubKey = get_pub_key();
  axios({
    method: 'post',
    url: 'http://172.17.0.03:5000/api/end_voting_phase',
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
    url: 'http://172.17.0.03:4242/api/get_result'
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
    url: 'http://172.17.0.03:5000/api/vote',
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

function ToggleGroup() {
  return <div>
    <button className={'btn-grad2'} onClick={() => callVote('Yes')}>YES</button>
    <button className={'btn-grad2'} onClick={() => callVote('No')}>NO</button>
    <button onClick={callEndVotingPhase}>END VOTING PHASE</button>
    <button onClick={callResultat}>CALL RESULTAT</button>
  </div>
}

function VoteInterface() {
  return (
    <div className="App">
      <header className="App-header">
        SHOULD CARLOS MATOS PRESIDE THE ETHEREUM FOUNDATION ?
        <ToggleGroup />
      </header>
    </div>
  );
}

export default VoteInterface;
