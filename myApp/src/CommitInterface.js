import {useState} from "react"

function CommitInterface() {
    return (
        <div>
            <h1>Prove you're human:</h1>
            <AddressInput/>
        </div>
    )
};

function onAddressSubmit (event) {
    event.preventDefault();
}

function AddressInput() {
    const [inputValue, setInputValue] = useState('default value');

    function saveValue(event) {
        console.log(event.target.value);
        setInputValue(event.target.value);
    }

    return (
      <form onSubmit={onAddressSubmit}>
        <p>{inputValue}</p>
        <input onChange={saveValue} placeholder="Enter address" />
        <button type="submit">Submit</button>
      </form>
    );
  }

export default CommitInterface;