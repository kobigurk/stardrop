const ethers = require('ethers');

module.exports = async function sign_message(message) {
  let provider;
  let rawSignature;

  window.ethereum.enable().then((provider = new ethers.providers.Web3Provider(window.ethereum)));
  const signer = provider.getSigner();

  // provider = ethers.providers.getDefaultProvider(
  //   'goerli',
  //   '2DWV9SDT3WK71GRR1YYWJRF1XIAPY1NKG6'
  // );
  // const signer = new ethers.Wallet("0x9e78bc7d736ed6f39bc1623e09d62ada9abcd7bc7e71735395b9d4cab91fcd36", provider);

  rawSignature = await signer.signMessage(message);

  return rawSignature;
};