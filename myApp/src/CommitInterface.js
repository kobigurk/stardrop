import {useState} from "react"

const axios = require('axios');
let rResult = 42;

function CommitInterface() {
    return (
        <div>
            <h1>Prove you're human:</h1>
            <AddressInput/>
        </div>
    )
};

const AddressInput = () => {
    const [inputValue, setInputValue] = useState('default value');
    const [errorMessage, setErrorMessage] = useState('');

    function onAddressSubmit (event) {
      axios.post('http://192.168.106.112:5000/api/request_token?address=0xDD2b3f1d3a4f08622a25a3f75284fC01ad0c5CcA')
          .then((response) => {
              console.log(response);
              if (response.status != 200) 
                setErrorMessage("POH address not found");
              rResult = response.data[0].commit_token.sdf;
          })
          .catch((error) => {
              setErrorMessage("POH address not found");
          })
      event.preventDefault();
    }

    function saveValue(event) {
        console.log(event.target.value);
        setInputValue(event.target.value);
    }

    return (
      <form onSubmit={onAddressSubmit}>
        <p>{errorMessage}</p>
        <input onChange={saveValue} placeholder="Enter address" />
        <button type="submit">Submit</button>
      </form>
    );
  }

function sendRResult() {
    axios.get('http://192.168.106.112:5000/api/generate_keys');
}

export default CommitInterface;