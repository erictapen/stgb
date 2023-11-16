/**
  * @param {String} url - address for the HTML to fetch
  * @return {String} the resulting HTML string fragment
  */
async function fetchHtmlAsText(url) {
    return await (await fetch(url)).text();
}

async function fetchJSON(url) {
    return await fetch(url)
        .then(res => res.json())
        .catch(err => { throw err });
}

async function init() {
    const left = document.getElementById("left");
    left.innerHTML = await fetchHtmlAsText("stgb.html");
    const right = document.getElementById("right");
    right.innerHTML = await fetchHtmlAsText("cover.html");

    const structure = await fetchJSON("stgb.json");

    Object.keys(structure).forEach(function(id, _) {
      let div = document.getElementById(id);
      div.addEventListener("pointerenter", (event) => {
        console.log(event);
        let metadata = structure[event.target.id]
        event.target.classList.add("highlight");
        metadata["part_of"].forEach(function(parent) {
          document.getElementById(parent).classList.remove("highlight");
          document.getElementById(parent).classList.add("lowlight");
        });
        document.getElementById(`right-${metadata["level"]}`).innerHTML = metadata["title"];
      });
      div.addEventListener("pointerleave", (event) => {
        console.log(event);
        let metadata = structure[event.target.id]
        event.target.classList.remove("highlight");
        event.target.classList.remove("lowlight");
        document.getElementById(`right-${metadata["level"]}`).innerHTML = "";
      });
      // structure[key];
    });

}

window.addEventListener("load", (event) => {
  console.log("page is fully loaded");
  init();
  console.log("finished init")
});
