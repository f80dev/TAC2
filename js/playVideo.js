var zone=document.createElement("div");
zone.id="myvideo";
zone.style="position:absolute;top:#2;left:#3;width:#4;height:#5;display:block;z-index:999999999;";
zone.innerHTML="<video width='100%' height='100%' autoplay muted><source src='#1' type='video/mp4'></video>"
document.body.appendChild(zone);
setTimeout(function(){
    document.body.removeChild(zone);
    },#6);


