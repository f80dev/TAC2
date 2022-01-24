function createCSS(content){
    var style = document.createElement('style');
    style.type = 'text/css';
    style.innerHTML = content;
    document.getElementsByTagName('head')[0].appendChild(style);
}

createCSS(".hidden  {visibility: hidden;opacity: 0;transition: visibility 0s 1s, opacity 1s linear;}");
var elt=document.getElementById("#1");
elt.style.opacity=1;
elt.classList.add("hidden");
setTimeout(()=>{elt.remove();},1000);

