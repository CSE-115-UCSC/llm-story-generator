import React, { useState, useEffect } from 'react';
import { Box, Typography } from '@mui/material';

function Characters() {
  const [characters, setCharacters] = useState({}); // hold a list of characters (append characters to it), 'character name': ['trait1', 'trait2', ...] 
  
  useEffect(() => {
    getCharacters();
  }, []);

  const getCharacters = () => {
    fetch('http://127.0.0.1:5000/characters', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })
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
    .catch (error => {
      console.error('Error fetching characters:', error);
    });
  };

  if (Object.keys(characters).length === 0) {
    return <Typography>No characters found</Typography>;
  }

  return (
    <Box> 
      {Object.keys(characters).map(name => (
        <Character name={name}/>
      ))} 
    </Box>
   );
}

function Character(props) {
  const [chapters, setChapter] = useState([]);

  useEffect(() => {
    fetch(`http://127.0.0.1:5000/characters/${props.name}`,{ method: 'GET'})
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
      {props.name}
      {Object.entries(chapters).map(([number, traits]) => (
        <Chapter number={number} traits={traits}/>
      ))}
    </Box>
  );
}

function Chapter({number, traits}){

  return ( 
  <Box>
    {number}
    <ul>
      {traits.map((trait) => ( <li>{trait}</li>))}
    </ul>
  </Box>
)}

export default Characters;
