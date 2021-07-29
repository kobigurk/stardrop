import React from 'react'
import './ContainerLayout.scss'

export default function PreviousResult({ state }) {
	let question = 'RIEN';
	let total_no = 0;
	let total_yes = 0;
	if (state && state.previous_results && state.previous_results.question) question = state.previous_results.question;
	if (state && state.previous_results && state.previous_results.total_no) total_no = state.previous_results.total_no;
	if (state && state.previous_results && state.previous_results.total_yes) total_yes = state.previous_results.total_yes;
	return (
		<div className={'container-layout'}>
			<div className={'title'}>Previous vote:</div>
			<div className={'question'}>{question}</div>
			<div className={'deux'}>
				<div>yes: {total_yes}</div>
				<div>no: {total_no}</div>
			</div>
		</div>
	)
}