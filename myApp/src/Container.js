import React from 'react'
import PreviousResult from './PreviousResult';
import CommitInterface from './CommitInterface';
import VoteInterface from './VoteInterface';
import { phases } from './PhaseHeader';
import './myStyles.scss';

function Container({ headerIndex, setHeaderIndex, isConnected, state }) {
    console.log('call Container')
    console.log("inside container state:", state);
    let currentInterface;

    //For debuging purposes
    const nextHeader = () => {
        console.log('calling nextHeader()');
        let index = headerIndex;
        index++;
        if (index > phases.length - 1)
            index = 0;
        console.log(index);
        setHeaderIndex(index);
    }

    switch (headerIndex) {
        case 0: case 1:
            currentInterface = <PreviousResult state={state} />
            break;
        case 2: case 3: case 4:
            currentInterface = <CommitInterface headerIndex={headerIndex} state={state} />
            break;
        case 5: case 6:
            currentInterface = <VoteInterface headerIndex={headerIndex} />
            break;
        default:
            currentInterface = <div>ERROR</div>
    }

    if (!isConnected)
        return <div className={'container'}>Please connect your web3 wallet</div>
    else
        return <div className={'container'}>
            {/* <button onClick={nextHeader}>Next header</button> */}
            {currentInterface}
        </div>
};

export default Container