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
  
  // const characters = [
  //   { id: 1, name: 'Character 1', details: 'Details of Character 1: meow' },
  //   { id: 2, name: 'Character 2', details: 'Details of Character 2: meow meow' },
  //   { id: 3, name: 'Character 3', details: 'Details of Character 3: meow meow meow' },
  // ];

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
      <Character name="Bob" traits={["white af", "smart", "goofy"]}/>
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
  
  const callAPI = () => {
    console.log("Hi I'm a button.")
  }

  useEffect(() => {
    fetch('http://127.0.0.1/character')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        console.log(data)
      })
      .catch(error => {
        console.log(error)
      });
  }, []);

  return (
    <Box>
      <Button onClick={callAPI}>Hello</Button>
      <p>props.name</p>
      {props.traits.map(item => (
        <p>{item}</p>
      ))}
    </Box>
  );
}

export default Characters;