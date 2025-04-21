import React from 'react';
import { Box, ThemeProvider, createTheme } from '@mui/material';
import CssBaseline from '@mui/material/CssBaseline';
import ChatInterface from './components/ChatInterface';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
    background: {
      default: '#f5f5f5',
    },
  },
});

const App = () => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ padding: '20px' }}>
        <ChatInterface />
      </Box>
    </ThemeProvider>
  );
};

export default App; 