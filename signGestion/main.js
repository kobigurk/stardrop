const sign_blinded_request = require('./sign_blinded_request');
const get_signer_address = require("./get_signer_address");

async function main() {
    const blinded_request = "lol";
    const rawSignature = await sign_blinded_request(blinded_request);
    const signer_address = await get_signer_address(rawSignature, blinded_request);

    console.log(signer_address);
    return signer_address;
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });