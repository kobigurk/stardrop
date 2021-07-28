import { useEffect, useState } from "react"

export default function Timer({ delayToCallback }) {
	const [timeLeft, setTimeLeft] = useState(delayToCallback);

	useEffect(() => {
	  const timer = setInterval(() => {
	    setTimeLeft(timeLeft - 1);
	  }, 1000);

	return () => clearInterval(timer);
	});

	return (
		<div className={'timer'}>
			Waiting {timeLeft} seconds...
		</div>
	)
}