let eat = document.querySelector('#home-eat');
let drink = document.querySelector('#home-drink');
let bg = document.querySelector('#image-bg')

eat.addEventListener('mouseenter',() =>{
    document.getElementById("image-bg").src = "static/main/Images/bg_eat.jpg";
    // document.getElementById("image-bg").style.transitionDuration = ".5s";

});

eat.addEventListener('mouseleave',() =>{
    document.getElementById("image-bg").src = "/static/main/Images/bg_restaurant.jpg";
    // document.getElementById("image-bg").style.transitionDuration = ".5s";
    
});

drink.addEventListener('mouseenter',() =>{
    document.getElementById("image-bg").src = "/static/main/Images/bg_drink.jpg";
});


drink.addEventListener('mouseleave',() =>{
    document.getElementById("image-bg").src = "/static/main/Images/bg_restaurant.jpg";
});
