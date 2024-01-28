import cors from "cors";
import express from "express";
import fetch from "node-fetch";

const app = express();
const PORT = 3000;

app.use(
  cors({
    origin: "http://dujetim.test",
  })
);
app.use(express.json());
// Define API endpoints
const apiEndpoints = [
  "/express/read-orders",
  "/express/read-products",
  "/express/read-users",
  "/express/read-order-items",
];

// Define Flask API URL
const flaskApiUrl = "http://flaskapp_master:5000/api";

// Create Express route handlers for each API endpoint
apiEndpoints.forEach((endpoint) => {
  app.get(endpoint, async (req, res) => {
    let parsedEndpoint = endpoint.replace("/express", "");
    try {
      console.log(`Received request for ${endpoint}`);
      const flaskApiResponse = await fetch(`${flaskApiUrl}${parsedEndpoint}`);
      const data = await flaskApiResponse.json();
      console.log(
        `Response from Flask API for ${parsedEndpoint}: ${JSON.stringify(data)}`
      );
      res.json(data);
    } catch (error) {
      console.error(
        `Error fetching data from Flask API for ${parsedEndpoint}: ${error.message}`
      );
      res.status(500).json({ error: "Internal Server Error" });
    }
  });
});

app.get("/express/", (req, res) => {
  res.send("Hello World!");
});

// Express route handler for user login
app.post("/express/login", async (req, res) => {
  const { email, password } = req.body;

  if (email && password) {
    try {
      console.log(`Received login request for user: ${email}`);
      const flaskApiResponse = await fetch(`${flaskApiUrl}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const data = await flaskApiResponse.json();
      console.log(`Response from Flask API for login: ${JSON.stringify(data)}`);
      res.json(data);
    } catch (error) {
      console.error(`Error during login: ${error.message}`);
      res
        .status(500)
        .json({ status: "error", message: "Internal Server Error" });
    }
  } else {
    res.status(400).json({ status: "error", message: "Invalid request" });
  }
});

// Express route handler for user register
app.post("/express/register", async (req, res) => {
  const { name, email, password } = req.body;

  if (name && email && password) {
    try {
      console.log(`Received registration request for user: ${email}`);
      const flaskApiResponse = await fetch(`${flaskApiUrl}/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password }),
      });

      const data = await flaskApiResponse.json();
      console.log(
        `Response from Flask API for registration: ${JSON.stringify(data)}`
      );

      // Check the response status and send an appropriate response to the client
      if (data.status === "success") {
        res
          .status(200)
          .json({
            status: "success",
            message: "User registered successfully",
            user: data.user,
          });
      } else {
        res
          .status(400)
          .json({ status: "error", message: "User registration failed" });
      }
    } catch (error) {
      console.error(`Error during registration: ${error.message}`);
      res
        .status(500)
        .json({ status: "error", message: "Internal Server Error" });
    }
  } else {
    res.status(400).json({ status: "error", message: "Invalid request" });
  }
});

// Express route handler for creating a new order
app.post("/express/create-order", async (req, res) => {
  const { user_id, products } = req.body;
  console.log(req.body);
  if (user_id && products) {
    try {
      console.log(`Received create order request for user: ${user_id}`);
      const flaskApiResponse = await fetch(`${flaskApiUrl}/create-order`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id, products }),
      });

      const data = await flaskApiResponse.json();
      console.log(
        `Response from Flask API for create order: ${JSON.stringify(data)}`
      );

      // Check the response status and send an appropriate response to the client
      if (data.status === "success") {
        res
          .status(200)
          .json({ status: "success", message: "Order created successfully" });
      } else {
        res
          .status(400)
          .json({ status: "error", message: "Order creation failed" });
      }
    } catch (error) {
      console.error(`Error during create order: ${error.message}`);
      res
        .status(500)
        .json({ status: "error", message: "Internal Server Error" });
    }
  } else {
    res.status(400).json({ status: "error", message: "Invalid request" });
  }
});

// Start the Express server
app.listen(PORT, () => {
  console.log(`Express server is running on http://localhost:${PORT}`);
});
