// src/App.js
import React from 'react';
import Chat from './Chat';
import { Container, styled } from '@mui/material';

const AppContainer = styled(Container)({
  display: 'flex',
  height: '100vh',
  alignItems: 'center',
  justifyContent: 'center',
});

function App() {
  return (
    <AppContainer>
      <Chat />
    </AppContainer>
  );
}

export default App;


