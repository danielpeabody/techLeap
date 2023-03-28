

let jobholder = document.getElementsByClassName('jobholder');

let url = 'http://localhost:3000/jobs'
let p = fetch(url);
p.then((response) => response.json())
.then((data) => {
    for(let i = 0; i < data.length; i ++){
        let keylist = Object.keys(data[0]);
        const singlejob = document.createElement("div");
        singlejob.className = "singlejob";
        //const textnode = document.createTextNode(data[i][keylist[0]] + " | " + data[i][keylist[1]] + " | " +  data[i][keylist[2]] + " | " + data[i][keylist[4]] + " | " + data[i][keylist[5]] + " | " + data[i][keylist[6]]);
        const h3 = document.createElement("h3");
        h3.className = "jobtitle-salary";
        h3.innerText = data[i][keylist[0]] + " | " + data[i][keylist[4]]
        singlejob.appendChild(h3);

        const h4 = document.createElement("h4");
        h4.className = "jobcompany-rating";
        h4.innerText = data[i][keylist[1]] + " | " + data[i][keylist[5]]
        singlejob.appendChild(h4);

        const h5 = document.createElement("h5");
        h5.className = "joblocation";
        h5.innerText = data[i][keylist[2]];
        singlejob.appendChild(h5);

        const p = document.createElement("p");
        p.className = "jobsnip";
        p.innerText = data[i][keylist[3]];
        singlejob.appendChild(p);
        
        const a = document.createElement("a");
        a.href = "https://www."+ data[i][keylist[6]];
        const button = document.createElement("button");
        button.className = "applybutton";
        button.innerText = "Apply";
        button.target = "_blank"
        a.appendChild(button);
        singlejob.appendChild(a);

        jobholder[0].appendChild(singlejob);
    }
    let url2 = 'http://localhost:3000/jobsTwo'
    let q = fetch(url2);
    q.then((response) => response.json())
    .then((data) => {
        console.log(data)
    })
})