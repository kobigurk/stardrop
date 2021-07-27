import { LOCAL_SERVER, STARK_SERVER } from "./constants"
const axios = require('axios');

export let pubKey, privKey;

export function get_pub_key() {
    return pubKey;
}

export function get_priv_key() {
    return privKey;
}

export function callGenerateKeys(callBack) {
    console.log('callGenerateKeys just clicked');
    axios.get(`${LOCAL_SERVER}/api/generate_keys`)
        .then((response) => {
            if (response.status !== 200) {
                console.log(response);
                return;
            }
            console.log(response)
            privKey = response.data[0].private_key;
            pubKey = response.data[0].public_key;
            console.log('call generate pubkey', pubKey);
            console.log('call generate privkeys', privKey);
            callBack()
        })
        .catch((err) => { console.log("ERRRRRRR"); });
}

export async function getCurrentState(prevValue, callBack) {
    console.log('call getCurrentState')
    // console.log(new Date());
    await axios.get(`${STARK_SERVER}/api/get_state`)
        .then((response) => {
            let { phase, previous_results, question, delay_to_callback } = response.data[0];
            console.log('TEST', phase, previous_results, question, delay_to_callback)
            // console.log('Time to wait:', timeToWait);
            if (prevValue !== phase) {
                console.log('USING CALLBACK')
                callBack(phase);
            }
            return [phase, delay_to_callback];
        })
        .catch((res) => {
            console.log('ERROR in getCurrentState')
        })
    // return [-1, 1000];
}