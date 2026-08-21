const express = require('express');
const router = express.Router();

// Mock data for initial state
let memoryContext = [
  { id: 1, type: 'system', content: 'Agent initialized. Awaiting tasks.' }
];

// Helper to delay response for simulation
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// Endpoint to handle chat messages
router.post('/chat', async (req, res) => {
  const { message } = req.body;
  
  if (!message) {
    return res.status(400).json({ error: 'Message is required' });
  }

  // Add user message to memory (simplified)
  memoryContext.push({ id: Date.now(), type: 'user', content: message });

  // Simulate agent thinking and planning
  const agentResponse = {
    message: `I have received your request: "${message}". I will start processing this immediately.`,
    plan: [
      { id: 'p1', step: 'Analyze the request', status: 'completed' },
      { id: 'p2', step: 'Search knowledge base', status: 'in-progress' },
      { id: 'p3', step: 'Formulate final response', status: 'pending' }
    ],
    toolUsage: {
      tool: 'knowledge_search',
      status: 'running',
      details: 'Querying internal database for relevant information...'
    }
  };

  // Simulate processing time
  await delay(1500);

  res.json(agentResponse);
});

// Endpoint to fetch current memory/context
router.get('/memory', (req, res) => {
  res.json({ context: memoryContext });
});

// Endpoint to simulate the completion of background tasks
router.get('/status/update', async (req, res) => {
    // In a real app, this might use SSE or WebSockets to push updates.
    // Here we just provide an endpoint to fetch simulated progress.
    await delay(1000);
    res.json({
        plan: [
            { id: 'p1', step: 'Analyze the request', status: 'completed' },
            { id: 'p2', step: 'Search knowledge base', status: 'completed' },
            { id: 'p3', step: 'Formulate final response', status: 'completed' }
        ],
        toolUsage: {
            tool: 'none',
            status: 'idle',
            details: 'All tasks completed successfully.'
        },
        finalResult: "Based on my analysis, I have completed the requested task."
    });
});


module.exports = router;
