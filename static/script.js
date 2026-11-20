let movements=[]

document.addEventListener("mousemove",e=>{

movements.push({
x:e.clientX,
y:e.clientY,
t:Date.now()
})

})

function sendData(){

fetch("/behavior",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify(movements)

})
.then(res=>res.json())
.then(data=>{

if(data.bot){
alert("Bot behavior detected")
}else{
alert("Human behavior detected")
}

})

fingerprint()

}

function fingerprint(){

const fp={
userAgent:navigator.userAgent,
platform:navigator.platform,
language:navigator.language,
screen:screen.width+"x"+screen.height
}

fetch("/fingerprint",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify(fp)

})

}