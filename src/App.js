import CommitInterfacee from './CommitInterface'
import VoteInterface from './VoteInterface'
import PhaseHeader from './PhaseHeader'
import Container from './Container'
import {useState} from 'react' 

const styles = {
    backgroundColor:'blue'
}
const axios = require('axios');
axios.post('http://192.168.106.112:5000/api/request_token?address=0xDD2b3f1d3a4f08622a25a3f75284fC01ad0c5CcA')
    .then((response) => {
        console.log(response.data);
    })
    .catch((error) => {
        console.log(error);
    })


function App() {
    console.log(axios);
    const [headerIndex, setHeaderIndex] = useState(0);

    return (
        <div>
        <PhaseHeader/>
        <Container headerIndex={headerIndex} setHeaderIndex={setHeaderIndex}/>
        </div>
    );
}

export default App;