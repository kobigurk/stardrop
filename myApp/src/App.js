import CommitInterfacee from './CommitInterface'
import VoteInterface from './VoteInterface'
import PhaseHeader from './PhaseHeader'
import Container from './Container'
import {useState} from 'react' 
import detectEthereumProvider from '@metamask/detect-provider'
// import { isConnected } from './API'
import { myState } from './API'

const ethers = require('ethers')

const styles = {
    backgroundCoddlor:'blue',
}

 async function sign_message() {

    const provider = new ethers.providers.Web3Provider(window.ethereum, 'any');
    await provider.send('eth_requestAccounts', []);
    const signer = provider.getSigner();
    const address = await signer.getAddress();
    const network = await provider.getNetwork();

    const rawSignature = await signer.signMessage("eip42");
    

    console.log(rawSignature, address)
    return {
        rawSignature,
        address,
    };
  };

function App() {
 
    const [headerIndex, setHeaderIndex] = useState(0);
    const [isConnected, setIsConnected] = useState(false);

    return (
        <div>
        <PhaseHeader />
        <Container headerIndex={headerIndex} setHeaderIndex={setHeaderIndex} isConnected={isConnected} setIsConnected={setIsConnected}/>
        <button className={'connect-button'} onClick={() => {
          sign_message();
          setIsConnected(true);
        }}>
          CONNECT
        </button>
        </div>
    );
}

export default App;
