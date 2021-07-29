import React from 'react'
import PreviousResult from './PreviousResult';
import CommitInterface from './CommitInterface';
import VoteInterface from './VoteInterface';
import PeriodInfo from './PeriodInfo';
import './myStyles.scss';

function Container({ headerIndex, setHeaderIndex, isConnected, state, delayToCallback, question }) {
    console.log('call Container')
    // console.log("inside container state:", state);
    let currentInterface;

    switch (headerIndex) {
        case 0: case 1:
            currentInterface = <PreviousResult state={state} />
            break;
        case 2: case 3: case 4:
            currentInterface = <CommitInterface headerIndex={headerIndex} state={state} />
            break;
        case 5: case 6:
            currentInterface = <VoteInterface headerIndex={headerIndex} state={state} />
            break;
        default:
            currentInterface = <div>ERROR</div>
    }

    // if (!isConnected)
    //     return <div className={'container'}>
    //         <div>Please connect your web3 wallet</div>
    //         <PeriodInfo index={headerIndex} />
    //     </div>
    // else
    return <div className={'container'}>
        {isConnected ? currentInterface : <div>Please connect your web3 wallet</div>}
        <PeriodInfo index={headerIndex} />
        {/* <Timer delayToCallback={delayToCallback} /> */}
    </div>
};

export default Container