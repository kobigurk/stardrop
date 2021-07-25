const sign_message = require('./sign_message');

async function main() {
    let signer_address;
    let rawSignature;
    const blinded_request = "eip42";
    [rawSignature, signer_address] = await sign_message(blinded_request);

    console.log(rawSignature, signer_address);
};

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });