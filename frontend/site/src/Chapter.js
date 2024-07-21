import React, { useState, useEffect } from 'react';
import { Box, Button, Typography } from '@mui/material';
import { splitTextIntoParagraphsAndLines } from './utils';

function Chapters() {
  //const [selectedChapter, setSelectedChapter] = useState(null);
  //const [expandedChapters, setExpandedChapters] = useState({});
  const [chapters, setChapters] = useState([]);

  console.log("TEST");
  UpdateChapterList(1);

  //add chapter to list
  //chapters.push({ id: 4, title: 'Chapter 4: test', content: `Content of Chapter 4: lalalala 12345678 lalal baba haha xixi cici` })

  //const addChapter = (newchapter) => { setChapters((prevChapters) => [...prevChapters, newchapter]); }
  useEffect (() => {fetch('http://127.0.0.1:5000/chapters', {
    method: 'GET' // Specify the request method
    })
    .then(response => response.json())
    .then(data=>{ 
      console.log('GET Response:', data)
      setChapters(data)
    })
  }, []);

  return (
    <Box>
      {chapters.map((text, index) => ( <Chapter number={index+1} text={text} key={index}/> ))}
    </Box>
  );
}

export default Chapters;

// call api and turn it into a dictionary that can then be added to the list
// 
// { id: #, title: 'Chapter #: name', content: `Content of Chapter #: ` }
function UpdateChapterList(chapter){
  //get chapter contents from api call

  fetch('http://127.0.0.1:5000/chapter/'+chapter, {
    method: 'GET' // Specify the request method
    })
    .then(response => response.json())
    .then(data=>{console.log('GET Response:', data)})
  

/*
  var ChapterContent='';
  const CapterNumber = chapter+1;

  const ChapterToAdd =  { id: CapterNumber, title: 'Chapter '+CapterNumber+':', content: "Content of Chapter "+ CapterNumber+":"+ChapterContent};

  return ChapterToAdd
  */
};

// props: string(chapter text), int(chapter number)
function Chapter(props) {
  const [selectedChapter, setSelectedChapter] = useState(null);
  const [expandedChapters, setExpandedChapters] = useState({});

  const toggleChapterExpansion = (chapterId) => {
    setExpandedChapters(prev => ({
      ...prev,
      [chapterId]: !prev[chapterId]
    }));
  };

  return (
    
    <Box key={props.number} mb={2}>
    <Button variant="outlined" onClick={() => setSelectedChapter(props.number)}>
      Chapter: {props.number}
    </Button>
    {selectedChapter === props.number && (
      <Box>
        {expandedChapters[props.number] ? (
          <>
            {splitTextIntoParagraphsAndLines(props.text, 10).map((paragraph, pIndex) => (
              <Box key={pIndex} mb={2}>
                {paragraph.map((line, lIndex) => (
                  <Typography key={lIndex}>{line}</Typography>
                ))}
              </Box>
            ))}
            <Button onClick={() => toggleChapterExpansion(props.number)}>
              Collapse
            </Button>
          </>
        ) : (
          <>
            {splitTextIntoParagraphsAndLines(props.text, 10).map((paragraph, pIndex) => (
              <Box key={pIndex} mb={2}>
                {paragraph.slice(0, 2).map((line, lIndex) => (
                  <Typography key={lIndex}>{line}</Typography>
                ))}
              </Box>
            ))}
            <Button onClick={() => toggleChapterExpansion(props.number)}>
              Load more
            </Button>
          </>
        )}
      </Box>
    )}
  </Box>

  );

};



