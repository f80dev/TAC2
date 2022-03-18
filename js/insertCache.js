var delayInSec=#1;

if(document.getElementById("#4")==null){
    var div=document.createElement("div");
    div.id="#4";
    div.style="opacity:0;transition: opacity "+delayInSec+"s;#2;z-index:#3;pointer-events: none;position:fixed;left:0;top:0;width:100vw;height:100vh;pointer-events:none;";
    document.body.appendChild(div);
    setTimeout(()=>{
        div.style.opacity="1";
    },100);
}
