export let pubKey, privKey;
//export let isConnected = false;


const axios = require('axios');

export function get_pub_key() {
    return pubKey;
}

export function get_priv_key() {
    return privKey;
}

export function callGenerateKeys() {
    axios.get('http://192.168.106.112:4242/api/generate_keys')
        .then((response) => {
            if (response.status != 200)
                return;
            console.log(response)
            privKey = response.data[0].private_key;
            pubKey = response.data[0].public_key;
            console.log('call generate pubkey', pubKey);
            console.log('call generate privkeys', privKey);
        })
        .catch((err) => { console.log("ERRRRRRR"); });
}