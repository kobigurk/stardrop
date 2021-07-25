import { data } from 'browserslist';

export let pubKey, privKey;
//export let isConnected = false;


const axios = require('axios');

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

//export const myState = new function(initialValue) {
//    this.isConnected = initialValue;
//
//    this.getIsConnected = () => {
//        return this.isConnected;
//    }
//
//    this.setIsConnected = (value) => {
//        this.isConnected = value;
//    }
//}

// export const myState = mygetState(false);