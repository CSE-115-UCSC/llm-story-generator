// src/Chat.js
import React, { useState, useEffect, useRef } from 'react';
import { Box, InputBase, IconButton, Typography, Paper, styled } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import PersonIcon from '@mui/icons-material/Person';

const ChatContainer = styled(Paper)({
  width: '50%',
  backgroundColor: '#ffffff',
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'space-between',
  boxSizing: 'border-box',
  height: '100%',
});

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

const ChatMessage = styled(Box)(({ user }) => ({
  display: 'flex',
  alignItems: 'center',
  marginLeft: '8px',
  padding: '10px',
  borderRadius: '5px',
  backgroundColor: user ? '#007BFF' : '#f0f0f0',
  color: user ? '#ffffff' : '#000000',
  maxWidth: '80%',
}));

const ChatInputContainer = styled(Box)({
  display: 'flex',
  alignItems: 'center',
  padding: '10px',
  borderTop: '1px solid #ccc',
  backgroundColor: '#fff',
});

const StyledInputBase = styled(InputBase)({
  flexGrow: 1,
  padding: '10px',
  borderRadius: '20px',
  backgroundColor: '#f0f0f0',
  marginRight: '10px',
});

function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);

  const handleSend = () => {
    if (input.trim()) {
      setMessages([...messages, { text: input, user: true }]);
      setInput('');
      simulateBotResponse('I am a robot. I do not know your word.');
    }
  };

  const simulateBotResponse = (text) => {
    setTimeout(() => {
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: '', user: false, typing: true },
      ]);
      let index = -1;
      const interval = setInterval(() => {
        if (index < text.length - 1) {
          setMessages((prevMessages) => {
            const newMessages = [...prevMessages];
            newMessages[newMessages.length - 1] = {
              ...newMessages[newMessages.length - 1],
              text: newMessages[newMessages.length - 1].text + text[index],
            };
            return newMessages;
          });
          index++;
        } else {
          clearInterval(interval);
        }
      }, 100); // Speed up the typing effect
    }, 500);
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
            {message.user ? <PersonIcon /> : <SmartToyIcon />}
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
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Type a message..."
        />
        <IconButton color="primary" onClick={handleSend}>
          <SendIcon />
        </IconButton>
      </ChatInputContainer>
    </ChatContainer>
  );
}

export default Chat;


