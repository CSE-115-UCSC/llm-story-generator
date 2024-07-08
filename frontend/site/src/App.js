import { Fragment, useState, ChangeEvent } from 'react';

import Paper from '@mui/material/Paper';
import InputBase from '@mui/material/InputBase';
import IconButton from '@mui/material/IconButton';
import Stack from '@mui/material/Stack';
import Box from '@mui/material/Box';

import { ThemeProvider, createTheme } from '@mui/material/styles';
import './App.css';

const theme = createTheme({
  components: {
    MuiStack: {
      defaultProps: {
        useFlexGap: true,
      },
    },
  },
});

function App() {
  
  return (
    <div>
      <ThemeProvider theme={theme}>
        <Conversation/>
      </ThemeProvider>
    </div>

  );
}

function Conversation() {
  return (
    <Stack
      direction="column"
      justifyContent="flex-start"
      alignItems="center"
      spacing={0.5}
    >
      <Box height={400}
      width={400}
      display="center"
      justifyContent="center"
      alignItems="center"
      >
        <p>How can I help you today?</p>
      </Box>
      <PromptField/>
    </Stack>
  );
}

function PromptField() {
  const [prompt, setPrompt] = useState("def");

  const handleSubmit = (e) => {
    console.log('submit called');
    setPrompt(e.target[0].value)
    e.preventDefault()
    // we need to add the flask api call here.
  }

  return (
    <Fragment>
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
