import React from 'react'
import CommitInterface from './CommitInterface';
import SendInterface from './SendInterface';
import VoteInterface from './VoteInterface';
import './myStyles.css';

const styles = {
    position: "absolute",
    top: "50%",
    left: "50%",
    transform: "translate(-50%, -50%)",
    backgroundColor: 'blue',
    maxWidth: "400px",
    width: "50%",
    height: "50%",
    borderRadius: "20px",
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
        <div className={'container'}>
            <button onClick={nextHeader}>Next header</button>
            {which}
        </div>
    )
};

export default Container