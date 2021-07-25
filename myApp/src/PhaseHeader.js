import React from 'react'
import PropTypes from 'prop-types'
import { findByLabelText } from '@testing-library/react'
import './myStyles.css'

//const styles = {
//    borderRadius: "12px",
//    maxWidth: "400px",
//    width: "50%",
//    borderRadius: "20px",
//    backgroundColor: 'red',
//}

const styles = {
    justifyContent: 'space-evenly',
    display: 'flex',
    maxWidth: "400px",
    //    width: "50%",
    height: "20px",
    borderRadius: "20px",
}

function PhaseHeader(props) {
    let { headerIndex } = props;
    return (
        <div className={'header'}>
            <div className={headerIndex == 0 ? 'selected-header' : ''}>Commit</div>
            <div className={headerIndex == 1 ? 'selected-header' : ''}>Vote</div>
        </div >
    )
}

export default PhaseHeader