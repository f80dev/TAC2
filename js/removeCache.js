//#1=id du cache

var delay=#2*1000;

function removeCache(){
    document.body.removeChild(document.getElementById("#1"));
}

var div=document.getElementById("#1");
if(div!=null){
    setTimeout(() => {removeCache();},delay);
    div.style.opacity="0";
}


