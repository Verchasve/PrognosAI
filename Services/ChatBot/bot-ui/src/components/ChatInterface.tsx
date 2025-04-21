import React, { useState, useRef, useEffect } from 'react';
import { Box, Paper, TextField, IconButton, Typography, Button } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import styled from 'styled-components';
import { Message } from '../types/chat';
import axios from 'axios';

const ChatContainer = styled(Paper)`
  height: 600px;
  max-width: 800px;
  margin: 20px auto;
  display: flex;
  flex-direction: column;
  padding: 20px;
`;

const MessagesContainer = styled(Box)`
  flex-grow: 1;
  overflow-y: auto;
  margin-bottom: 20px;
  padding: 10px;
`;

const MessageBubble = styled(Box)<{ isUser: boolean }>`
  background-color: ${props => props.isUser ? '#e3f2fd' : '#f5f5f5'};
  padding: 10px 15px;
  border-radius: 15px;
  margin: 5px 0;
  max-width: 70%;
  align-self: ${props => props.isUser ? 'flex-end' : 'flex-start'};
  word-wrap: break-word;
`;

const InputContainer = styled(Box)`
  display: flex;
  gap: 10px;
  padding: 10px 0;
`;

const ButtonContainer = styled(Box)`
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-top: 8px;
`;

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      text: input,
      isUser: true,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await axios.post('http://localhost:5005/webhooks/rest/webhook', {
        sender: 'user',
        message: input,
      });

      const botResponses = response.data.map((msg: any) => ({
        text: msg.text,
        isUser: false,
        timestamp: new Date(),
        buttons: msg.buttons,
      }));

      setMessages(prev => [...prev, ...botResponses]);

    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [
        ...prev,
        {
          text: 'Sorry, I encountered an error. Please try again.',
          isUser: false,
          timestamp: new Date(),
        },
      ]);
    }

    setIsLoading(false);
  };

  const handleKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  };

  const handleButtonClick = (payload: string) => {
    setInput(payload);
    handleSend();
  };

  const renderButtons = (buttons: any[]) => {
    if (!buttons) return null;

    return (
      <ButtonContainer>
        {buttons.map((button, index) => (
          <Button
            key={index}
            variant="outlined"
            size="small"
            onClick={() => handleButtonClick(button.payload)}
          >
            {button.title}
          </Button>
        ))}
      </ButtonContainer>
    );
  };

  return (
    <ChatContainer elevation={3}>
      <Typography variant="h5" gutterBottom>
        Diagnostic Chatbot
      </Typography>
      <MessagesContainer>
        {messages.map((message, index) => (
          <Box
            key={index}
            sx={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: message.isUser ? 'flex-end' : 'flex-start',
            }}
          >
            <MessageBubble isUser={message.isUser}>
              <Typography>{message.text}</Typography>
            </MessageBubble>
            {renderButtons(message.buttons)}
          </Box>
        ))}
        <div ref={messagesEndRef} />
      </MessagesContainer>
      <InputContainer>
        <TextField
          fullWidth
          variant="outlined"
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={isLoading}
          size="small"
        />
        <IconButton
          color="primary"
          onClick={handleSend}
          disabled={isLoading || !input.trim()}
        >
          <SendIcon />
        </IconButton>
      </InputContainer>
    </ChatContainer>
  );
};

export default ChatInterface; 