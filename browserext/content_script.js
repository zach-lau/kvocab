const scriptElem = document.createElement("script")
scriptElem.text = `
(function initScraper(){
    const TARGET_LANG = "ko";
    const SERVER_URL = "http://127.0.0.1:5000"; // Other hosts might have CORS issues
   
    // Basic post function from mozilla
    async function postJSON(data) {
      try {
        const response = await fetch(SERVER_URL, {
          method: "POST",
          mode : "cors",
          credentials : "include",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
        });
    
        const result = await response.json();
        console.log("Success:", result);
      } catch (error) {
        console.error("Error:", error);
      }
    }

    function send(obj){
        console.log("Sending", obj);
        postJSON(obj);
    }
    
    function vikiExtract(movieObj) {
        console.log("Extracting");
        const movieId = movieObj.video.id;
        const movieName = movieObj.video.container.titles.en;
        const ep = movieObj.video.number;
        for (const track of movieObj.subtitles) {
          if (track.srclang && track.srclang === TARGET_LANG){
            console.log("Found srclanag track");
            send({
                movieId : movieId,
                movieName : movieName,
                ep : ep,
                url : track.src
            });
          }
        }
      }
    
    // Strategy basedon subadub
    const originalParse = JSON.parse;
    JSON.parse = function() {
      const value = originalParse.apply(this, arguments);
      if (value && value.video && value.subtitles){
        console.log("Found subfile");
        vikiExtract(value);
      }
      return value;
    }
    console.log("This is a test");
})();
`;

document.head.insertBefore(scriptElem, document.head.firstChild);
