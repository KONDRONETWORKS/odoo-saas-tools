const counts = document.querySelectorAll(".count");
const speed = 397;
counts.forEach((count) => {
  function upDate() {
    const target = Number(count.getAttribute("data-target"));
    const counter = Number(count.innerText);
    const inc = target / speed;
    if (counter < target) {
      count.innerText = Math.floor(inc + counter);
      setTimeout(upDate, 15);
    } else {
      count.innerText = target;
    }
  }
  upDate();
});
