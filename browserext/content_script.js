const scriptElem = document.createElement("script")
scriptElem.text = `
(function initScraper(){
    const TARGET_LANG = "ko";

    function send(obj){
        console.log("Sending", obj);
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
