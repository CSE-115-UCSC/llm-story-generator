import { Fragment, useState, useCallback } from 'react';

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
  const [prompt, setPrompt] = useState("");

  // wrap the hook and pass the function name to the prompt field
  const wrapperSetPrompt = useCallback(prompt => {
    setPrompt(prompt);
  }, [setPrompt]);

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
      <p>{prompt}</p>
      <PromptField submitPrompt={wrapperSetPrompt}/>
    </Stack>
  );
}

function PromptField({submitPrompt}) {

  const handleSubmit = (e) => {
    submitPrompt(e.target[0].value)
    e.target[0].value = ""
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
