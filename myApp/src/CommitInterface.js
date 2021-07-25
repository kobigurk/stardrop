import {useState} from "react"
import {pubKey, privKey, callGenerateKeys } from './API.js'
import { get_var } from './App'

const axios = require('axios');
let areKeysGenerated = false;

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
  axios.get('http://192.168.0.44:4242/api/end_commit_phase', {params : {message: "vitalik<3"}})
      .then((response) => {
          console.log(response);
          if (response.status != 200) 
            setErrorMessage("ERROR");
      })
      .catch((error) => {
          setErrorMessage("catch ERROR");
      })
}

const CommitToken = () => {
    const [inputValue, setInputValue] = useState('default value');
    const [errorMessage, setErrorMessage] = useState('');

    function generateCommitToken () {
      const {rawSignature, pohAddress} = get_var();
      axios.get('http://192.168.0.44:4242/api/generate_commit_token', { params: {
        poh_address: pohAddress,
        signature: rawSignature,
        public_key: pubKey
      }})
          .then((response) => {
              console.log(response);
              if (response.status != 200) 
                setErrorMessage("ERROR");
             rResult = response.data[0].commit_token.sdf;
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
        <button onClick={callEndCommitPhase}>End Commit Phase</button>
        </div>
    );
  }

export default function CommitInterface() {
  const [areKeysGenerated, setAreKeysGenerated] = useState(false)
    return (
        <div>
            <h1>bonsoir</h1>
            {areKeysGenerated ?
            <CommitToken/> :
            <GenerateKeys setAreKeysGenerated={setAreKeysGenerated}/>}
        </div>
        
    )
};