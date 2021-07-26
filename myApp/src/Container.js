import React from 'react'
import CommitInterface from './CommitInterface';
import VoteInterface from './VoteInterface';
import { phases } from './PhaseHeader';
import './myStyles.scss';
import { getCurrentState } from './API';

function Container({ headerIndex, setHeaderIndex, isConnected }) {
    let currentInterface;

    const nextHeader = () => {
        let index = headerIndex;
        index++;
        if (index > phases.length - 1)
            index = 0;
        console.log(index);
        setHeaderIndex(index);
        getCurrentState();
    }

    if (headerIndex === 0)
        currentInterface = <CommitInterface isConnected={isConnected} />
    else
        currentInterface = <VoteInterface />
    return (
        <div className={'container'}>
            <button onClick={nextHeader}>Next header</button>
            {currentInterface}
        </div>
    )
};

export default Container