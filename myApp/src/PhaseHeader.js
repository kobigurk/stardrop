import React from 'react'
import PropTypes from 'prop-types'

const styles = {
    backgroundColor: 'red',
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

