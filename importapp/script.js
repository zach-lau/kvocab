const server = "http://localhost:5001";
function populate(word){
    const wordElem = document.getElementById("word");
    const meaningElem = document.getElementById("meaning");
    const exampleElem = document.getElementById("example");
    wordElem.value = word.word;
    meaningElem.value = word.meaning;
    exampleElem.value = word.example;
}
function addOptions(options){
    const selectElem = document.getElementById("type");
    for (const t of options.types){
        const opt = document.createElement("option");
        opt.value = t.id;
        opt.innerText = t.value;
        selectElem.appendChild(opt);
    }
}
async function getNewWord(){
    return fetch(`${server}/new`).then((res) => res.json());
}
async function getOptions(){
    return fetch(`${server}/types`).then((res) => res.json());
}
getNewWord().then((word) => {
    // console.log(word);
    populate(word);
})
getOptions().then((options) => {
    console.log(options.types);
    addOptions(options);
})
