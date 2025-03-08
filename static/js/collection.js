document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll(".model").forEach((model) => {
        model.classList.add("fade-in");
    });
})

setTimeout(() => {
    document.querySelectorAll(".model").forEach((model) => {
        model.classList.remove("hidden");
        model.classList.remove("fade-in");
    })
}, 1000);