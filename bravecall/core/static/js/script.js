const imageContainer = document.querySelector(".image-container");
const image = document.querySelector(".image");

imageContainer.addEventListener("mousemove", (event) => {
    let xAxis = (window.innerWidth / 2 - event.pageX) / 25;
    let yAxis = (window.innerHeight / 2 - event.pageY) / 25;

    image.style.transform = `rotateY(${xAxis}deg) rotateX(${yAxis}deg) scale(1.1)`;
    image.style.boxShadow = `${-xAxis}px ${yAxis}px 20px rgba(0, 0, 0, 0.5)`;
});

imageContainer.addEventListener("mouseleave", () => {
    image.style.transform = "rotateY(0deg) rotateX(0deg) scale(1)";
    image.style.boxShadow = "none";
});

// Auto spin every 3 seconds
let rotation = 0;
setInterval(() => {
    rotation += 360;
    image.style.transition = "transform 2s ease-in-out";
    image.style.transform = `rotateY(${rotation}deg)`;
}, 3000);