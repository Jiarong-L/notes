


<style>
    th {
        border: 1;
        background-color: beige;
    }
    td {
        border: 1;
    }
    button {
        background-color: rgb(222, 217, 217);
    }
    .back {
        border-color:red;
    }
    /* canvas {
        border: 1px solid black;
    } */
</style>
    



<fieldset>
    <legend>南萧音调</legend>
    <button id="C-Key-button" onclick="myFunction('C-Key')">C-Key</button>  
    <button id="D-Key-button" onclick="myFunction('D-Key')">D-Key</button>  
    <button id="F-Key-button" onclick="myFunction('F-Key')">F-Key</button>  
    <button id="G-Key-button" onclick="myFunction('G-Key')">G-Key</button>  
    <button id="bB-Key-button" onclick="myFunction('bB-Key')">bB-Key</button>
</fieldset>

<div>
    <h2 id="Current-Key"></h2>
    <table id="Key-Table" border="2" bordercolor="black" cellspacing="0" cellpadding="1"></table>
</div>


<div>
 <h2>参考</h2>
 
 <img src="../Nanyin/keys.png" alt="南音洞箫指法表——《泉州南音洞箫教程》">  <br> 《泉州南音洞箫教程》  <br>   <br> 
 <a href="http://www.qznanyin.cn/zrhy.html">直入花园: http://www.qznanyin.cn/zrhy.html</a>  <br> 
 <a href="http://www.qzhnet.com/qzh153.htm#gongchapu">工乂谱: 乂、工、六、思/士/电、一/乙</a>
</div>

    
    
<script>
var fullTable = {
    "BlowType" : ["缓","缓","缓","缓","缓","缓","缓","缓","缓","缓","缓","缓",  
               "急","急","急","急","急","急","急","急","急","急","急","急","急",
               "超","超","超","超","超","超","超","超","超" ],
    "KeyName" : ["艹工","艹六","艹乂六","贝士","士","下","毛乂","贝乂","乂","乂","乂","全乂",  
               "入工","工","六","乂六","贝思","入士","思","一","毛?乂","δ亻乂","-亻乂","","",
               "亻工","亻工","亻工","亻六","亻思","亻一","亻一","彳乂","彳乂" ],
    "C-Key" : ["2.","3.","4.","#4.","5.","6.","#6.","7.","1","1","1","#1",  
               "2","2","3","4","#4","#4","5","6","#6","7","^1","#^1","#^1",
               "^2","^2","^2","^3","^5","^6","^6","^7","^7" ],
    "D-Key" : ["1.","2.","","3.","4.","5.","","6.","","","","7.",  
               "1","1","2","","3","3","4","5","","6","","7","7",
               "^1","^1","^1","^2","^4","^5","^5","^6","^6" ],
    "F-Key" : ["6_","7_","1.","","2.","3.","4.","#4.","5.","5.","5.","",  
               "6.","6.","7.","1","","","2","3","4","#4","5","","",
               "6","6","6","7","^2","^3","^3","#^4","#^4" ],
    "G-Key" : ["5.","6.","","7.","1","2","","3","4","4","4","#4",  
               "5","5","6","","7","7","^1","^2","","^3","^4","#^4","#^4",
               "^5","^5","^5","^6","^@1","^@2","^@2","^@3","^@3" ],
    "bB-Key": ["3.","#4.","5.","","6.","7.","1","","2","2","2","",  
               "3","3","#4","5","","","6","7","^1","","^2","","",
               "^3","^3","^3","#^4","^6","^7","^7","","" ],
    "pressBack": [2,2,2,2,2,2,2,2,0,0,0,0,  2,0,2,2,2,2,2,2,2,2,2,0,2,  0,0,0,2,2,0,0,2,2],
    "press1":    [2,2,2,2,2,2,0,0,2,2,2,0,  2,2,2,2,2,2,2,2,0,0,0,0,2,  0,2,0,2,0,0,0,2,2],
    "press2":    [2,2,2,2,2,0,2,0,2,2,2,0,  2,2,2,2,2,2,2,0,2,2,2,0,2,  2,2,2,0,2,2,2,0,0],
    "press3":    [2,2,2,2,0,0,0,0,0,2,0,0,  2,2,2,2,2,0,0,0,0,2,2,0,2,  2,0,1,0,2,0,0,2,2],
    "press4":    [2,2,0,0,0,0,2,0,0,0,0,0,  2,2,2,0,0,2,0,0,0,2,1,0,0,  0,0,0,0,0,0,0,2,2],
    "press5":    [2,0,2,0,0,0,2,0,0,2,2,0,  2,2,0,2,0,2,0,0,0,2,0,0,0,  0,0,0,2,2,2,0,2,0],
}



