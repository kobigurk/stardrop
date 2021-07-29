import { STARK_SERVER } from './constants'
import PhaseHeader from './PhaseHeader'
import Container from './Container'
import ConnectButton from './ConnectButton'
import DebugButton from './DebugButton'
import { useEffect, useState } from 'react'
// import { getCurrentState } from './API'
const axios = require('axios');

const ethers = require('ethers')

let pohAddress;
let rawSignature;

export function get_var() {
  return { rawSignature, pohAddress }
}

async function sign_message(callBack) {
  const provider = new ethers.providers.Web3Provider(window.ethereum, 'any');
  await provider.send('eth_requestAccounts', []);
  const signer = provider.getSigner();
  pohAddress = await signer.getAddress();
  // const _network = await provider.getNetwork();
  rawSignature = await signer.signMessage("eip42");
  console.log(rawSignature, pohAddress)
  callBack();
};

function App() {
  const [headerIndex, setHeaderIndex] = useState(0);
  const [isConnected, setIsConnected] = useState(false);//false
  // const [phaseIndex, setPhaseIndex] = useState(-1);
  const [delayToCallback, setTimeToNextCall] = useState(0)
  const [watcher, setWatcher] = useState(0)
  const [state, setState] = useState({})
  console.log('call APP');
  console.log("Delay to callback", delayToCallback)

  useEffect(() => {
    let timer;
    console.log('USE EFFECT get_state');
    axios.get(`${STARK_SERVER}/api/get_state`)
      .then((response) => {
        let { phase, previous_results, question, delay_to_callback } = response.data[0];

        // Ensure we are dealing with ints and not floats
        delay_to_callback = Math.floor(delay_to_callback)

        setState(response.data[0]);
        console.log('RESPONSE:', phase, previous_results, question, delay_to_callback);
        setHeaderIndex(phase);
        setTimeToNextCall(delay_to_callback);
        timer = setTimeout(() => {
          console.log(`PENZOPENZOPENZO This will run after ${delayToCallback} Msecond!, ${headerIndex}`);
          setWatcher(watcher + 1);//A LA PLACELOOP
        }, delayToCallback * 1000);
      })
      .catch((res) => {
        console.log('ERROR in getCurrentState:', res);
      })
    return (() => { clearTimeout(timer) });
  }, [watcher])

  // if (phaseInfo === null) setPhaseInfo(getCurrentState());

  return (
    <>
      <div className={'phase-connect-wrapper'}>
        <PhaseHeader headerIndex={headerIndex} />
        <ConnectButton sign_message={sign_message} isConnected={isConnected} setIsConnected={setIsConnected} />
      </div>
      <Container
        headerIndex={headerIndex}
        setHeaderIndex={setHeaderIndex}
        isConnected={isConnected}
        state={state}
        delayToCallback={delayToCallback}
      />
      <DebugButton headerIndex={headerIndex} setHeaderIndex={setHeaderIndex} />
    </>
  );
}

export default App;