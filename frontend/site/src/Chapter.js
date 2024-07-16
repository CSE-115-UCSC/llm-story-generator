import React, { useState } from 'react';
import { Box, Button, Typography } from '@mui/material';
import { splitTextIntoParagraphsAndLines } from './utils';

function Chapters() {
  const [selectedChapter, setSelectedChapter] = useState(null);
  const [expandedChapters, setExpandedChapters] = useState({});

  const chapters = [
    { id: 1, title: 'Chapter 1: RAC1', content: `The paper by Winston Royce was published in August 1970. This paper was published from Proceedings, IEEE WESCON. This article is motivated by Dr. Royce's analysis of the past three decades has been based on the development of software packages for spacecraft mission planning, command and post-flight, so he has a unique perspective on managing large software development projects.` },
    { id: 2, title: 'Chapter 2: Rac11', content: `I think there are six reasons to do extensive documentation in software development. First, documents can visualize the technology, allowing designers, management and customers to communicate clearly and effectively, which reduces a lot of misunderstandings. Secondly, there needs to be a collective design at the beginning of software development, so that there can be a formal discussion. Let the team have a clear picture to work on. Thirdly, valid documentation allows testers to identify and fix bugs in programs more quickly. Then, there can't be just one person who knows what's going on with the program.` },
    { id: 3, title: 'Chapter 3: test the content', content: `Content of Chapter 3: lalalala 12345678 lalal baba haha xixi cici` },
  ];

  const toggleChapterExpansion = (chapterId) => {
    setExpandedChapters(prev => ({
      ...prev,
      [chapterId]: !prev[chapterId]
    }));
  };

  return (
    <Box>
      {chapters.map(chapter => (
        <Box key={chapter.id} mb={2}>
          <Button variant="outlined" onClick={() => setSelectedChapter(chapter.id)}>
            {chapter.title}
          </Button>
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

export default Chapters;


