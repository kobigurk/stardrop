import React from 'react'
import './PhaseHeader.scss'

export const phases = ['Deploy SC', 'Init SC', 'Commit Phase', 'End Commit', 'Server Key Reveal', 'Voting Phase', 'End Voting'];

// function PhaseName({ index, currentIndex, children }) {
//     return <div>
//         {children}
//     </div>
// }

export default function PhaseHeader({ headerIndex }) {
    return (
        <div className={'header'}>
            {phases.map((phaseName, index) => <React.Fragment key={'phase-header' + index}>
                <div className={headerIndex === index ? 'selected-header' : ''}>
                    {phaseName}
                </div>
                {(index < phases.length - 1) && '·'}
            </React.Fragment>)}
        </div >
    )
}