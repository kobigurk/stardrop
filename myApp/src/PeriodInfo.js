import React from 'react'
import './PeriodInfo.scss';

const INFOS = [
	'The server is deploying the smart contract on Starknet.',
	'The server sent the initialization transaction to the smart contract. The server is waiting for the transaction to be confirmed by Starknet.',
	'Users can now register to the next voting round. We removed the Proof of Humanity check for the demo, but your address would be checked here.',
	'The smart contract is ending the registration period. It will no longer accept new registrations.',
	'The server sent its private key to the smart contract. The server is waiting for the transaction to be confirmed by Starknet',
	'Users who registered during the registration period can now cast their votes!',
	'The smart contract is ending the voting period. Results will be computed after this transaction gets confirmed.'
]

export default function PeriodInfo({ index }) {
	return (
		<div className={'period-info'}>
			<p>What's happening ?</p>
			{INFOS[index]}
		</div>
	)
}