const scriptElem = document.createElement("script")
scriptElem.text = `
(function initScraper(){
    const TARGET_LANGS = ["ko", "ja", "yue"];
    const SERVER_URL = "https://localhost:5000"; // Other hosts might have CORS issues
    const WEBVTT_FMT = 'webvtt-lssdh-ios8';
    const IMSC = 'imsc1.1';

    // Used to translate audio to subtitle where appropriate for netflix
    const NETFLIX_SUB_DICT = { yue : "zh-Hant" };
     
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
        // console.log("Sending", obj);
        postJSON(obj);
    }
    
    function vikiExtract(movieObj) {
        console.log("Extracting");
        const movieId = movieObj.video.id;
        const movieName = movieObj.video.container.titles.en;
        const ep = movieObj.video.number;
        const originLang = movieObj.video.origin.language;
        if (!TARGET_LANGS.includes(originLang))
          return;
        for (const track of movieObj.subtitles) {
          if (track.srclang && track.srclang === originLang){
            console.log("Found srclang track");
            send({
                movieId : movieId,
                movieName : movieName,
                ep : ep,
                url : track.src,
                lang : originLang
            });
          }
        }
      }

    function getOriginLangNetflix(movieObj){
      for (const track of movieObj.audio_tracks){
        if (track.languageDescription && track.languageDescription.includes("[Original]")){
          console.log("Origin language", track.language);
          return track.language;
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
      const originLang = getOriginLangNetflix(movieObj);
      let subLang = NETFLIX_SUB_DICT[originLang];
      if (!subLang)
        subLang = originLang;
      if (!TARGET_LANGS.includes(originLang))
        return;
      for (const track of movieObj.timedtexttracks){
        if (track.isForcedNarrative || track.isNoneTrack) continue;
        if (!track.ttDownloadables) continue;
        if (track.language !== subLang) continue;
        if (track.languageDescription === "Off") continue;
        console.log("Target lang subs");
        // console.log(track);
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
          url : bestUrl,
          lang : originLang
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
          if (value && value.result 
            && value.result.movieId 
            && value.result.timedtexttracks
            && value.result.duration > 300000 // Get rid of short clips
            ) {
            // console.log("Netflix subs");
            console.log(value);
            netflixExtract(value.result);
          }
      }
      return value;
    }
    console.log(window.location.hostname);
})();
`;

document.head.insertBefore(scriptElem, document.head.firstChild);
