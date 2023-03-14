
const csv = require('csv-parser');
const fs = require('fs');
const { it } = require('node:test');
const results = []

fs.createReadStream('jobs.csv')
.pipe(csv({}))
.on('data',(data) => results.push(data))
.on('end', ()=>{
    console.log('done');
});

setTimeout(() => {
    for(let i = 0; i < results.length; i++){
        console.log(results[i]);
    }
},1000)