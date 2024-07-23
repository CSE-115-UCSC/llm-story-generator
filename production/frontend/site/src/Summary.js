import React, { useState, forwardRef, useImperativeHandle, useEffect } from 'react';
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

  useEffect (() => {fetch('http://127.0.0.1:5000/summaries', {
    method: 'GET' // Specify the request method
    })
    .then(response => response.json())
    .then(data=>{ 
      console.log('GET Response:', data)
      setSummaries(data)
    })
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <Box sx={{ padding: 2 }}>
        {Object.entries(summaries).map(([key, value]) => (
          <Summary key={key} chapterNumber={key} summaryText={value} />
        ))}
      </Box>
    </ThemeProvider>
  );
});

function Summary(props) {
  const [facts, setFacts] = useState([]);
  const [indices, setIndices] = useState([]);

  const updatedSummary = () => {
    return indices
      .filter(index => index >= 0 && index < facts.length)
      .map(index => facts[index])
      .join(' '); 
  };

  const handleCorrect = (id) => {
    console.log(`Summary ${id} is correct`);
  };

  const handleIncorrect = (id) => {
    console.log(`Summary ${id} is incorrect`);
  };
  
  const toFacts = (summary) => { 
    return summary.split(/(?<=[.!?])\s+/); 
  };
  
  useEffect (() => {
    setFacts(toFacts(props.summaryText))
  }, []); 
  
  
  return(
    <Box key={props.chapterNumber} sx={{ marginBottom: 2 }}>
      <Button variant="outlined">
        Chapter: {props.chapterNumber}
      </Button>
      <Typography variant="body1">
        {props.summaryText}
      </Typography>
      <Button variant="contained" color="primary" onClick={() => handleCorrect(props.chapterNumber)} sx={{ marginRight: 1 }}>
        Correct
      </Button>
      <Button variant="contained" color="secondary" onClick={() => handleIncorrect(props.chapterNumber)}>
        Incorrect
      </Button>
    </Box>
  );
}

export default Summaries;



