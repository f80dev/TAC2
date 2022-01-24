//#1=title
//#2=subtitle
//#3=delay in millisecond
//#4=style

function createCSS(content){
    var style = document.createElement('style');
    style.type = 'text/css';
    style.innerHTML = content;
    document.getElementsByTagName('head')[0].appendChild(style);
}

var doc=document;
while(doc.parentNode!=null)doc=doc.parentNode;

window.scrollTo(0,0);

var s=doc.createElement("style");
s.innerHTML="@import url('https://fonts.googleapis.com/css?family=Open+Sans:300');";

var div=document.createElement('div');

div.id='title_div';
div.style="display:block;position:absolute;left:10%;top:0px;z-index:30000;width:80%;height:100vh;transition:opacity 1s;opacity:0;";
div.innerHTML="<div style=\"#4;margin-top:20%;font-family:'Open Sans',sans-serif;font-size:5vw;\">#1</div>";

doc.body.appendChild(div);

setTimeout(function(){div.style.opacity="1";},10);

if(#3<100000){
    setTimeout(function(){div.innerHTML+="<br><br><br><div style='#4;font-size:2.5vw;'>#2</div>";},#3/5+1);
    setTimeout(function(){div.style.opacity="0"},#3-2000);
    setTimeout(function(){doc.body.removeChild(div);},#3);
} else {
    setTimeout(function(){div.innerHTML+="<br><div style='#4;margin-top:5vh;font-size:2.5vw;'>#2</div>";},1000);
}

