const server = "http://localhost:5001";
// Global element values - could make these functions I guess...
const wordElem = document.getElementById("word");
const posElem = document.getElementById("pos");
const meaningElem = document.getElementById("meaning");
const exampleElem = document.getElementById("example");
const typeElem = document.getElementById("type");
// State variables
let currentId = null;
let currentWord = null;

function populate(word){
    wordElem.value = word.word;
    posElem.value = word.pos;
    meaningElem.value = word.meaning;
    exampleElem.value = word.example;
    typeElem.value = 5;
}
function addOptions(options){
    const selectElem = document.getElementById("type");
    for (const t of options.types){
        const opt = document.createElement("option");
        opt.value = t.id;
        opt.innerText = `${t.id}: ${t.value}`;
        selectElem.appendChild(opt);
    }
}
async function getNewWord(){
    return fetch(`${server}/new`).then((res) => res.json());
}
async function getOptions(){
    return fetch(`${server}/types`).then((res) => res.json());
}
function updateSearchURL(searchTerm){
    const dict_link = "https://korean.dict.naver.com/koendict/#/search";
    const search_link = `${dict_link}?query=${searchTerm}`;
    const searchFrame = document.querySelector(".lookup iframe");
    searchFrame.src = search_link;
}
async function postJSON(post_url, data) {
    try {
      const response = await fetch(post_url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });
      const result = await response.json();
    //   console.log("Success:", result);
    } catch (error) {
      console.error("Error:", error);
    }
  }
function refresh(){
    getNewWord().then((word) => {
        // console.log(word);
        populate(word);
        updateSearchURL(word.word);
        currentId = word.id;
        currentWord = word.word;
    })
    meaningElem.focus();
}

function sendData(){
    // Send data and return promse resolving to response
    if (currentWord === wordElem.value){
        const data = {
            id : currentId,
            meaning : meaningElem.value,
            type : typeElem.value
        }
        // console.log(subObj);
        return postJSON(`${server}/update`, data)
    }
    else {
        // We have changed the word
        const data = {
            word : wordElem.value,
            pos : posElem.value,
            meaning : meaningElem.value,
            type : typeElem.value,
            num : 0,
            example : exampleElem.value,
        }
        return postJSON(`${server}/addnew`, data)
    }
}
function submit(){
    sendData().then(()=>refresh());
}

// Main loop code
getOptions().then((options) => {
    // console.log(options.types);
    addOptions(options);
});
refresh();
document.getElementById("subButton").onclick = submit;
document.getElementById("ref-button").onclick = () => {
    updateSearchURL(wordElem.value); // Update with the current value
}
