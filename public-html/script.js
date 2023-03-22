

let intro = document.getElementsByClassName('intro-container2');

let url = 'http://localhost:3000/jobs'
let p = fetch(url);
p.then((response) => response.json())
.then((data) => {
    for(let i = 0; i < data.length; i ++){
        const node = document.createElement("h2");
        const textnode = document.createTextNode(data[i].company);
        node.appendChild(textnode);
        intro[0].appendChild(node);

    }
}
)