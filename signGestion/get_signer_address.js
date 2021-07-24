const ethers = require('ethers');

async function main() {
    const rawSignature = process.argv[2];
    const message = process.argv[3];
    const address_suppose_tobe = process.argv[4];
    let provider;

  window.ethereum.enable().then((provider = new ethers.providers.Web3Provider(window.ethereum)));

//   provider = ethers.providers.getDefaultProvider(
//     'goerli',
//     '2DWV9SDT3WK71GRR1YYWJRF1XIAPY1NKG6'
//   );

  const signerAddress = ethers.utils.verifyMessage(message, rawSignature);

  if (address_suppose_tobe.toString() == signerAddress.toString()) {
    console.log(0);
  }
  else {
    console.log(1);
  }
};

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });