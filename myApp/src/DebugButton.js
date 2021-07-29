import React from 'react'
import "./DebugButton.scss"
import { phases } from './PhaseHeader';

export default function ConnectButton({ headerIndex, setHeaderIndex }) {
	const nextHeader = () => {
		console.log('calling nextHeader()');
		let index = headerIndex;
		index++;
		if (index > phases.length - 1)
			index = 0;
		console.log(index);
		setHeaderIndex(index);
	}
	return (
		<button className={'debug-button'} onClick={() => nextHeader()}>
			next header
		</button>
	)
}