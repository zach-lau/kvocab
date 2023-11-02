const scriptElem = document.createElement("script")
scriptElem.text = `
(function initScraper(){
    const TARGET_LANGS = ["ko"];
    const SERVER_URL = "http://127.0.0.1:5000"; // Other hosts might have CORS issues
    const WEBVTT_FMT = 'webvtt-lssdh-ios8';
    const IMSC = 'imsc1.1';
     
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
        const origin_lang = movieObj.video.origin.language;
        if (!TARGET_LANGS.includes(origin_lang))
          return;
        for (const track of movieObj.subtitles) {
          if (track.srclang && track.srclang === origin_lang){
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

    // This function is mostly copied from subadub
    function netflixExtract(movieObj){
      console.log("Netflix extract");
      const movieId = movieObj.movieId;
      const filenamePieces = [];
      for (const elem of document.querySelectorAll('.a[data-uia="video-title]')) {
        console.log("Found elem");
        if (elem.textContent) { // only get 'leaf' elements with text
          filenamePieces.push(elem.textContent);
        }
      }
      let movieName;
      if (filenamePieces.length) {
        srcFilename = filenamePieces.join(' ');
      } else {
        movieName = movieId.toString();
      }
      // console.log(filenamePieces);
      for (const track of movieObj.timedtexttracks){
        console.log("test");
        if (track.isForcedNarrative || track.isNoneTrack) continue;
        if (!track.ttDownloadables) continue;
        if (!TARGET_LANGS.includes(track.language)) continue;
        console.log("Korean subs");
        console.log(track);
        let dlObj = track.ttDownloadables[WEBVTT_FMT];
        if (!dlObj || !dlObj.urls){
          dlObj = track.ttDownloadables[IMSC];
        } 
        if (!dlObj || !dlObj.urls) continue;
        const bestUrl = dlObj.urls[0].url;
        if (!bestUrl) continue;
        console.log("Found src lang track");
        send({
          movieId : movieId,
          movieName : movieName,
          ep : 1,
          url : bestUrl
        });
      }
    }
    
    // Strategy basedon subadub
    const originalParse = JSON.parse;
    JSON.parse = function() {
      const value = originalParse.apply(this, arguments);
      // Different parsing strategy based on hostname
      switch(window.location.hostname){
        case "www.viki.com":
          if (value && value.video && value.subtitles){
            console.log("Found subfile");
            vikiExtract(value);
          }
          break;
        case "www.netflix.com":
          if (value && value.result && value.result.movieId && value.result.timedtexttracks) {
            console.log("Netflix subs");
            netflixExtract(value.result);
          }
      }
      return value;
    }
    console.log("This is a test");
    console.log(window.location.hostname);
})();
`;

document.head.insertBefore(scriptElem, document.head.firstChild);
