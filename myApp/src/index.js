import App from './App';
import { StrictMode } from 'react';
import ReactDOM from 'react-dom';

console.log("LOADING INDEX");

ReactDOM.render(
    // <StrictMode>
    <App />
    // </StrictMode>
    , document.getElementById('root')
)