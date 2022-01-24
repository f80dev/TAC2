var img=document.createElement('img');
img.name='infoclick_img';
img.style='pointer-events: none;position:absolute;left:#1px;top:#2px;width:40px;height:40px;z-index:1000;';
img.src='https://shifumixweb.appspot.com/assets/img/handclick.svg';

document.body.appendChild(img);
setTimeout(() => {
    document.getElementsByName('infoclick_img').forEach((child) => {
        document.body.removeChild(child);
    });
},#3);