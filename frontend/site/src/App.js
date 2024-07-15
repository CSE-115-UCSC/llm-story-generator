import { ThemeProvider } from '@mui/material/styles';
import React, { useState, useEffect } from 'react';
import { Container, Box, Button, ButtonGroup, Typography, CssBaseline, Paper, styled } from '@mui/material';
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

// Chat component for the left sidebar
//function Chat() {
//  const [message, setMessage] = useState("");
  
//  const getData = () => {
//    fetch('http://127.0.0.1:5000/chapter/1')
//    .then((response) => {
//      const reader = response.body.getReader();
      // read() returns a promise that resolves when a value has been received
//      reader.read().then(function pump({ done, value }) {
//        if (done) {
          // Do something with last chunk of data then exit reader
//          return;
//        }
        // Otherwise do something here to process current chunk
//        const chunkString = new TextDecoder().decode(value);
        // Log the chunk string
 //       console.log(chunkString);
//        setMessage(message => [...message, chunkString])
        // Read some more, and call this function again
//        return reader.read().then(pump);
//      });
//    })
//    .catch((err) => console.error(err));
//  }

  // useEffect(() => {
  //   console.log("creating event...")
  //   const eventSource = new EventSource('http://127.0.0.1:5000/chapter/1', {
  //     withCredentials: true,
  //   });
  //   console.log("Event created.")
  //   eventSource.onmessage = (event) => {
  //     console.log("Got message!")
  //     setMessage(message+event.data);
  //   };

  //   eventSource.onerror = (error) => {
  //     console.error('EventSource failed:', error);
  //     eventSource.close();
  //   };

  //   // Clean up the EventSource when the component unmounts
  //   return () => {
  //     eventSource.close();
  //   };
  // }, []);
  
//  return (
//    <Box>
//      <Typography variant="h6">Chat with AI</Typography>
//      <p>{message}</p>
//      <Button variant="outlined" onClick={getData}>
//        generate
//      </Button>
//    </Box>
//  );
//}

export default App;
