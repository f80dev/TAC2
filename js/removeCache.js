//#1=id du cache

function removeCache(){
    document.body.removeChild(document.getElementById("#1"));
}

var div=document.getElementById("#1");
if(div!=null){
    setTimeout(() => {removeCache();},10000);
    div.style.opacity="0";
}


