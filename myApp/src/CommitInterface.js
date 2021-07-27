import { useState } from "react"
import { callGenerateKeys } from './API.js'
import { get_var } from './App'
import { get_pub_key } from './API'
import { get_priv_key } from './API'
import { STARK_SERVER, LOCAL_SERVER } from "./constants.js"

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

function initCommitToVote() {
  console.log('GETTING TABOUILLED');
  callGenerateKeys(
    () => {
      generateCommitToken(
        () => {
          callCommit()
        })
    });
}

function CommitToVoteButton({ }) {
  return <button className={'btn-grad'} onClick={initCommitToVote}>Commit to next vote</button>
}

export default function CommitInterface({ state }) {
  return (
    <div>
      {state.question}
      {state.phase === 2 && <CommitToVoteButton />}
    </div>
  )
};