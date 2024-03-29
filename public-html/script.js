

let jobholder = document.getElementsByClassName('jobholder');
let searchbutton = document.getElementById('searchbutton');
let filterTitle = document.getElementById('filtertitle');
console.log(filterTitle);


searchbutton.addEventListener("click",(event)=>{
    console.log('click')
    while (jobholder[0].firstChild) {
        jobholder[0].firstChild.remove();
    }
    jobsearch();
});

function jobsearch(){
let jobtitle = document.getElementById('title');
if(jobtitle.value == ''){
    jobtitle.value = "$ALL";
}
let company = document.getElementById('company');
if(company.value == ''){
    company.value = "$ALL";
}
let location = document.getElementById('location');
if(location.value == ''){
    location.value = "$ALL";
}
let salary = document.getElementById('salary');
if(salary.value == ''){
    salary.value = "$ALL";
}

let keywords = document.getElementById('keywords');
if(keywords.value == ''){
    keywords.value = "$ALL";
}
console.log(location.value)
let url = 'jobs/' + jobtitle.value + "/" + company.value + "/" + location.value + "/" + salary.value + "/" + keywords.value;
let p = fetch(url);
let jobList = [];
let jobnumber = 0;
p.then((response) => response.json())
.then((data) => {
    jobnumber = jobnumber + data.length
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

        jobList.push(singlejob);

    }
    let url2 = 'jobsTwo/' + jobtitle.value + "/" + company.value + "/" + location.value + "/" + salary.value + "/" + keywords.value;
    let q = fetch(url2);
    q.then((response) => response.json())
    .then((data) => {
        jobnumber = jobnumber + data.length
        for(let i = 0; i < data.length; i ++){
            let keylist = Object.keys(data[0]);
            const singlejob = document.createElement("div");
            singlejob.className = "singlejob";

            const h3 = document.createElement("h3");
            h3.className = "jobtitle-salary";
            h3.innerText = data[i][keylist[0]] + " | " + "N/A";
            singlejob.appendChild(h3);
    
            const h4 = document.createElement("h4");
            h4.className = "jobcompany-rating";
            h4.innerText = data[i][keylist[1]] + " | " + "N/A"
            singlejob.appendChild(h4);
    
            const h5 = document.createElement("h5");
            h5.className = "joblocation";
            h5.innerText = data[i][keylist[2]];
            singlejob.appendChild(h5);
    
            const p = document.createElement("p");
            p.className = "jobsnip";
            let textContent = data[i][keylist[4]].slice(0,300) + "...";
            let textContent2 = textContent.replace(/\n|\r/g, "");
            p.innerText = textContent2
            singlejob.appendChild(p);
            
            const a = document.createElement("a");
            a.href = data[i][keylist[7]];
            const button = document.createElement("button");
            button.className = "applybutton";
            button.innerText = "Apply";
            button.target = "_blank"
            a.appendChild(button);
            singlejob.appendChild(a);

            jobList.push(singlejob)
        }
        console.log(filterTitle.textContent);
        filterTitle.textContent = "Filtering Options | Showing " + jobnumber + " jobs"
        if(jobtitle.value == "$ALL"){
            jobtitle.value = '';
        }
        if(company.value == "$ALL"){
            company.value = '';
        }
        if(location.value == "$ALL"){
            location.value = '';
        };
        if(salary.value == "$ALL"){
            salary.value = '';
        };
        if(keywords.value == "$ALL"){
            keywords.value = '';
        };
        let shuffleJobs = shuffle(jobList);
        for(let i = 0; i < shuffleJobs.length; i++){
            jobholder[0].appendChild(shuffleJobs[i]);
        }

    })
})


}

function shuffle(array) {
    let currentIndex = array.length,  randomIndex;
  
    // While there remain elements to shuffle.
    while (currentIndex != 0) {
  
      // Pick a remaining element.
      randomIndex = Math.floor(Math.random() * currentIndex);
      currentIndex--;
  
      // And swap it with the current element.
      [array[currentIndex], array[randomIndex]] = [
        array[randomIndex], array[currentIndex]];
    }
  
    return array;
  }