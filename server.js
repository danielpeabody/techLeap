const csv = require('csv-parser');
const fs = require('fs');
const express = require('express')
const app     = express();
const port    = 3000;
const path = require('path');
const { spawn } = require('child_process');

app.use(express.static('public-html'));

app.listen(port, () => 
  console.log(`App listening at http://localhost:${port}`))

let results = [];

fs.createReadStream('job_postings.csv')
  .pipe(csv({}))
  .on('data',(data) => results.push(data))
  .on('end', ()=>{
    console.log('CSV file read successfully');
});

// Run the script once a day
setInterval(() => {
  const pyProg = spawn('python', ['script.py']);

  pyProg.stdout.on('data', function(data) {
      console.log(data.toString());
  });
  pyProg.stderr.on('data', (data) => {
      console.error(`stderr: ${data}`);
  });
  
  // Write the updated data back to the CSV file
  const stream = fs.createWriteStream("job_postings.csv");
  stream.once('open', () => {
    results.forEach((row) => {
      stream.write(`${row.title},${row.company},${row.location},${row.summary}\n`);
    });
    stream.end();
    console.log('Data written to CSV file successfully');
  });
}, 24 * 60 * 60 * 1000); // Run once a day

app.get('/jobs',(req,res) => {
    res.send(results)
})
