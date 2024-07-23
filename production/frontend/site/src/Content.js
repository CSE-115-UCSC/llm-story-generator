import React, { useState } from 'react';
import { Box, Button, ButtonGroup } from '@mui/material';
import Chapters from './Chapter';
import Summaries from './Summary';
import Characters from './Character';

function Content() {
  const [view, setView] = useState('chapters');
  
  return (
    <Box p={2}>
      <ButtonGroup variant="contained">
        <Button onClick={() => setView('chapters')}>Chapters</Button>
        <Button onClick={() => setView('summaries')}>Summaries</Button>
        <Button onClick={() => setView('characters')}>Characters</Button>
      </ButtonGroup>
      <Box mt={2} overflow="auto" maxHeight="80vh">
        {view === 'chapters' && <Chapters />}
        {view === 'summaries' && <Summaries />}
        {view === 'characters' && <Characters />}
      </Box>
    </Box>
  );
}

export default Content;
