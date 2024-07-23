import { ThemeProvider } from '@mui/material/styles';
import React from 'react';
import { Container, Box, CssBaseline, Paper, styled } from '@mui/material';
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

export default App;
