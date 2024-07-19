import React, { useState, forwardRef, useImperativeHandle } from 'react';
import { Box, Button, Typography } from '@mui/material';
import { ThemeProvider } from '@mui/material/styles';
import theme from './theme';

const Summaries = forwardRef((props, ref) => {
  // State to manage the currently selected summary
  const [selectedSummary, setSelectedSummary] = useState(null);
  const [summaries, setSummaries] = useState({});

  // Fetch summaries from the API
  const getSummaries = () => {
    fetch('http://127.0.0.1:5000/summaries')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
      })
      .then(data => {
        console.log('summaries: ', data);
        setSummaries(data);
      })
      .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
      });
  };

  useImperativeHandle(ref, () => ({
    getSummaries
  }));

  // Handle the correctness of a summary
  const handleCorrect = (id) => {
    console.log(`Summary ${id} is correct`);
  };

  // Handle the incorrectness of a summary
  const handleIncorrect = (id) => {
    console.log(`Summary ${id} is incorrect`);
  };

  return (
    <ThemeProvider theme={theme}>
      <Box sx={{ padding: 2 }}>
        {Object.entries(summaries).map(([key, value]) => (
          <Box key={key} sx={{ marginBottom: 2 }}>
            <Typography variant="body1">
              <strong>{key}:</strong> {JSON.stringify(value)}
            </Typography>
            <Button variant="contained" color="primary" onClick={() => handleCorrect(key)} sx={{ marginRight: 1 }}>
              Correct
            </Button>
            <Button variant="contained" color="secondary" onClick={() => handleIncorrect(key)}>
              Incorrect
            </Button>
          </Box>
        ))}
        <Button variant="outlined" onClick={getSummaries}>
          Fetch Summaries
        </Button>
      </Box>
    </ThemeProvider>
  );
});

export default Summaries;



