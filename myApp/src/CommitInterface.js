import { useState } from "react"
import { callGenerateKeys } from './API.js'
import { get_var } from './App'
import { get_pub_key } from './API'
import { get_priv_key } from './API'

const axios = require('axios');
let areKeysGenerated = false;
let commit_token;
let privKey;
let pubKey;

export function get_commit_token() {
  return commit_token;
}



const GenerateKeys = (props) => {
  return (
    <div>
      <button className={'btn-grad2'} onClick={() => {
        callGenerateKeys();
        props.setAreKeysGenerated(true);
      }}>Generate Keys</button>
    </div>
  )

}

function callEndCommitPhase() {
  axios({
    method: 'post',
    url: 'http://192.168.106.112:5000/api/end_commit_phase',
    data: {
      message: "vitalik<3"
    }
  })
    .then((response) => {
      console.log(response);
    })
    .catch((error) => {
      console.log("catch ERROR");
    })
}

function callCommit() {
  privKey = get_priv_key();
  console.log("poh = ", privKey);
  if (!commit_token || !privKey) {
    return 300;
  }
  axios({
    method: 'post',
    url: 'http://192.168.106.112:4242/api/commit',
    data: {
      commit_token: commit_token,
      private_key: privKey
    }
  }).then((response) => {
    console.log(response);
    if (response.status != 200)
      console.log("error")
  })
    .catch((error) => {
      console.log("error")
    })
}

const CommitToken = () => {
  const [inputValue, setInputValue] = useState('default value');
  const [errorMessage, setErrorMessage] = useState('');

  function generateCommitToken() {
    const { rawSignature, pohAddress } = get_var();
    pubKey = get_pub_key();
    console.log("poh = ", pubKey);
    if (!rawSignature || !pohAddress || !pubKey) {
      return 300;
    }
    axios({
      method: 'post',
      url: 'http://192.168.106.112:4242/api/generate_commit_token',
      data: {
        poh_address: pohAddress,
        signature: rawSignature,
        public_key: pubKey
      }
    }).then((response) => {
      console.log(response.data[0].commit_token);
      commit_token = response.data[0].commit_token;
      if (response.status != 200)
        setErrorMessage("ERROR");
    })
      .catch((error) => {
        setErrorMessage("catch ERROR");
      })
  }

  function saveValue(event) {
    console.log(event.target.value);
    setInputValue(event.target.value);
  }

  return (
    <div>
      <button className={'btn-grad'} onClick={generateCommitToken}>Generate commit token</button>
      <button className={'btn-grad'} onClick={callCommit}>COMMIT</button>
      <button className={'btn-grad'} onClick={callEndCommitPhase}>End Commit Phase</button>
    </div>
  );
}

export default function CommitInterface(props) {
  let { isConnected, setIsConnected } = props;
  const [areKeysGenerated, setAreKeysGenerated] = useState(false)
  // console.log("FFF:", myState.getIsConnected());
  return (
    <div>
      {!isConnected ? <h1>Please connect your web3 wallet</h1> :
        areKeysGenerated ?
          <CommitToken /> :
          <GenerateKeys setAreKeysGenerated={setAreKeysGenerated} />
      }
    </div>
  )
};