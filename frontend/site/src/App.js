//import { ThemeProvider, createTheme } from '@mui/material/styles';
/*const theme = createTheme({
  components: {
    MuiStack: {
      defaultProps: {
        useFlexGap: true,
      },
    },
  },
});*/

import React, { useState } from 'react';
import { Container, Box, Button, ButtonGroup, Typography } from '@mui/material';
//import Paper from '@mui/material/Paper';
//import InputBase from '@mui/material/InputBase';
//import IconButton from '@mui/material/IconButton';
//import Stack from '@mui/material/Stack';
//import Box from '@mui/material/Box';

// Utility function to split text into lines with a specified number of words per line
function splitTextIntoParagraphsAndLines(text, wordsPerLine) {
  const paragraphs = text.split('\n');
  const processedParagraphs = paragraphs.map(paragraph => {
    const words = paragraph.split(' ');
    const lines = [];
    for (let i = 0; i < words.length; i += wordsPerLine) {
      lines.push(words.slice(i, i + wordsPerLine).join(' '));
    }
    return lines;
  });
  return processedParagraphs;
}

// Main App component
function App() {
  // State to manage the current view (chapters, summaries, characters)
  const [view, setView] = useState('chapters');

  return (
    <Container>
      <Box display="flex">
        {/* Left sidebar for chat functionality */}
        <Box width="25%" p={2}>
          <Chat />
        </Box>
        {/* Right content area for chapters, summaries, and characters */}
        <Box width="75%" p={2}>
          {/* Navigation buttons to switch between views */}
          <ButtonGroup variant="contained">
            <Button onClick={() => setView('chapters')}>Chapters</Button>
            <Button onClick={() => setView('summaries')}>Summaries</Button>
            <Button onClick={() => setView('characters')}>Characters</Button>
          </ButtonGroup>
          {/* Display the content based on the current view */}
          <Box mt={2} overflow="auto" maxHeight="80vh">
            {view === 'chapters' && <Chapters />}
            {view === 'summaries' && <Summaries />}
            {view === 'characters' && <Characters />}
          </Box>
        </Box>
      </Box>
    </Container>
  );
}

// Chat component for the left sidebar
function Chat() {
  return (
    <Box>
      <Typography variant="h6">Chat with AI</Typography>
    </Box>
  );
}

// Chapters component to display chapter buttons and content
function Chapters() {
  // State to manage the currently selected chapter
  const [selectedChapter, setSelectedChapter] = useState(null);
  const [expandedChapters, setExpandedChapters] = useState({});

  // Array of chapter objects with id, title, and content
  const chapters = [
    { id: 1, title: 'Chapter 1: RAC1', content: `The paper by Winston Royce was published in August 1970.This paper was published from Proceedings, IEEE WESCON.
This article is motivated by Dr. Royce's analysis of the past three decades has been based on the development of software packages for spacecraft mission planning, command and post-flight, so he has a unique perspective on managing large software development projects.` },
    { id: 2, title: 'Chapter 2: Rac11', content: `:”<>?!@#$%^&*()_+I think there are six reasons to do extensive documentation in software development. First, documents can visualize the technology, allowing designers, management and customers to communicate clearly and effectively, which reduces a lot of misunderstandings. Secondly, there needs to be a collective design at the beginning of software development, so that there can be a formal discussion. Let the team have a clear picture to work on. Thirdly, valid documentation allows testers to identify and fix bugs in programs more quickly. Then, there can't be just one person who knows what's going on with the program.` },
    { id: 3, title: 'Chapter 3: test the content', content: `Content of Chapter 3: lalalala
12345678 lalal baba haha xixi cici` },
  ];

  const toggleChapterExpansion = (chapterId) => {
    setExpandedChapters(prev => ({
      ...prev,
      [chapterId]: !prev[chapterId]
    }));
  };

  return (
    <Box>
      {/* Map through chapters array and create buttons for each chapter */}
      {chapters.map(chapter => (
        <Box key={chapter.id} mb={2}>
          <Button variant="outlined" onClick={() => setSelectedChapter(chapter.id)}>
            {chapter.title}
          </Button>
          {/* Display chapter content if it is the currently selected chapter */}
          {selectedChapter === chapter.id && (
            <Box>
              {expandedChapters[chapter.id] ? (
                <>
                  {splitTextIntoParagraphsAndLines(chapter.content, 10).map((paragraph, pIndex) => (
                    <Box key={pIndex} mb={2}>
                      {paragraph.map((line, lIndex) => (
                        <Typography key={lIndex}>{line}</Typography>
                      ))}
                    </Box>
                  ))}
                  <Button onClick={() => toggleChapterExpansion(chapter.id)}>
                    Collapse
                  </Button>
                </>
              ) : (
                <>
                  {splitTextIntoParagraphsAndLines(chapter.content, 10).map((paragraph, pIndex) => (
                    <Box key={pIndex} mb={2}>
                      {paragraph.slice(0, 2).map((line, lIndex) => (
                        <Typography key={lIndex}>{line}</Typography>
                      ))}
                    </Box>
                  ))}
                  <Button onClick={() => toggleChapterExpansion(chapter.id)}>
                    Load more
                  </Button>
                </>
              )}
            </Box>
          )}
        </Box>
      ))}
    </Box>
  );
}

