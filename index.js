/**
  * @param {String} url - address for the HTML to fetch
  * @return {String} the resulting HTML string fragment
  */
async function fetchHtmlAsText(url) {
    return await (await fetch(url)).text();
}

async function init() {
    const contentDiv = document.getElementById("left");
    contentDiv.innerHTML = await fetchHtmlAsText("stgb.html");
}

window.addEventListener("load", (event) => {
  console.log("page is fully loaded");
  init();
  console.log("finished")
});
