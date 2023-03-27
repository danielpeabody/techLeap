

let intro = document.getElementsByClassName('intro-container2');

let url = 'http://localhost:3000/jobs'
let p = fetch(url);
p.then((response) => response.json())
.then((data) => {
    for(let i = 0; i < data.length; i ++){
        let keylist = Object.keys(data[0]);
        const node = document.createElement("h2");
        const textnode = document.createTextNode(data[i][keylist[0]] + " | " + data[i][keylist[1]] + " | " +  data[i][keylist[2]] + " | " + data[i][keylist[4]] + " | " + data[i][keylist[5]] + " | " + data[i][keylist[6]]);
        node.appendChild(textnode);
        intro[0].appendChild(node);

    }
}
)