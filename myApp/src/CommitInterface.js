import { callGenerateKeys } from './API.js'
import { get_var } from './App'
import { get_pub_key } from './API'
import { get_priv_key } from './API'
import { LOCAL_SERVER } from "./constants.js"
import { useState } from 'react'
import Timer from './Timer';
import "./ConnectButton.scss"

const axios = require('axios');
let commit_token;
let privKey;
let pubKey;
let voting_token;

export function get_commit_token() {
  return commit_token;
}

export function get_voting_token() {
  return voting_token;
}

export function reset_tokens() {
  voting_token = null;
  commit_token = null;
}

function callCommit() {
  privKey = get_priv_key();
  console.log("commit = ", commit_token);
  if (!commit_token || !privKey) return 300;
  axios({
    method: 'post',
    url: `${LOCAL_SERVER}/api/commit`,
    data: {
      commit_token: commit_token,
      private_key: privKey
    }
  }).then((response) => {
    console.log(response);
    if (response.status !== 200)
      console.log("error")
    else console.log('BIG SUCCESS');
  })
    .catch((error) => {
      console.log("error")
    })
}

function generateCommitToken(callBack) {
  const { rawSignature, pohAddress } = get_var();
  pubKey = get_pub_key();
  console.log("poh = ", pubKey);
  if (!rawSignature || !pohAddress || !pubKey) return 300;
  axios({
    method: 'post',
    url: `${LOCAL_SERVER}/api/generate_commit_token`,
    data: {
      poh_address: pohAddress,
      signature: rawSignature,
      public_key: pubKey
    }
  }).then((response) => {
    console.log(response.data[0].commit_token);
    commit_token = response.data[0].commit_token;
    voting_token = response.data[0].voting_token;

    console.log(voting_token)
    callBack()
    // if (response.status !== 200)
    //   setErrorMessage("ERROR");
  })
    .catch((error) => {
      // setErrorMessage("catch ERROR");
    })
}

function initCommitToVote(setHasCommitted) {
  console.log('GETTING TABOUILLED');
  setHasCommitted(true);
  callGenerateKeys(
    () => {
      generateCommitToken(
        () => {
          callCommit()
        })
    });
}

function CommitToVoteButton() {
  const [hasCommitted, setHasCommitted] = useState(false);

  return <button className={`${hasCommitted ? 'btn-grad rekt' : 'btn-grad'} `} onClick={() => initCommitToVote(setHasCommitted)}>
    {hasCommitted ? 'Registered to next vote!' : 'Register to next vote'}
  </button>
}

export default function CommitInterface({ headerIndex, state }) {
  return (
    <div className={'container-layout'}>
      <div className={'question'}>{state.question}</div>
      {headerIndex === 2 &&
        <><CommitToVoteButton />
          <Timer className={'timer'} delayToCallback={state.delay_to_callback} />
        </>
      }
    </div>
  )
};