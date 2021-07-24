import {useState} from "react"

function VoteInterface() {
    const [VoteResult, SetVoteResult] = useState('default value');
    return (
        <div>
            <h1>Should Carlos Matos become president of the Ethereum foundation ?</h1>
            <button type="pick1">Yes</button>
            <button type="pick2">No</button>
        </div>
    )
};

export default VoteInterface;