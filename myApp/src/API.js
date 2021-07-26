import { LOCAL_SERVER, STARK_SERVER } from "./constants"
const axios = require('axios');

export let pubKey, privKey;

export function get_pub_key() {
    return pubKey;
}

export function get_priv_key() {
    return privKey;
}

export function callGenerateKeys() {
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
        })
        .catch((err) => { console.log("ERRRRRRR"); });
}