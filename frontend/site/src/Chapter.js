import React, { useState, useEffect } from 'react';
import { Box, Button, Typography } from '@mui/material';
import { splitTextIntoParagraphsAndLines } from './utils';

function Chapters() {
  //const [selectedChapter, setSelectedChapter] = useState(null);
  //const [expandedChapters, setExpandedChapters] = useState({});
  const [chapters, setChapters] = useState([]);

  //total chapters 
  //var TotalChapter = -1;
  //list of chapters 
  // var chapters = [ 
  //   { id: 1, title: 'Chapter 1: RAC1', content: `The paper by Winston Royce was published in August 1970. This paper was published from Proceedings, IEEE WESCON. This article is motivated by Dr. Royce's analysis of the past three decades has been based on the development of software packages for spacecraft mission planning, command and post-flight, so he has a unique perspective on managing large software development projects.` },
  //   { id: 2, title: 'Chapter 2: Rac11', content: `I think there are six reasons to do extensive documentation in software development. First, documents can visualize the technology, allowing designers, management and customers to communicate clearly and effectively, which reduces a lot of misunderstandings. Secondly, there needs to be a collective design at the beginning of software development, so that there can be a formal discussion. Let the team have a clear picture to work on. Thirdly, valid documentation allows testers to identify and fix bugs in programs more quickly. Then, there can't be just one person who knows what's going on with the program.` },
  //   { id: 3, title: 'Chapter 3: test the content', content: `Content of Chapter 3: lalalala 12345678 lalal baba haha xixi cici` },
  // ];
  //call to api to get chapters

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



