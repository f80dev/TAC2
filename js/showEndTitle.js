function createCSS(content){
    var style = document.createElement('style');
    style.type = 'text/css';
    style.innerHTML = content;
    document.getElementsByTagName('head')[0].appendChild(style);
}

var s=document.createElement("style");
s.innerHTML="@import url('https://fonts.googleapis.com/css?family=Open+Sans:300');";

var div=document.createElement('div');
div.id='title_div';
div.style='z-index:1000;pointer-events: none;position:absolute;left:0px;top:0px;width:100%;height:100%;text-align:center;font-size:x-large;background-color:black;color:white;';
div.innerHTML="<div style='display:inline;font-family: \"Open Sans\", sans-serif;width:80%;text-align:center;font-size:x-large;font-weight:300;'>#1</div>";
document.body.appendChild(div);

createCSS(".visible {visibility: visible;opacity: 1;transition: opacity 2s linear;}");
createCSS(".hidden  {visibility: hidden;opacity: 0;transition: visibility 0s 2s, opacity 2s linear;}");

div.className="hidden";

setTimeout(()=>{div.className="visible"},1000);