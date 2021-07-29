import React from 'react'
import './PhaseHeader.scss'

export const phases = ['Deploy Contract', 'Init Contract', 'Registration Period', 'End Registration', 'Server Key Reveal', 'Voting Period', 'End Voting'];

function PhaseName({ index, currentIndex, children }) {
    return <div
        className={currentIndex === index ? 'selected-header' : ''}>
        {children}
    </div>
}

export default function PhaseHeader({ headerIndex }) {
    return (
        <div className={'header'}>
            {phases.map((children, index) => <React.Fragment key={'phase-header' + index}>
                <PhaseName index={index} currentIndex={headerIndex}>
                    {children}
                </PhaseName>
                {(index < phases.length - 1) && '>'}
            </React.Fragment>)}
        </div >
    )
}