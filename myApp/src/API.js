import { data } from 'browserslist';
import { get_var } from './App'

export let pubKey, privKey;

const axios = require('axios');
let commitToken;

export function get_commit_token() {
    return commitToken;
}

export function callGenerateCommitToken() {
    const {rawSignature, pohAddress} = get_var();
    axios.post('http://192.168.0.44:4242/api/generate_commit_token', {
        poh_address: pohAddress,
        signature: rawSignature,
        public_key: pubKey
    })
    .then((response) => {
        if (response.status != 200)
            return;
        console.log(response)
        commitToken = response.data[0].commitToken
    })
    .catch((err) => {console.log("ERRRRRRR");});
}

export function callGenerateKeys() {
    axios.get('http://192.168.0.44:4242/api/generate_keys')
    .then((response) => {
        if (response.status != 200)
            return;
        console.log(response)
        privKey = response.data[0].private_key;
        pubKey = response.data[0].public_key;
        console.log('call generate pubkey', pubKey);
        console.log('call generate privkeys', privKey);
    })
    .catch((err) => {console.log("ERRRRRRR");});
}