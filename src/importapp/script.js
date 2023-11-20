const server = "http://localhost:5001";
// Global element values - could make these functions I guess...
const wordElem = document.getElementById("word");
const posElem = document.getElementById("pos");
const meaningElem = document.getElementById("meaning");
const exampleElem = document.getElementById("example");
const typeElem = document.getElementById("type");

const langElem = document.getElementById("select-lang");

const dbElem = document.querySelector(".database");
// State variables
let currentId = null;
let currentWord = null;
let currentLanguage = 1;
let validWord = false;

function populate(word){
    wordElem.value = word.word;
    posElem.value = word.pos;
    meaningElem.value = word.meaning;
    exampleElem.value = word.example;
    typeElem.value = 5;
}
function addOptions(elem, optionsList){
    for (const t of optionsList){
        const opt = document.createElement("option");
        opt.value = t.id;
        opt.innerText = `${t.id}: ${t.value}`;
        elem.appendChild(opt);
    }
}
async function getNewWord(language){
    return fetch(`${server}/new?language=${language}`).then((res) => res.json());
}
async function getTypes(){
    return fetch(`${server}/types`).then((res) => res.json());
}
async function getLanguages(){
    return fetch(`${server}/languages`).then((res) => res.json());
}
async function getDatabase(){
    return fetch(`${server}/dbname`).then((res) => res.json());
} 

function updateSearchURL(searchTerm){
    // Todo might need to more complicated logic to perform search later e.g. post request
    const dictionaries = {
        1 : "https://korean.dict.naver.com/koendict/#/search?query=",
        2 : "https://cantonese.org/search.php?q=",
    };
    const dict_link = dictionaries[currentLanguage];
    if (!dict_link) dict_link = "https://www.google.com/search?q="
    const search_link = `${dict_link}${searchTerm}`;
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
function clearInputs(){
    [wordElem, posElem, meaningElem, exampleElem].forEach((elem) => {
        elem.value = "";
    })
}
function refresh(){
    getNewWord(currentLanguage).then((word) => {
        // console.log(word);
        if (!word.valid){
            clearInputs();
            validWord = false;
            return;
        }
        populate(word);
        updateSearchURL(word.word);
        currentId = word.id;
        currentWord = word.word;
        validWord = true;
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
            language : currentLanguage,
            example : exampleElem.value,
        }
        return postJSON(`${server}/addnew`, data)
    }
}
function submit(){
    sendData().then(()=>refresh());
}

// Main loop code
getTypes().then((types) => {
    // console.log(options.types);
    addOptions(typeElem, types.types);
});
getLanguages().then((languages) => {
    addOptions(langElem, languages.languages);
})
getDatabase().then((res)=>{
    dbElem.innerText = `Database name: ${res["name"]}`;
});
refresh();
document.getElementById("subButton").onclick = submit;
document.getElementById("ref-button").onclick = () => {
    updateSearchURL(wordElem.value); // Update with the current value
}
document.getElementById("refresh-language").onclick = () => {
    currentLanguage = langElem.value;
    refresh();
}