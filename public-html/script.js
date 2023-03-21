
let url = 'http://localhost:3000/jobs'
let p = fetch(url);
p.then((response) => response.json())
.then((data) => {
    console.log(data);
    console.log('test');
    }
)