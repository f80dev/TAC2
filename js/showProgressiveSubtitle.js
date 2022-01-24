var i=0;
var div=document.createElement("div");

function addWord(){
    if(i<words.length){
        div.innerHTML+=words[i]+" ";
        setTimeout(addWord,delay*0.4+delay*(0.3)*Math.random());
    }else{
        setTimeout(()=>{
            document.body.removeChild(div);
        },300);
    }
    i=i+1;

}

div.id="subtitle_div";
div.style="#3;position:absolute;left:0px;top:#position;margin-left:10%;width:80vw;text-align:center;pointer-events: none;z-index:100000;";

var words="#1".split(" ");
var delay=#2/words.length;

div.innerHTML="";
document.body.appendChild(div);
addWord();






