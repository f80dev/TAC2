//#1=text
//#2=delay in milliseconde

var div=document.createElement("div");
div.id="subtitle_div";
div.style="#3;transition:opacity 0.6s;opacity:0;filter:blur(0.035rem);position:absolute;left:0px;top:#4;margin-left:10%;width:80vw;text-align:center;pointer-events: none;z-index:99999999999;";
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
    },#2-500);

