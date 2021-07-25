import {useState} from "react"
import {pubKey, privKey, callGenerateKeys } from './API.js'

const axios = require('axios');
//let rResult = 42;
let areKeysGenerated = false;

const GenerateKeys = (props) => {
    return (
      <button onClick={() => {
        callGenerateKeys();
        props.setAreKeysGenerated(true);
      }}>GenerateKeys</button>
    )
  
}

const CommitToken = () => {
    const [inputValue, setInputValue] = useState('default value');
    const [errorMessage, setErrorMessage] = useState('');

    function generateCommitToken () {
      axios.get('http://192.168.0.44:4242/api/generate_commit_token', {}, { params: {
      }})
          .then((response) => {
              console.log(response);
              if (response.status != 200) 
                setErrorMessage("ERROR");
             // rResult = response.data[0].commit_token.sdf;
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
        <button onClick={generateCommitToken}>Generate commit token</button>
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