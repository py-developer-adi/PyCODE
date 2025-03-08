let menu = document.querySelector(".menu");
menu.addEventListener('click', () => {
    if(document.querySelector(".bar1").classList.contains("rotate-45n")){
        document.querySelector(".bar1").classList.remove("rotate-45n");
        document.querySelector(".bar2").classList.remove("rotate-45p");
        document.querySelector(".bar1").style.margin = "10px 0px"
        document.querySelector(".bar2").style.margin = "10px 0px"
        document.querySelector(".bottom").classList.remove('wipe-right');
        document.querySelector(".bottom").style.display = "none";
    } else {
        document.querySelector(".bar1").classList.add("rotate-45n");
        document.querySelector(".bar2").classList.add("rotate-45p");
        document.querySelector(".bar1").style.margin = "-2px 0px"
        document.querySelector(".bar2").style.margin = "-1px 0px"
        document.querySelector(".bottom").classList.add('wipe-right');
        document.querySelector(".bottom").style.display = "flex";
    }
})