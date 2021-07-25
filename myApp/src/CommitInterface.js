import {useState} from "react"
import {pubKey, privKey, callGenerateKeys} from './API.js'
// import { myState } from './API'

const axios = require('axios');
let rResult = 42;
let areKeysGenerated = false;

const GenerateKeys = (props) => {
    return (
      <button className={'btn-grad2'} onClick={() => {
        callGenerateKeys();
        props.setAreKeysGenerated(true);
      }}>Generate Keys</button>
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
        <button className={'btn-grad2'} onClick={generateCommitToken}>Generate commit token</button>
    );
  }

export default function CommitInterface(props) {
  let {isConnected, setIsConnected } = props;
  const [areKeysGenerated, setAreKeysGenerated] = useState(false)
  // console.log("FFF:", myState.getIsConnected());
    return (
        <div>
            {!isConnected ? <h1>Please connect your web3 wallet</h1> :
            areKeysGenerated ?
            <CommitToken/> :
            <GenerateKeys setAreKeysGenerated={setAreKeysGenerated}/>
            }
        </div>
    )
};