import React from 'react'
import { get_var } from "./App"
import "./ConnectButton.scss"

export default function ConnectButton({ sign_message, isConnected, setIsConnected }) {
	let { pohAddress } = get_var();
	let walletAddress;

	if (pohAddress) walletAddress = pohAddress.slice(0, 7) + '...' + pohAddress.slice(-4, -1)

	return (
		<button className={`connect-button ${isConnected ? 'disabled' : ''}`} onClick={() => {
			sign_message(() => { setIsConnected(true) });
		}}>
			{isConnected
				? walletAddress
				: "Connect Wallet"}
		</button>
	)
}