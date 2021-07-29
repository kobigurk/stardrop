import React from 'react'
import './PhaseHeader.scss'

export const phases = ['Deploy Contract', 'Init Contract', 'Registration Period', 'End Registration', 'Server Key Reveal', 'Voting Period', 'End Voting'];

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