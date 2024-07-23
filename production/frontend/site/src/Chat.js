import React, { useState, useEffect, useRef } from 'react';
import { Box, InputBase, IconButton, Typography, Paper, styled, useTheme } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import PersonIcon from '@mui/icons-material/Person';

const ChatContainer = styled(Paper)(({ theme }) => ({
  width: '100%',
  height: '100%',
  backgroundColor: theme.palette.background.default,
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'space-between',
  boxSizing: 'border-box',
}));

const ChatMessages = styled(Box)({
  flexGrow: 1,
  padding: '10px',
  overflowY: 'auto',
});

const ChatMessageContainer = styled(Box)({
  display: 'flex',
  alignItems: 'flex-start',
  margin: '10px 0',
});

const ChatMessage = styled(Box)(({ user, theme }) => ({
  display: 'flex',
  alignItems: 'center',
  marginLeft: '15px',
  padding: '10px',
  borderRadius: '5px',
  backgroundColor: user == 'true' ? theme.palette.custom.messageBubble.user.background : theme.palette.custom.messageBubble.bot.background,
  color: user == 'true' ? theme.palette.custom.messageBubble.user.text : theme.palette.custom.messageBubble.bot.text,
  maxWidth: '80%',
}));

const ChatInputContainer = styled(Box)(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  padding: '10px',
  borderTop: `1px solid ${theme.palette.divider}`,
  backgroundColor: theme.palette.background.default,
}));

const StyledInputBase = styled(InputBase)(({ theme }) => ({
  flexGrow: 1,
  padding: '10px',
  borderRadius: '20px',
  backgroundColor: theme.palette.custom.inputField.background,
  marginRight: '10px',
  color: theme.palette.custom.inputField.text,
}));

const StyledPersonIcon = styled(PersonIcon)(({ theme }) => ({
  fontSize: '50px', // Adjust size of the user icon
  color: theme.palette.custom.icons.user,
  alignSelf: 'flex-start', // Adjust vertical position
}));

const StyledSmartToyIcon = styled(SmartToyIcon)(({ theme }) => ({
  fontSize: '50px', // Adjust size of the bot icon
  color: theme.palette.custom.icons.bot,
  alignSelf: 'flex-start', // Adjust vertical position
}));

function Chat() {
  const theme = useTheme();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [chapterNumber, setChapterNumber] = useState(1);
  const messagesEndRef = useRef(null);

  const incrementChapter = () =>{
    setChapterNumber(chapterNumber => chapterNumber + 1)
  }

  const getLLMResponse = () => {
    const prompt = input.trim();
    if (!prompt) return;

    incrementChapter();

    setMessages([...messages, { text: prompt, user: 'true' }]);
    setInput('');
    setMessages((prevMessages) => [
      ...prevMessages,
      { text: '', user: 'false', typing: true },
    ]);

    fetch(`http://127.0.0.1:5000/chapter/${chapterNumber}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ "query": prompt })
    })
    .then((response) => {
      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8'); // Ensure UTF-8 decoding
      let partialResult = '';
  
      reader.read().then(function pump({ done, value }) {
        if (done) {
          
          return;
        }
  
        const chunkString = decoder.decode(value, { stream: true });
        partialResult += chunkString;
        //simulateBotResponse(chunkString);
        // Finalize message if done
        setMessages((prevMessages) => {
          const newMessages = [...prevMessages];
          newMessages[newMessages.length - 1] = {
            ...newMessages[newMessages.length - 1],
            text: partialResult,
            typing: false,
          };
          return newMessages;
        });
        return reader.read().then(pump);
  
  
      });
    })
    .catch((err) => console.error(err));
  };

  const simulateBotResponse = (text) => {
    let index = -1;
    const interval = setInterval(() => {
      if (index < text.length - 1) {
        setMessages((prevMessages) => {
          const newMessages = [...prevMessages];
          newMessages[newMessages.length - 1] = {
            ...newMessages[newMessages.length - 1],
            text: newMessages[newMessages.length - 1].text + text,
          };
          return newMessages;
        });
      } else {
        clearInterval(interval);
      }
    }, 25);
  };

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  return (
    <ChatContainer elevation={3}>
      <ChatMessages>
        {messages.map((message, index) => (
          <ChatMessageContainer key={index}>
            {message.user == 'true' ? 
              <StyledPersonIcon /> :
              <StyledSmartToyIcon />
            }
            <ChatMessage user={message.user}>
              <Typography>{message.text}</Typography>
            </ChatMessage>
          </ChatMessageContainer>
        ))}
        <div ref={messagesEndRef} />
      </ChatMessages>
      <ChatInputContainer>
        <StyledInputBase
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && getLLMResponse()}
          placeholder="Type a message..."
        />
        <IconButton color="primary" onClick={getLLMResponse}>
          <SendIcon />
        </IconButton>
      </ChatInputContainer>
    </ChatContainer>
  );
}

export default Chat;