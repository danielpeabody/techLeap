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

let csvOne = [];

fs.createReadStream('simply_hired_data_v3.csv')
  .pipe(csv({}))
  .on('data',(data) => csvOne.push(data))
  .on('end', ()=>{
    console.log('CSV file read successfully');
});

let csvTwo = [];

fs.createReadStream('remoterocketship.csv')
  .pipe(csv({}))
  .on('data',(data) => csvTwo.push(data))
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

app.get('/jobs/:jobtitle/:company',(req,res) => {
  let retval = []
  if(req.params.jobtitle == "$ALL"){
    req.params.jobtitle = '';
  }
  if(req.params.company == "$ALL"){
    req.params.company = '';
  }
  let keylist = Object.keys(csvOne[0]);
  for(let i = 0; i < csvOne.length; i++){
    if(csvOne[i][keylist[0]].toLowerCase().includes(req.params.jobtitle) & csvOne[i][keylist[1]].toLowerCase().includes(req.params.company)){
      retval.push(csvOne[i])
    }
  }
    res.send(retval)
})

app.get('/jobsTwo/:jobtitle/:company',(req,res) => {
  let retval = []
  if(req.params.jobtitle == "$ALL"){
    req.params.jobtitle = '';
  }
  if(req.params.company == "$ALL"){
    req.params.company = '';
  }
  let keylist = Object.keys(csvTwo[0]);
  for(let i = 0; i < csvTwo.length; i++){
    if(csvTwo[i][keylist[0]].toLowerCase().includes(req.params.jobtitle) & csvOne[i][keylist[1]].toLowerCase().includes(req.params.company)){
      retval.push(csvTwo[i])
    }
  }
    res.send(retval)
})