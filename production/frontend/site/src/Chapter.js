import React, { useState, useEffect } from 'react';
import { Box, Button, Typography } from '@mui/material';
import { splitTextIntoParagraphsAndLines } from './utils';

export default function Chapters() {
  const [chapters, setChapters] = useState([]);

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
      {chapters.map((text, index) => ( <Chapter number={index+1} text={text} key={index+1}/> ))}
    </Box>
  );
}

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
