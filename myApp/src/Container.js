import React from 'react'
import CommitInterface from './CommitInterface';
import VoteInterface from './VoteInterface';
import './myStyles.scss';

function Container({ headerIndex, setHeaderIndex, isConnected }) {
    // let { headerIndex, setHeaderIndex } = props;
    // let { isConnected } = props;
    let which;

    const nextHeader = () => {
        let index = headerIndex;
        index++;
        if (index > 1)
            index = 0;
        console.log(index);
        setHeaderIndex(index);
    }

    if (headerIndex === 0)
        which = <CommitInterface isConnected={isConnected} />
    else
        which = <VoteInterface />
    return (
        <div className={'container'}>
            <button onClick={nextHeader}>Next header</button>
            {which}
        </div>
    )
};

export default Container