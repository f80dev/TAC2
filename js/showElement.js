//#1=position left de l'objet
//#2=position top de l'objet
//#3=width de l'objet
//#4=height de l'objet
//#5=image à utiliser
//#6=delay de disparition


var img=document.createElement("img");
img.name="infoclick_img";
img.style="z-index:99999999999;pointer-events: none;position:fixed;left:#1px;top:#2px;width:#3px;height:#4px;pointer-events:none;";
img.src="#5";
document.body.appendChild(img);
setTimeout(() => {
    document.getElementsByName("infoclick_img").forEach((child) => {
        document.body.removeChild(child);
    });
},#6);