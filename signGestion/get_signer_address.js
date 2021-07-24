const ethers = require('ethers');

module.exports = async function sign_blinded_request(rawSignature, blinded_request) {
  let provider;

  window.ethereum.enable().then((provider = new ethers.providers.Web3Provider(window.ethereum)));

//   provider = ethers.providers.getDefaultProvider(
//     'goerli',
//     '2DWV9SDT3WK71GRR1YYWJRF1XIAPY1NKG6'
//   );

  const signerAddress = ethers.utils.verifyMessage(blinded_request, rawSignature);

  return signerAddress;
};