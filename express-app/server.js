
import cors from 'cors';
import express from 'express';
import fetch from 'node-fetch';

const app = express();
const PORT = 3000;

app.use(cors({
  origin: 'http://dujetim.test',
}));

// Define API endpoints
const apiEndpoints = [
  '/express/read-cart',
  '/express/read-categories',
  '/express/read-orders',
  '/express/read-products',
  '/express/read-users',
];

// Define Flask API URL
const flaskApiUrl = 'http://flaskapp_master:5000/api';  // Replace with the actual Flask app URL

// Create Express route handlers for each API endpoint

apiEndpoints.forEach(endpoint => {
  app.get(endpoint, async (req, res) => {
    let parsedEndpoint = endpoint.replace('/express', '');
    try {
      console.log(`Received request for ${endpoint}`);
      const flaskApiResponse = await fetch(`${flaskApiUrl}${parsedEndpoint}`);
      const data = await flaskApiResponse.json();
      console.log(`Response from Flask API for ${parsedEndpoint}: ${JSON.stringify(data)}`);
      res.json(data);
    } catch (error) {
      console.error(`Error fetching data from Flask API for ${parsedEndpoint}: ${error.message}`);
      res.status(500).json({ error: 'Internal Server Error' });
    }
  });
});

app.get('/express/', (req, res) => {
  res.send('Hello World!')
})

// Start the Express server
app.listen(PORT, () => {
  console.log(`Express server is running on http://localhost:${PORT}`);

  
});