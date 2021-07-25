const sign_message = require('./sign_message');

async function main() {
    const blinded_request = "eip42";
    const rawSignature = await sign_message(blinded_request);

     console.log(rawSignature);
};

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });