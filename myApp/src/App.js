import CommitInterfacee from './CommitInterface'
import VoteInterface from './VoteInterface'
import PhaseHeader from './PhaseHeader'
import Container from './Container'
import {useState} from 'react' 

const styles = {
    backgroundColor:'blue'
}

function App() {
    const [headerIndex, setHeaderIndex] = useState(0);

    return (
        <div>
        <PhaseHeader/>
        <Container headerIndex={headerIndex} setHeaderIndex={setHeaderIndex}/>
        </div>
    );
}

export default App;