function fillCircle(mycanvas,r,type,fillColor) {
    var ctx = mycanvas.getContext("2d");
    ctx.fillStyle = fillColor;
    ctx.beginPath();                
    ctx.arc(r, r, r, 0, Math.PI * 1, true); // (x,y,r,sAngle,eAngle,counterclockwise)
    if (type === "0") {ctx.stroke()} else {ctx.fill()};
    ctx.beginPath();                 
    ctx.arc(r, r, r, 0, Math.PI * 2, true); 
    if (type === "2") {ctx.fill()} else {ctx.stroke()};
}

function processStr(myTdStr){
    clean_str = myTdStr.replace(/#/g, "").replace(/_/g, "").replace(/\./g, "").replace(/\^/g, "");
    pound_str = ""
    myTdStr.split('').forEach(function (value,index){
        if (value === "#") {pound_str = `<sup>#</sup>`;};
        if (value === "_") {clean_str = `<u>${clean_str}</u>.`;};    // 双下划标识  _  -->   _ .
        if (value === ".") {clean_str = `<u>${clean_str}</u>`;}      //   下划标识  .  -->   _
        if (value === "^") {clean_str = `<span style="text-decoration: overline">${clean_str}</span>`;};  //   上划标识  -   -->  -
    })
    return `${pound_str}${clean_str}`                                //  双上划标识@  -->  @-
}

function tdElementStr(myTdStr) {
    tempTdStr = `<td>${processStr(myTdStr)}</td>`;
    return tempTdStr
}

function tdCanvasStr(myTdStr,canvasClass) {  // "Circle" "firstCircle"
    tempTdStr = `<td><canvas class="${canvasClass}" width="16" height="16">${myTdStr}</canvas></td>`;
    return tempTdStr
}


function trElementStr (rowName,myArray,canvasClass) {
    tempTds = ``;
    tempTds += tdElementStr(rowName);
    if (canvasClass === "") {
        myArray.forEach(function (value,index) {tempTds += tdElementStr(value)});
    } else {
        myArray.forEach(function (value,index) {tempTds += tdCanvasStr(value,canvasClass)});
    };
    tempTrStr = `<tr>${tempTds}</tr>`;
    return tempTrStr;
}



function filterKeyIndex(fullTable,key){
    select_Idx = [];
    fullTable[key].forEach(
        (value,index) => {
            if (value !== "") {select_Idx.push(index)};
        }
    );
    return select_Idx;
}


function getValueByIndex(select_Idx,fullTable,word){
    select_Val = [];
    select_Idx.forEach(
        (Idx,_Index) => {
            select_Val.push(fullTable[word][Idx]);
        }
    );
    return select_Val;
}


function mainFunc(fullTable,key){
    document.getElementById('Current-Key').textContent = key;
    var select_Idx = filterKeyIndex(fullTable,key);
    var text_BlowType =  trElementStr("吹",getValueByIndex(select_Idx,fullTable,'BlowType'),"");
    var text_KeyName =   trElementStr("名",getValueByIndex(select_Idx,fullTable,'KeyName'),"");
    var text_Keynote =   trElementStr("简",getValueByIndex(select_Idx,fullTable,key),"");
    var text_pressBack = trElementStr("后",getValueByIndex(select_Idx,fullTable,'pressBack'),"firstCircle");
    var text_press1 = trElementStr("一",getValueByIndex(select_Idx,fullTable,'press1'),"Circle");
    var text_press2 = trElementStr("二",getValueByIndex(select_Idx,fullTable,'press2'),"Circle");
    var text_press3 = trElementStr("三",getValueByIndex(select_Idx,fullTable,'press3'),"Circle");
    var text_press4 = trElementStr("四",getValueByIndex(select_Idx,fullTable,'press4'),"Circle");
    var text_press5 = trElementStr("五",getValueByIndex(select_Idx,fullTable,'press5'),"Circle");

    document.getElementById("Key-Table").innerHTML = `${text_BlowType}${text_KeyName}${text_Keynote}${text_pressBack}${text_press1}${text_press2}${text_press3}${text_press4}${text_press5}`;
    
    canvasObjs = document.querySelectorAll('canvas.Circle');    // canvasObjs = document.getElementsByTagName('canvas')
    for (k=0;k<canvasObjs.length;k++) {
        fillCircle(canvasObjs[k],8,canvasObjs[k].textContent,'black');
    }
    canvasObjs = document.querySelectorAll('canvas.firstCircle');  
    for (k=0;k<canvasObjs.length;k++) {
        fillCircle(canvasObjs[k],8,canvasObjs[k].textContent,'gray');
    }
}


mainFunc(fullTable,"C-Key")

function myFunction(newKey) {
    mainFunc(fullTable,newKey);
}

</script>
    
    
    
    