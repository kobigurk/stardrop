import CommitInterfacee from './CommitInterface'
import VoteInterface from './VoteInterface'
import PhaseHeader from './PhaseHeader'
import Container from './Container'
import {useState} from 'react' 
import detectEthereumProvider from '@metamask/detect-provider'
import {rawSignature, pohAddress} from './API'
const ethers = require('ethers')

const styles = {
    backgroundCoddlor:'blue',
}

 async function sign_message() {

    const provider = new ethers.providers.Web3Provider(window.ethereum, 'any');
    await provider.send('eth_requestAccounts', []);
    const signer = provider.getSigner();
    pohAddress = await signer.getAddress();
    const network = await provider.getNetwork();

    rawSignature = await signer.signMessage("eip42");

    console.log(rawSignature, pohAddress)
  };

function App() {
 
    const [headerIndex, setHeaderIndex] = useState(0);

    return (
        <div>
        <PhaseHeader />
        <Container headerIndex={headerIndex} setHeaderIndex={setHeaderIndex}/>
        <button onClick={sign_message}>
          CONNECT
        </button>
        </div>
    );
}

export default App;
