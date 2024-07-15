// src/Chat.js
import React, { useState, useEffect, useRef } from 'react';
import { Box, InputBase, IconButton, Typography, Paper, styled, useTheme } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import PersonIcon from '@mui/icons-material/Person';

const ChatContainer = styled(Paper)(({ theme }) => ({
  width: '100%', // 占用整个父容器的宽度
  height: '100%', // 占用整个父容器的高度
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
  marginLeft: '8px',
  padding: '10px',
  borderRadius: '5px',
  backgroundColor: user ? theme.palette.custom.messageBubble.user.background : theme.palette.custom.messageBubble.bot.background,
  color: user ? theme.palette.custom.messageBubble.user.text : theme.palette.custom.messageBubble.bot.text,
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

function Chat() {
  const theme = useTheme(); // 使用 useTheme 钩子获取主题

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
      }, 25); // Speed up the typing effect
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
            {message.user ? <PersonIcon style={{ color: theme.palette.custom.icons.user }} /> : <SmartToyIcon style={{ color: theme.palette.custom.icons.bot }} />}
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
