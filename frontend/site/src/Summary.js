import React, { useState } from 'react';
import { Box, Button, Typography, IconButton, Grid } from '@mui/material';
import CheckIcon from '@mui/icons-material/Check';
import CloseIcon from '@mui/icons-material/Close';
import { splitTextIntoParagraphsAndLines } from './utils';

function Summaries() {
  const [selectedSummary, setSelectedSummary] = useState(null);

  const summaries = [
    { id: 1, title: 'Chapter 1: s', content: 'Summary of Chapter 1: meow' },
    { id: 2, title: 'Chapter 2: s', content: 'Summary of Chapter 2: meow meow' },
    { id: 3, title: 'Chapter 3: s', content: 'Summary of Chapter 3: meow meow meow' },
  ];

  const handleCorrect = (id) => {
    console.log(`Summary ${id} marked as correct`);
    // Send message to AI
    // SendMessageToAI(id, 'correct');
  };

  const handleIncorrect = (id) => {
    console.log(`Summary ${id} marked as incorrect`);
    // Send message to AI
    // SendMessageToAI(id, 'incorrect');
  };

  return (
    <Box>
      {summaries.map(summary => (
        <Box key={summary.id} mb={2}>
          <Button variant="outlined" onClick={() => setSelectedSummary(summary.id)}>
            {summary.title}
          </Button>
          {selectedSummary === summary.id && (
            <Box>
              {splitTextIntoParagraphsAndLines(summary.content, 10).map((paragraph, pIndex) => (
                <Box key={pIndex} mb={2}>
                  {paragraph.map((line, lIndex) => (
                    <Typography key={lIndex}>{line}</Typography>
                  ))}
                </Box>
              ))}
              <Grid container spacing={1}>
                <Grid item>
                  <IconButton color="primary" sx={{ p: 0.5 }} onClick={() => handleCorrect(summary.id)}>
                    <CheckIcon />
                  </IconButton>
                </Grid>
                <Grid item>
                  <IconButton color="secondary" sx={{ p: 0.5 }} onClick={() => handleIncorrect(summary.id)}>
                    <CloseIcon />
                  </IconButton>
                </Grid>
              </Grid>
            </Box>
          )}
        </Box>
      ))}
    </Box>
  );
}

export default Summaries;



