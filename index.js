
const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const { spawn } = require('child_process'); 


const app = express();
const PORT = process.env.PORT || 3000;


app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));


app.get('/', (req, res) => {
  res.send('Welcome to the AQI Prediction API for Anand Vihar, Delhi!');
});


app.post('/predict', (req, res) => {
 
  const inputFeatures = req.body.features; 

  if (!inputFeatures) {
    return res.status(400).send({ error: 'Features are required for prediction' });
  }

  
  const pythonProcess = spawn('python3', ['predict_aqi.py', JSON.stringify(inputFeatures)]);

  let result = '';
  let error = '';

  pythonProcess.stdout.on('data', (data) => {
    result += data.toString();
  });

  pythonProcess.stderr.on('data', (data) => {
    error += data.toString();
  });

  pythonProcess.on('close', (code) => {
    if (code === 0) {
      
      try {
        const prediction = JSON.parse(result);
        res.status(200).send({ prediction });
      } catch (e) {
        res.status(500).send({ error: 'Error parsing prediction result' });
      }
    } else {
      
      res.status(500).send({ error: error || 'Failed to generate prediction' });
    }
  });
});


app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
