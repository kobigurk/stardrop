import {useState} from "react"
import { callGenerateKeys } from './API.js'
import { get_var } from './App'
import { get_pub_key } from './API'
import { get_priv_key } from './API'

let pubKey;
let privKey;
const axios = require('axios');
let areKeysGenerated = false;
let commit_token;

export function get_commit_token() {
  return commit_token;
}

const GenerateKeys = (props) => {
    return (
      <div>
      <button onClick={() => {
        callGenerateKeys();
        props.setAreKeysGenerated(true);
      }}>GenerateKeys</button>
      <button onClick={() => {
        callEndCommitPhase()
      }}></button>
      </div>
    )
  
}

function callEndCommitPhase () {
  axios({
    method: 'post',
    url: 'http://192.168.0.44:5000/api/end_commit_phase',
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

function callCommit () {
  privKey = get_priv_key();
  console.log("poh = ", privKey);
  if (!commit_token || !privKey) {
    return 300;
  }
  axios({
    method: 'post',
    url: 'http://192.168.0.44:4242/api/commit',
    data: {
      commit_token : commit_token,
      private_key : privKey
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
    

    function generateCommitToken () {
      const {rawSignature, pohAddress} = get_var();
      pubKey = get_pub_key();
      console.log("poh = ", pubKey);
      if (!rawSignature || !pohAddress || !pubKey) {
        return 300;
      }
      axios({
        method: 'post',
        url: 'http://192.168.0.44:4242/api/generate_commit_token',
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
        <button onClick={generateCommitToken}>Generate commit token</button>
        <button onClick={callCommit}>COMMIT</button>
        <button onClick={callEndCommitPhase}>End Commit Phase</button>
        </div>
    );
  }

export default function CommitInterface() {
  const [areKeysGenerated, setAreKeysGenerated] = useState(false)
    return (
        <div>
            <h1>Wassu wassu wassu wassuuuuupppppp!!!</h1>
            {areKeysGenerated ?
            <CommitToken/> :
            <GenerateKeys setAreKeysGenerated={setAreKeysGenerated}/>}
        </div>   
    )
};