import React from 'react'
import './myStyles.css'

function PhaseHeader(props) {
    let { headerIndex } = props;
    return (
        <div className={'header'}>
            <div className={headerIndex === 0 ? 'selected-header' : ''}>Commit</div>
            <div className={headerIndex === 1 ? 'selected-header' : ''}>Vote</div>
        </div >
    )
}

export default PhaseHeader