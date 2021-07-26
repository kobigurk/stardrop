import React from 'react'
import './PhaseHeader.scss'

function PhaseName({ index, currentIndex, children }) {
    return <div
        className={currentIndex === index ? 'selected-header' : ''}>
        {children}
    </div>
}

export default function PhaseHeader({ headerIndex }) {
    return (
        <div className={'header'}>
            <PhaseName index={0} currentIndex={headerIndex}>
                Commit Phase
            </PhaseName>
            <PhaseName index={1} currentIndex={headerIndex}>
                Vote Phase
            </PhaseName>
        </div >
    )
}