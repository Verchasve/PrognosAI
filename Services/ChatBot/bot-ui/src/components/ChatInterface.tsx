import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  Paper,
  TextField,
  IconButton,
  Typography,
  Button,
  CircularProgress,
  Fade,
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import styled from 'styled-components';
import axios from 'axios';
import { Message } from '../types/chat';

// Glassmorphism container
const ChatContainer = styled(Paper)`
  height: 650px;
  max-width: 850px;
  margin: 40px auto;
  display: flex;
  flex-direction: column;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(14px);
  border: 1px solid rgba(255, 255, 255, 0.25);
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
  overflow: hidden;
  color: #f0f0f0;
`;

const Header = styled(Box)`
  padding: 10px;
  text-align: center;
  background: linear-gradient(135deg, #3a7bd5, #00d2ff);
  color: white;
  font-weight: bold;
  letter-spacing: 0.5px;
`;

const MessagesContainer = styled(Box)`
  flex-grow: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  scroll-behavior: smooth;
  background: radial-gradient(circle at top left, #1f2937, #111827);
`;

const MessageWrapper = styled(Box)<{ isUser: boolean }>`
  display: flex;
  flex-direction: column;
  align-items: ${(props) => (props.isUser ? 'flex-end' : 'flex-start')};
  position: relative;
`;

const MessageBubble = styled(Box)<{ isUser: boolean }>`
  background: ${(props) =>
    props.isUser
      ? 'linear-gradient(135deg, #06beb6 0%, #48b1bf 100%)'
      : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'};
  padding: 12px 16px;
  border-radius: 18px;
  color: #fff;
  font-size: 0.95rem;
  max-width: 75%;
  align-self: ${(props) => (props.isUser ? 'flex-end' : 'flex-start')};
  animation: fadeIn 0.4s ease;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.25);

  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(8px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
`;

const Timestamp = styled(Typography)<{ isUser: boolean }>`
  font-size: 0.7rem !important;
  color: rgba(255, 255, 255, 0.6);
  margin-top: 3px;
  align-self: ${(props) => (props.isUser ? 'flex-end' : 'flex-start')};
`;

const InputContainer = styled(Box)`
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 16px;
  background: rgba(20, 20, 20, 0.85);
  border-top: 1px solid rgba(255, 255, 255, 0.2);
`;

const StyledTextField = styled(TextField)`
  flex-grow: 1;

  & .MuiOutlinedInput-root {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    color: #ffffff;

    & fieldset {
      border: 1px solid rgba(255, 255, 255, 0.2);
    }

    &:hover fieldset {
      border-color: rgba(255, 255, 255, 0.4);
    }

    &.Mui-focused fieldset {
      border-color: #00d2ff;
    }

    input {
      color: #ffffff;
      caret-color: #00d2ff;
    }

    input::placeholder {
      color: rgba(255, 255, 255, 0.6);
    }
  }
`;

const FloatingSendButton = styled(IconButton)`
  background: linear-gradient(135deg, #3a7bd5, #00d2ff);
  color: #fff !important;
  transition: all 0.3s ease;
  &:hover {
    transform: scale(1.1);
    box-shadow: 0 0 12px rgba(0, 210, 255, 0.6);
  }
`;

const ButtonContainer = styled(Box)`
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-top: 6px;
`;

const TypingIndicator = styled(Box)`
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.15);
  width: fit-content;
  align-self: flex-start;

  & div {
    width: 8px;
    height: 8px;
    background-color: #fff;
    border-radius: 50%;
    animation: blink 1.4s infinite both;
  }

  & div:nth-child(2) {
    animation-delay: 0.2s;
  }
  & div:nth-child(3) {
    animation-delay: 0.4s;
  }

  @keyframes blink {
    0%, 80%, 100% {
      opacity: 0.2;
    }
    40% {
      opacity: 1;
    }
  }
`;

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const handleSend = async () => {
    if (!input.trim()) return;
    const userMessage: Message = {
      text: input,
      isUser: true,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    setIsTyping(true);

    try {
      const response = await axios.post('http://localhost:4000/api/chat', {
        sender: 'user',
        message: input,
      });

      const source = response.data.source;
      const messagesData = response.data.messages;
      let botResponses: Message[] = [];

      if (source === 'rasa' || source === 'ollama') {
        botResponses = messagesData.map((msg: any) => ({
          text: msg.text,
          isUser: false,
          timestamp: new Date(),
          buttons: msg.buttons,
        }));
      }

      // Simulate typing delay for realism
      setTimeout(() => {
        setMessages((prev) => [...prev, ...botResponses]);
        setIsTyping(false);
      }, 800);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          text: '⚠️ Oops! Something went wrong. Please try again.',
          isUser: false,
          timestamp: new Date(),
        },
      ]);
      setIsTyping(false);
    } finally {
      setIsLoading(false);
    }
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
            sx={{
              color: '#fff',
              borderColor: 'rgba(255,255,255,0.3)',
              '&:hover': { borderColor: '#00d2ff', background: 'rgba(255,255,255,0.1)' },
            }}
            onClick={() => handleButtonClick(button.payload)}
          >
            {button.title}
          </Button>
        ))}
      </ButtonContainer>
    );
  };

  return (
    <ChatContainer>
      <Header>
        <Typography variant="h6">🤖 Prognos AI Assistant</Typography>
      </Header>

      <MessagesContainer>
        {messages.map((message, index) => (
          <MessageWrapper key={index} isUser={message.isUser}>
            <Fade in timeout={400}>
              <MessageBubble isUser={message.isUser}>
                <Typography>{message.text}</Typography>
              </MessageBubble>
            </Fade>

            <Timestamp isUser={message.isUser}>
              {new Date(message.timestamp).toLocaleTimeString([], {
                hour: '2-digit',
                minute: '2-digit',
              })}
            </Timestamp>

            {renderButtons(message.buttons)}
          </MessageWrapper>
        ))}


        {isTyping && (
          <TypingIndicator>
            <div></div>
            <div></div>
            <div></div>
          </TypingIndicator>
        )}

        <div ref={messagesEndRef} />
      </MessagesContainer>

      <InputContainer>
        <StyledTextField
          fullWidth
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={isLoading}
          size="small"
        />
        <FloatingSendButton
          onClick={handleSend}
          disabled={isLoading || !input.trim()}
          size="large"
        >
          <SendIcon />
        </FloatingSendButton>
      </InputContainer>
    </ChatContainer>
  );
};

export default ChatInterface;
