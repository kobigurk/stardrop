import React from 'react'
import PropTypes from 'prop-types'
import { findByLabelText } from '@testing-library/react'

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
    backgroundColor: 'blue',
    maxWidth: "400px",
//    width: "50%",
    height: "20px",
    borderRadius: "20px",
}

function PhaseHeader(props) {
    return (
        <div style={styles}>
          <div>Commit</div>  
          <div>Send</div>  
          <div>Vote</div>  
        </div>
    )
}

export default PhaseHeader

