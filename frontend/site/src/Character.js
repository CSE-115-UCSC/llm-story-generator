import React, { useState, useEffect } from 'react';
import { Box, Button, Typography, IconButton, Grid } from '@mui/material';
import CheckIcon from '@mui/icons-material/Check';
import CloseIcon from '@mui/icons-material/Close';
import { splitTextIntoParagraphsAndLines } from './utils';

// Can you see making a comment. YES
// cd frontend/site && npm start
function Characters() {
  const [selectedCharacter, setSelectedCharacter] = useState(null);
  const [characters, setCharacters] = useState([]); // hold a list of characters (append characters to it), 'character name': ['trait1', 'trait2', ...] 
  
  useEffect(() => {
    fetch('http://127.0.0.1/characters',{ method: 'GET'})
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        console.log(data)
        setCharacters(data)
      })
      .catch(error => {
        console.log(error)
      });
  }, []);
  
  const handleCorrect = (id) => {
    console.log(`Character ${id} marked as correct`);
    // Send message to AI
    // SendMessageToAI(id, 'correct');
  };

  const handleIncorrect = (id) => {
    console.log(`Character ${id} marked as incorrect`);
    // Send message to AI
    // SendMessageToAI(id, 'incorrect');
  };

  return (
    <Box>
      {characters.map(name => (
        <Character name={name}/>
      ))}
    </Box>
  );
}

// {characters.map(character => (
//   <Box key={character.id} mb={2}>
//     <Button variant="outlined" onClick={() => setSelectedCharacter(character.id)}>
//       {character.name}
//     </Button>
//     {selectedCharacter === character.id && (
//       <Box>
//         {splitTextIntoParagraphsAndLines(character.details, 10).map((paragraph, pIndex) => (
//           <Box key={pIndex} mb={2}>
//             {paragraph.map((line, lIndex) => (
//               <Typography key={lIndex}>{line}</Typography>
//             ))}
//           </Box>
//         ))}
//         <Grid container spacing={1}>
//           <Grid item>
//             <IconButton color="primary" sx={{ p: 0.5 }} onClick={() => handleCorrect(character.id)}>
//               <CheckIcon />
//             </IconButton>
//           </Grid>
//           <Grid item>
//             <IconButton color="secondary" sx={{ p: 0.5 }} onClick={() => handleIncorrect(character.id)}>
//               <CloseIcon />
//             </IconButton>
//           </Grid>
//         </Grid>
//       </Box>
//     )}
//   </Box>
// ))}


// might need to split character up a lil bit
function Character(props) {
  const [chapters, setChapter] = useState([]);
  const callAPI = () => {
    console.log("Hi I'm a button.")
  }

  useEffect(() => {
    fetch(`http://127.0.0.1/characters/${props.name}`,{ method: 'GET'})
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        console.log(data)
        setChapter(data)
      })
      .catch(error => {
        console.log(error)
      });
  }, []);

  return (
    <Box>
      {Object.entries(chapters).map((number, value) => (
        <Chapter number={number}/>
      ))}
    </Box>
  );
}

export default Characters;