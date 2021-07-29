import React from 'react'
import './PeriodInfo.scss';

const INFOS = [
	'Deploying smart contract on Starknet.',
	'Initializing smart contract.',
	'Users can now register to the next voting round.',
	'Ending the registration period. The smart contract will longer accept new registration tokens.',
	'The server reveals its private key by sending it to the smart contract.',
	'Users who registered during the registration period can now cast their votes.',
	'Ending the voting period. Results will be computed after this step.'
]

export default function PeriodInfo({ index }) {
	return (
		<div className={'period-info'}>
			<p>What's happening ?</p>
			{INFOS[index]}
		</div>
	)
}