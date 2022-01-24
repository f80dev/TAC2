
var div=document.createElement('div');
div.id='subtitle_div';
div.style='padding:10px;border-radius: 10px;border: 1px #bfbec4 solid;box-shadow: 4px 4px 7px #aaa;background-color:lightgrey;opacity:1;pointer-events: none;' +
    'position:absolute;left:0px;top:20vh;margin-left:10%;width:80vw;text-align:center;font-weight:300;font-size:x-large;z-index:100000;';
div.style.filter="blur(0)";
div.innerHTML="#1";
document.body.appendChild(div);
