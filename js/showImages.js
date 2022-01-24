function createCSS(content){
    var style = document.createElement('style');
    style.type = 'text/css';
    style.innerHTML = content;
    document.getElementsByTagName('head')[0].appendChild(style);
}

var doc=document;
while(doc.parentNode!=null)
    doc=doc.parentNode;

var div=document.createElement('div');
div.id='title_div';
div.style='z-index:100000;pointer-events: none;position:absolute;left:0px;top:0px;width:100vw;height:100vh;text-align:center;font-size:x-large;background-color:black;color:white;font-weight:200;';
div.innerHTML="<img src='#1' style='width:100vw;object-fit:cover'>";
doc.body.appendChild(div);

createCSS(".visible {visibility: visible;opacity: 1;transition: opacity 0s 2s linear;}");
createCSS(".hidden  {visibility: hidden;opacity: 0;transition: visibility 0s 2s, opacity 2s linear;}");

setTimeout(()=>{div.className="visible"},400);
setTimeout(()=>{div.className="hidden"},#2*1000);