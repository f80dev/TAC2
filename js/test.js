//1:title
//2:subtitle
//3:delay
//4:style

function createCSS(content){
    var style = document.createElement('style');
    style.type = 'text/css';
    style.innerHTML = content;
    document.getElementsByTagName('head')[0].appendChild(style);
}

createCSS(".text-title {transition:opacity 1s;opacity:0;width:100%;text-align:center;background:none;font-family: 'Open Sans', sans-serif;font-weight:200;color:black;}");

var doc=document;
while(doc.parentNode!=null)
    doc=doc.parentNode;

window.scrollTo(0,0);

var s=doc.createElement("style");
s.innerHTML="@import url('https://fonts.googleapis.com/css?family=Open+Sans:300');";

var div=document.createElement('div');

div.id='title_div';
div.style="display:block;position:absolute;left:0px;top:0px;z-index:30000;width:100%;";
div.innerHTML="<br><br><br><br><div class='text-title' style='font-size:5vw;'>Tutoriel Google Image</div>";

doc.body.appendChild(div);

setTimeout(()=>{div.style.opacity="1"},10);
//Apparition du sous titre
setTimeout(()=>{div.innerHTML+="<br><br><div class='text-title' style='font-size:2.5vw;'>Présentation des fonctions de bases</div>";},7000/2);
//Dispartion de l'ensemble
setTimeout(()=>{div.style.opacity="0"},7000);
//setTimeout(()=>{doc.body.removeChild(div);},7000+2000);