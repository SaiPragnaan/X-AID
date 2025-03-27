console.log("hello");

document.addEventListener("DOMContentLoaded", function () {
  let body = document.querySelector("body");
  let modeBtn = document.querySelector("#mode-toggle");

  let currMode = localStorage.getItem("theme");
  if (!currMode || currMode === "auto") {
    currMode = "dark";
    localStorage.setItem("theme", "dark");
  }
  body.classList.add(currMode);

  modeBtn.addEventListener("click", () => {
    currMode = currMode === "light" ? "dark" : "light";
    if (currMode === "light") {
      modeBtn.setAttribute("class", "fa-solid fa-circle-half-stroke");
    }
    else{
        modeBtn.setAttribute("class", "fa-solid fa-moon");
    }
    body.classList.remove("dark", "light");
    body.classList.add(currMode);
    localStorage.setItem("theme", currMode);
  });
});

window.addEventListener("scroll", () => {
  if (window.scrollY < 0) {
    window.scrollTo(0, 0);
  }
});
