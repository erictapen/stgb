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

var referencedElements = []

async function init() {
    const left = document.getElementById("left");
    left.innerHTML = await fetchHtmlAsText("stgb.html");
    const right = document.getElementById("right");
    right.innerHTML = await fetchHtmlAsText("cover.html");

    const data = await fetchJSON("stgb.json");

    Object.keys(data["structure"]).forEach(function(id, _) {
      let div = document.getElementById(id);
      let metadata = data["structure"][id]
      let section = metadata["section"];

      if (section) {
        console.log(section);
        document.getElementById(id + "-large-heading").innerText = section;
      }

      div.addEventListener("pointerenter", (event) => {
        if (section) {
          references = data["sections"][section];
          if (references) {
            var referencedElements = references;
            references.forEach((id) => {
              document.getElementById(id).classList.add("referenced");
              console.log("Marked " + section + " " + id);
            });
          }
        }
        console.log(referencedElements);

        event.target.classList.add("highlight");
        metadata["part_of"].forEach((parent) => {
          document.getElementById(parent).classList.remove("highlight");
          document.getElementById(parent).classList.add("lowlight");
        });

        document.getElementById(`right-${metadata["level"]}`).innerHTML = metadata["title"];

      });

      div.addEventListener("pointerleave", (event) => {
        event.target.classList.remove("highlight");
        event.target.classList.remove("lowlight");

        if (section) {
          references = data["sections"][section];
          if (references) {
            references.forEach((id) => {
              document.getElementById(id).classList.remove("referenced");
            });
            var referencedElements = []
          }
        }

        document.getElementById(`right-${metadata["level"]}`).innerHTML = "";
      });

    });

}

window.addEventListener("load", (event) => {
  console.log("page is fully loaded");
  init();
  console.log("finished init")
});
