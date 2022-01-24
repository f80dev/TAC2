var div=document.createElement("div");
div.id="div_text";
div.style="transition:opacity 0.6s;opacity:0;position:absolute;left:0px;top:#2;margin-left:10%;width:80vw;text-align:left;pointer-events: none;z-index:100000;";
div.innerHTML="#1";
document.body.appendChild(div);
setTimeout(()=>{
    div.style.opacity="1";
},10);
setTimeout(() => {
                    try{
                        div.style.opacity="0";
                        setTimeout(function(){
                            document.body.removeChild(div);
                        },800);
                    }catch (e) {

                    }
    },#2);

