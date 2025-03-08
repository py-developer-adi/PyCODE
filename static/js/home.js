var typed = new Typed('.greet', {
    strings: ['HELLO!'],
    typeSpeed: 20,
    showCursor: false,
    onComplete: function(){
        setTimeout(() => {
            var typed2 = new Typed('.headline', {
                strings: ['Welcome to PyCODE'],
                typeSpeed: 20,
                showCursor: false,
                onComplete: function(){
                    setTimeout(() => {
                        var typed3 = new Typed('.sub-headline', {
                            strings: ['Learn, Build, and Innovate!'],
                            typeSpeed: 20,
                            showCursor: false,
                            onComplete: function(){
                                setTimeout(() => {
                                    document.querySelectorAll(".hero-img").forEach((ele) => {
                                        ele.style.opacity = "1";
                                    });
                                    setTimeout(() => {
                                        document.querySelectorAll(".hero-img").forEach((ele) => {
                                            ele.classList.add("flip");
                                        });
                                        setTimeout(() => {
                                            document.querySelectorAll(".hero-img").forEach((ele) => {
                                                ele.classList.remove("flip");
                                            });
                                        }, 800);
                                    }, 500);
                                }, 500);
                            }
                        });
                    }, 500)
                }
            });
        }, 500);
    }
})

/* 
document.querySelector(".hero-img").style.opacity = "1";
                                    setTimeout(() => {
                                        document.querySelector('.hero-img').classList.add("flip");
                                        setTimeout(() => {
                                            document.querySelector('.hero-img').classList.remove("flip");
                                        }, 500);
                                    }, 500);
*/

document.addEventListener('scroll', () => {
    document.querySelector(".benefit_section").classList.add("fade-in")
})