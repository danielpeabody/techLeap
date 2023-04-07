const csv = require('csv-parser');
const fs = require('fs');
const express = require('express')
const app     = express();
const port    = 3000;
const path = require('path');
const { spawn } = require('child_process');
const internal = require('stream');

app.use(express.static('public-html'));

app.listen(port,() => 
  console.log(`App listening at http://localhost:${port}`))

let csvOne = [];

fs.createReadStream('SimplyHired_data.csv')
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

/* Run the script every 3 days
setInterval(runScripts,(1000 * 60 * 60 * 24) * 3)

function runScripts(){
  console.log('running')
  const SimplyHired = spawn('python',["SimplyHired_scraping.py"]);
  const remoterocketship = spawn('python',["remoterocketship.py"]);
}

 Run once a day */

app.get('/jobs/:jobtitle/:company/:location/:salary/:keywords',(req,res) => {
  let retval = []
  if(req.params.jobtitle == "$ALL"){
    req.params.jobtitle = '';
  }
  if(req.params.company == "$ALL"){
    req.params.company = '';
  }
  if(req.params.location == "$ALL"){
    req.params.location = '';
  }
  if(req.params.salary == "$ALL"){
    req.params.salary = '';
  }
  if(req.params.keywords == "$ALL"){
    req.params.keywords = '';
  }
  let keylist = Object.keys(csvOne[0]);
  for(let i = 0; i < csvOne.length; i++){
    if(csvOne[i][keylist[0]].toLowerCase().includes((req.params.jobtitle).toLowerCase()) 
    & csvOne[i][keylist[1]].toLowerCase().includes((req.params.company).toLowerCase()) 
    & csvOne[i][keylist[2]].toLowerCase().includes((req.params.location).toLowerCase()) 
    & csvOne[i][keylist[4]].includes((req.params.salary))
    & csvOne[i][keylist[3]].toLowerCase().includes((req.params.keywords).toLowerCase())){
      retval.push(csvOne[i])
    }
  }
    res.send(retval)
})

app.get('/jobsTwo/:jobtitle/:company/:location/:salary/:keywords',(req,res) => {
  let retval = []
  if(req.params.jobtitle == "$ALL"){
    req.params.jobtitle = '';
  }
  if(req.params.company == "$ALL"){
    req.params.company = '';
  }
  if(req.params.location == "$ALL"){
    req.params.location = '';
  }
  if(req.params.salary == "$ALL"){
    req.params.salary = '';
  }
  if(req.params.keywords == "$ALL"){
    req.params.keywords = '';
  }
  let keylist = Object.keys(csvTwo[0]);
  for(let i = 0; i < csvTwo.length; i++){
    if(csvTwo[i][keylist[0]].toLowerCase().includes((req.params.jobtitle).toLowerCase()) 
    & csvTwo[i][keylist[1]].toLowerCase().includes((req.params.company).toLowerCase()) 
    & csvTwo[i][keylist[2]].toLowerCase().includes((req.params.location).toLowerCase())
    & csvTwo[i][keylist[5]].includes((req.params.salary))
    & csvTwo[i][keylist[4]].toLowerCase().includes((req.params.keywords).toLowerCase())){
      retval.push(csvTwo[i])
    }
  }
    res.send(retval)
})