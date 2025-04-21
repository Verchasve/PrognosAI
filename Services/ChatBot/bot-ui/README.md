# Rasa Chatbot Web Interface

A modern, responsive web interface for interacting with your Rasa chatbot.

## Features

- 💬 Real-time chat interface
- 🎨 Material-UI components
- 📱 Responsive design
- 🔘 Support for button responses
- ⌨️ Keyboard shortcuts
- 🔄 Auto-scroll to latest messages

## Prerequisites

- Node.js (v14 or higher)
- npm (v6 or higher)
- Rasa server running on http://localhost:5005

## Setup

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm start
```

3. Open [http://localhost:3000](http://localhost:3000) to view the chat interface in your browser.

## Usage

1. Make sure your Rasa server is running:
```bash
rasa run --enable-api --cors "*"
rasa run actions
rasa run --enable-api
```

2. Start chatting with the bot through the web interface.

## Available Commands

- `npm start` - Runs the app in development mode
- `npm test` - Launches the test runner
- `npm run build` - Builds the app for production
- `npm run eject` - Ejects from create-react-app

## Environment Variables

Create a `.env` file in the root directory to customize the configuration:

```env
REACT_APP_RASA_API_URL=http://localhost:5005
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 