// Summaries component to display summary buttons and content
function Summaries() {
  // State to manage the currently selected summary
  const [selectedSummary, setSelectedSummary] = useState(null);

  // Array of summary objects with id, title, and content
  const summaries = [
    { id: 1, title: 'Chapter 1: s', content: 'Summary of Chapter 1: meow' },
    { id: 2, title: 'Chapter 2: s', content: 'Summary of Chapter 2: meow meow' },
    { id: 3, title: 'Chapter 3: s', content: 'Summary of Chapter 3: meow meow meow' },
  ];

  return (
    <Box>
      {/* Map through summaries array and create buttons for each summary */}
      {summaries.map(summary => (
        <Box key={summary.id} mb={2}>
          <Button variant="outlined" onClick={() => setSelectedSummary(summary.id)}>
            {summary.title}
          </Button>
          {/* Display summary content if it is the currently selected summary */}
          {selectedSummary === summary.id && (
            <Box>
              {splitTextIntoParagraphsAndLines(summary.content, 10).map((paragraph, pIndex) => (
                <Box key={pIndex} mb={2}>
                  {paragraph.map((line, lIndex) => (
                    <Typography key={lIndex}>{line}</Typography>
                  ))}
                </Box>
              ))}
            </Box>
          )}
        </Box>
      ))}
    </Box>
  );
}

// Characters component to display character buttons and details
function Characters() {
  // State to manage the currently selected character
  const [selectedCharacter, setSelectedCharacter] = useState(null);

  // Array of character objects with id, name, and details
  const characters = [
    { id: 1, name: 'Character 1', details: 'Details of Character 1: meow' },
    { id: 2, name: 'Character 2', details: 'Details of Character 2: meow meow' },
    { id: 3, name: 'Character 3', details: 'Details of Character 3: meow meow meow' },
  ];

  return (
    <Box>
      {/* Map through characters array and create buttons for each character */}
      {characters.map(character => (
        <Box key={character.id} mb={2}>
          <Button variant="outlined" onClick={() => setSelectedCharacter(character.id)}>
            {character.name}
          </Button>
          {/* Display character details if it is the currently selected character */}
          {selectedCharacter === character.id && (
            <Box>
              {splitTextIntoParagraphsAndLines(character.details, 10).map((paragraph, pIndex) => (
                <Box key={pIndex} mb={2}>
                  {paragraph.map((line, lIndex) => (
                    <Typography key={lIndex}>{line}</Typography>
                  ))}
                </Box>
              ))}
            </Box>
          )}
        </Box>
      ))}
    </Box>
  );
}

export default App;







