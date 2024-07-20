import React, { useState, useEffect } from 'react';
//import { Box, Button, Typography, IconButton, Grid } from '@mui/material';
import { Box, Typography, IconButton, TextField, Button  } from '@mui/material';
import CheckIcon from '@mui/icons-material/Check';
import CloseIcon from '@mui/icons-material/Close';
//import { splitTextIntoParagraphsAndLines } from './utils';

// Function to fetch characters from the backend
const getCharacters = async () => {
  try {
    const response = await fetch('http://127.0.0.1:5000/character', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching characters:', error);
    return { characteristics: {} };
  }
};

// Function to update character traits in the backend
const updateCharacter = async (character, traits) => {
  try {
    const response = await fetch('http://127.0.0.1:5000/character', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ character, traits })
    });
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return await response.json();
  } catch (error) {
    console.error('Error updating character:', error);
  }
};

// Can you see making a comment. YES
// cd frontend/site && npm start
function Characters() {
  const [selectedCharacter, setSelectedCharacter] = useState(null);
  const [newTrait, setNewTrait] = useState("");
  const [characters, setCharacters] = useState({}); // hold a list of characters (append characters to it), 'character name': ['trait1', 'trait2', ...] 
  const [editableTraits, setEditableTraits] = useState({});
  // const characters = [
  //   { id: 1, name: 'Character 1', details: 'Details of Character 1: meow' },
  //   { id: 2, name: 'Character 2', details: 'Details of Character 2: meow meow' },
  //   { id: 3, name: 'Character 3', details: 'Details of Character 3: meow meow meow' },
  // ];
  useEffect(() => {
    fetchCharacters();
  }, []);

  const fetchCharacters = async () => {
    try {
      const response = await getCharacters();
      setCharacters(response.data.characteristics);
    } catch (error) {
      console.error('Error fetching characters:', error);
    }
  };
  
  const handleCorrectTrait = (character, traitIndex) => {
    setCharacters(prevState => {
      const newTraits = prevState[character].split(', ');
      if (!editableTraits[character]) {
        setEditableTraits(prevState => ({
          ...prevState,
          [character]: [...newTraits]
        }));
      }
      newTraits[traitIndex] = "Correct";
      updateCharacter(character, newTraits.join(', '));
      return {
        ...prevState,
        [character]: newTraits.join(', ')
      };
    });
  };

  const handleIncorrectTrait = (character, traitIndex) => {
    setCharacters(prevState => {
      const newTraits = prevState[character].split(', ');
      if (!editableTraits[character]) {
        setEditableTraits(prevState => ({
          ...prevState,
          [character]: [...newTraits]
        }));
      }
      newTraits[traitIndex] = "Incorrect";
      updateCharacter(character, newTraits.join(', '));
      return {
        ...prevState,
        [character]: newTraits.join(', ')
      };
    });
  };
  const handleAddTrait = () => {
    if (newTrait && selectedCharacter) {
      setCharacters(prevState => {
        const newTraits = prevState[selectedCharacter].split(', ');
        newTraits.push(newTrait);
        updateCharacter(selectedCharacter, newTraits.join(', '));
        setNewTrait("");
        return {
          ...prevState,
          [selectedCharacter]: newTraits.join(', ')
        };
      });
    }
  };

  if (Object.keys(characters).length === 0) {
    return <Typography>No characters found</Typography>;
  }

  return (
    <Box>
      <Box>
        {Object.keys(characters).map(character => (
          <Button
            key={character}
            onClick={() => setSelectedCharacter(character)}
            variant={selectedCharacter === character ? "contained" : "outlined"}
            sx={{ margin: '5px' }}
          >
            {character}
          </Button>
        ))}
      </Box>
      {selectedCharacter && (
        <Box mt={2}>
          <Typography variant="h6">{selectedCharacter}</Typography>
          {characters[selectedCharacter].split(', ').map((trait, index) => (
            <Box key={index} display="flex" alignItems="center" mb={1}>
              <Typography>{trait}</Typography>
              <IconButton color="primary" sx={{ p: 0.5 }} onClick={() => handleCorrectTrait(selectedCharacter, index)}>
                <CheckIcon />
              </IconButton>
              <IconButton color="secondary" sx={{ p: 0.5 }} onClick={() => handleIncorrectTrait(selectedCharacter, index)}>
                <CloseIcon />
              </IconButton>
            </Box>
          ))}
          <TextField
            label="Add Trait"
            value={newTrait}
            onChange={(e) => setNewTrait(e.target.value)}
            variant="outlined"
            size="small"
            sx={{ marginTop: '10px' }}
          />
          <Button onClick={handleAddTrait} variant="contained" sx={{ marginTop: '10px' }}>
            Add Trait
          </Button>
        </Box>
      )}
    </Box>
  );
}

export default Characters;
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
//function Character(props) {
  
// const callAPI = () => {
//    console.log("Hi I'm a button.")
  //}

//  useEffect(() => {
 //   fetch('http://127.0.0.1/character')
//      .then(response => {
//        if (!response.ok) {
//          throw new Error('Network response was not ok');
//        }
//        return response.json();
//      })
//      .then(data => {
//        console.log(data)
//      })
//      .catch(error => {
//        console.log(error)
//      });
//  }, []);

  //return (
   // <Box>
     // <Button onClick={callAPI}>Hello</Button>
     // <p>props.name</p>
     // {props.traits.map(item => (
      //  <p>{item}</p>
      //))}
    //</Box>
  //);
//}

