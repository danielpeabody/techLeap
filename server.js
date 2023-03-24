
const csv = require('csv-parser');
const fs = require('fs');
const express = require('express')
const app     = express();
const port    = 3000;
const path = require('path');
const results = [];

app.use(express.static('public-html'));

app.listen(port, () => 
  console.log(`App listening at http://localhost:${port}`))

fs.createReadStream('jobs.csv')
.pipe(csv({}))
.on('data',(data) => results.push(data))
.on('end', ()=>{
    console.log('done');
});




app.get('/jobs',(req,res) => {
    res.send(results)
})