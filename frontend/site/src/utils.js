export function splitTextIntoParagraphsAndLines(text, wordsPerLine) {
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

