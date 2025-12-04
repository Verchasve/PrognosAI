// ...existing code...
import express from 'express';
import axios from 'axios';

const router = express.Router();

const RASA_URL = process.env.RASA_URL || 'http://localhost:5005/webhooks/rest/webhook';
const OLLAMA_URL = process.env.OLLAMA_URL || 'http://localhost:11434/api/generate';
const OLLAMA_MODEL = process.env.OLLAMA_MODEL || 'gemma3:1b';

function isTicketQuery(text: string): boolean {
  if (!text) return false;
  const t = text.toLowerCase();
  const keywords = ['incident', 'incident:', 'incident#', 'jira', 'ticket', 'issue', 'bug', 'story', 'inc', 'request'];
  if (keywords.some(k => t.includes(k))) return true;
  if (/[A-Z]{2,}-\d+/.test(text)) return true;
  return false;
}

router.post('/chat', async (req, res) => {

  const { message } = req.body as { message?: string };
  console.log('Received message:', message);
  if (typeof message !== 'string') {
    return res.status(400).json({ error: 'Invalid payload: message required' });
  }

  try {
    if (isTicketQuery(message)) {
      const rasaResp = await axios.post(RASA_URL, {
        sender: 'user',
        message,
      });
      const messages = (rasaResp.data || []).map((m: any) => ({
        text: m.text || '',
        buttons: m.buttons || null,
      }));
      return res.json({ source: 'rasa', messages });
    } else {
      const ollamaBody = { model: OLLAMA_MODEL, prompt: message , num_predict: 30,
      stream: false};
      const ollamaResp = await axios.post(OLLAMA_URL, ollamaBody, {
        headers: { 'Content-Type': 'application/json' },
        timeout: 60000,
      });
      const ollText = (ollamaResp.data?.text || ollamaResp.data?.response || JSON.stringify(ollamaResp.data)) as string;
      const messages = [{ text: String(ollText), buttons: null }];
      return res.json({ source: 'ollama', messages });
    }
  } catch (err: any) {
    console.error('Routing error:', err?.message || err);
    return res.status(500).json({ error: 'Upstream error', details: err?.message });
  }
});

export default router;