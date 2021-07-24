import React from 'react'
import CommitInterface from './CommitInterface';
import SendInterface from './SendInterface';
import VoteInterface from './VoteInterface';

const styles = {
    backgroundColor: 'blue',
}

function Container(props) {
    let {headerIndex, setHeaderIndex} = props;
    let which;

    const nextHeader = () => {
        let index = headerIndex;
        index++;
        if (index > 2)
            index = 0;
        console.log(index);
        setHeaderIndex(index);
    }

    if (headerIndex == 0)
        which = <CommitInterface/>
    else if (headerIndex == 1)
        which = <SendInterface/>
    else
        which = <VoteInterface/>
    return (
        <div style={styles}>
            <button onClick={nextHeader}>Next header</button>
            {which}
        </div>
    )
};

export default Container