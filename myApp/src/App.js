import CommitInterfacee from './CommitInterface'
import VoteInterface from './VoteInterface'
import PhaseHeader from './PhaseHeader'
import Container from './Container'
import { useState } from 'react'
import detectEthereumProvider from '@metamask/detect-provider'
// import { isConnected } from './API'

const ethers = require('ethers')

let pohAddress;
let rawSignature;

const styles = {
  backgroundCoddlor: 'blue',
}

export function get_var() {
  return { rawSignature, pohAddress }
}

async function sign_message(callBack) {

  const provider = new ethers.providers.Web3Provider(window.ethereum, 'any');
  await provider.send('eth_requestAccounts', []);
  const signer = provider.getSigner();
  pohAddress = await signer.getAddress();
  const network = await provider.getNetwork();

  rawSignature = await signer.signMessage("eip42");


  console.log(rawSignature, pohAddress)
  callBack();
};

function App() {

  const [headerIndex, setHeaderIndex] = useState(0);
  const [isConnected, setIsConnected] = useState(false);

  return (
    <div>
      <PhaseHeader headerIndex={headerIndex} />
      <Container headerIndex={headerIndex} setHeaderIndex={setHeaderIndex} isConnected={isConnected} setIsConnected={setIsConnected} />
      <button className={'connect-button'} onClick={() => {
        sign_message(() => { setIsConnected(true) });
        // setIsConnected(true);
      }}>
        CONNECT
      </button>
    </div>
  );
}

export default App;
