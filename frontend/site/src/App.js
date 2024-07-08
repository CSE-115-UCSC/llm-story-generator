import { Fragment, useState, ChangeEvent } from 'react';

import Paper from '@mui/material/Paper';
import InputBase from '@mui/material/InputBase';
import IconButton from '@mui/material/IconButton';

import './App.css';

function App() {
  
  return (
    <div className="App">
      <header className="App-header">
        <CustomizedInputBase/>
      </header>
    </div>
  );
}

function CustomizedInputBase() {
  const [prompt, setPrompt] = useState("def");

  const handleSubmit = (e) => {
    console.log('submit called');
    setPrompt(e.target[0].value)
    e.preventDefault()
    // we need to add the flask api call here.
  }

  return (
    <Fragment>
    {prompt}
    <Paper
      component="form"
      onSubmit={handleSubmit}
      sx={{ p: '2px 4px', display: 'flex', alignItems: 'center', width: 400,  borderRadius: 8 }}
    >
      <InputBase
        sx={{ ml: 1, flex: 1}}
        placeholder="Message Veracity"
      />
      <IconButton type="submit" sx={{ p: '10px'}} aria-label="menu">
      </IconButton>
    </Paper>
    </Fragment>
  );
}

export default App;
