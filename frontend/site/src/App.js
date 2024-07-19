import { ThemeProvider } from '@mui/material/styles';
import React, { useState } from 'react';
import { Container, Box, Button, InputBase, Typography, CssBaseline, Paper, styled, Tab, Tabs } from '@mui/material';
import Content from './Content';
import Chat from './Chat';
import theme from './theme';

const ChaptersContainer = styled(Paper)({
  width: '100%',
  height: '100%', 
  backgroundColor: '#f0f0f0',
  padding: '10px',
  boxSizing: 'border-box',
});

const ChatInputContainer = styled(Box)(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  padding: '10px',
  borderTop: `1px solid ${theme.palette.divider}`,
  backgroundColor: theme.palette.background.default,
}));

const StyledInputBase = styled(InputBase)(({ theme }) => ({
  flexGrow: 1,
  padding: '10px',
  borderRadius: '20px',
  backgroundColor: theme.palette.custom.inputField.background,
  marginRight: '10px',
  color: theme.palette.custom.inputField.text,
}));

const ChatMessage = styled(Box)(({ user, theme }) => ({
  display: 'flex',
  alignItems: 'center',
  marginLeft: '8px',
  padding: '10px',
  borderRadius: '5px',
  backgroundColor: user ? theme.palette.custom.messageBubble.user.background : theme.palette.custom.messageBubble.bot.background,
  color: user ? theme.palette.custom.messageBubble.user.text : theme.palette.custom.messageBubble.bot.text,
  maxWidth: '80%',
}));

function App() {
  // State to manage the current view (chapters, summaries, characters)
  const [view, setView] = useState('chapters');
  
  return (
	<ThemeProvider theme={theme}>
    <CssBaseline />
    <Container disableGutters maxWidth={false} sx={{ height: '100vh', display: 'flex' }}>
      <Box width="40%" height="100%">
        <ChaptersContainer>
          <Content />
        </ChaptersContainer>
      </Box>
      <Box width="60%" height="100%">
        <Chat />
      </Box>
    </Container>
	</ThemeProvider>
  );
}
/*
// Chat component for the left sidebar
function Chat() {
  const [message, setMessage] = useState("");
  const [prompt, setPrompt] = useState("")

  const getLLMResponse = () => {
    setPrompt("")
    fetch('http://127.0.0.1:5000/chapter/1', {
      method: 'POST', // Specify the request method
      headers: {
          'Content-Type': 'application/json' // Specify the content type
      },
      body: JSON.stringify({"query": prompt}) // Convert the data to a JSON string
    })
    .then((response) => {
      const reader = response.body.getReader();
      // read() returns a promise that resolves when a value has been received
      reader.read().then(function pump({ done, value }) {
        if (done) {
          // Do something with last chunk of data then exit reader
          return;
        }
        // Otherwise do something here to process current chunk
        const chunkString = new TextDecoder().decode(value);
        // Log the chunk string
        console.log(chunkString);
        setMessage(message => [...message, chunkString])
        // Read some more, and call this function again
        return reader.read().then(pump);
      });
    })
    .catch((err) => console.error(err));
  }
  
  return (
    <Box>
      <Typography variant="h6">Chat with AI</Typography>
      <ChatMessage>{message}</ChatMessage>
      <ChatInputContainer>
        <StyledInputBase
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && getLLMResponse()}
          placeholder="Type a message..."
        />
        <Button variant="outlined" onClick={getLLMResponse}>
        generate
        </Button>
      </ChatInputContainer>
    </Box>
  );
}
*/
export default App;
