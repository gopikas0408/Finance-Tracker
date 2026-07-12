const sidebar=document.getElementById("sidebar");
const overlay=document.getElementById("overlay");
const mobileBtn=document.getElementById("mobile-menu-btn");

mobileBtn.addEventListener("click",()=>{

sidebar.classList.toggle("active");
overlay.classList.toggle("active");

});

overlay.addEventListener("click",()=>{

sidebar.classList.remove("active");
overlay.classList.remove("active");

});