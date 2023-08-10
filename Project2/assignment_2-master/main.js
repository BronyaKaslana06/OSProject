//let allocMem;
let state=10;
let myList;
let stateType={
    'FIRST': 0,
    'BEST': 1,
}
class Node{
    constructor(pos,len,sta){
        this.position=pos;
        this.length=len;
        this.statement=sta;
        this.pre=null;
        this.next=null;
    }
}
class List{
    constructor(){
        this.head=new Node;
        this.tail=new Node;
        this.head.next=this.tail;
        this.tail.pre=this.head;
        this.head.pre=null;
        this.tail.next=null;
        this.size=0;
    }


    findNode=(pos)=>{//找到本位置的结点
        let temp=this.head.next;
        for(let i=1;i<pos;i++){
            temp=temp.next;
        }
        return temp;
    }

    findPos=(pos)=>{
        let temp=this.head.next;
        for(let i=1;i<=this.size;i++){
            if(temp.position===pos&&temp.statement===false){
                console.log("find to set free");
                return i;
            }
            temp=temp.next;
        }
        return 0;
    }

    insert=(pos,node)=>{//插在pos之后
        if(pos>this.size){//超出范围的话，加在最后
            let temp=this.tail.pre;
            temp.next=node;
            node.pre=temp;
            node.next=this.tail;
            this.tail.pre=node;
        }
        else{//插在pos之后
            let temp=this.findNode(pos);
            node.next=temp.next;
            temp.next.pre=node;
            temp.next=node;
            node.pre=temp;
        }
        this.size+=1;
        return;
    }

    addBack=(node)=>{//插在最后
        let temp=this.tail.pre;
        temp.next=node;
        node.pre=temp;
        node.next=this.tail;
        this.tail.pre=node;
        this.size+=1;
        return;
    }

    clear=()=>{
        let temp=this.head.next;
        let i=0;
        while(this.size!==0)
        {
            let temp1=temp.next;
            this.remove(temp);
            temp=temp1;
            this.size-=1;
        }
    }
    remove=(node)=>{
        let tempPre=node.pre;
        let tempNext=node.next;
        tempPre.next=tempNext;
        tempNext.pre=tempPre;
    }

    firstFit=(value)=>{
        //首次适应算法
        let temp=this.head.next;
        let i=0;
        for(i=1;i<=this.size;i++){
            if(temp.statement===true&&temp.length>=value){
                let pos=temp.position;
                let newtemp=new Node(pos,value,false);
                if(temp.length>value){
                    //Math.abs(lift.currentFloor - callFloor)
                    temp.position=pos + value;
                    temp.length=temp.length-value;
                    temp.pre.next=newtemp;
                    newtemp.pre=temp.pre;
                    newtemp.next=temp;
                    temp.pre=newtemp;
                    this.size+=1;
                    console.log("show:",this.size);
                }
                else if(temp.length===value){
                    temp.statement=false;
                }
                console.log("firstFit:",value);
                return;
            }
            temp=temp.next;
        }
        return alert("空间不足");
    }
    bestFit=(value)=>{
        let tempFit=new Node();
        tempFit=null;
        let temp=this.head.next;
        let i=0;
        for(i=1;i<=this.size;i++){
            if(temp.statement===true&&temp.length>=value){
                if(tempFit===null){
                    tempFit=temp;
                }
                else if(tempFit.length>temp.length){
                    tempFit=temp;
                }
            }
            temp=temp.next;
        }
        if(tempFit===null)
        return alert("空间不足");
        else{
            let pos=tempFit.position;
                let newtemp=new Node(pos,value,false);
                if(tempFit.length>value){
                    tempFit.position=pos+value;
                    tempFit.length=tempFit.length-value;
                    tempFit.pre.next=newtemp;
                    newtemp.pre=tempFit.pre;
                    newtemp.next=tempFit;
                    tempFit.pre=newtemp;
                    this.size+=1;
                    console.log("show:",this.size);
                }
                else if(tempFit.length===value){
                    tempFit.pre.next=newtemp;
                    newtemp.pre=tempFit.pre;
                    newtemp.next=tempFit.next;
                    tempFit.next.pre=newtemp;
                    this.remove(tempFit);
                }
                console.log("bestFit:",value);
                return;
        }
    }

    setFree=(i)=>{
        console.log("要释放哪个结点：",i);
        let temp=this.findNode(i);
        let tempPre=temp.pre;
        let tempNext=temp.next;
        if(tempPre.statement===true){
            tempPre.length+=temp.length;
            tempPre.next=tempNext;
            tempNext.pre=tempPre;
            temp=tempPre;
            this.size-=1;
        }
        if(tempNext.statement===true){
            temp.length+=tempNext.length;
            temp.next=tempNext.next;
            tempNext.next.pre=temp;
            temp.statement=true;
            this.size-=1;
        }
        temp.statement=true;
        return;
    }

    show=()=>{
        let i=0;
        for(i=1;i<64;i++){
            $("#memShow").children().eq(i).attr("class", "table-primary");
            $("#memShow").children().eq(i).text(" ");
        }
        console.log("show多少结点",this.size);
        let temp=this.head.next;
        let j=0;
        for(j=1;j<=this.size;j++){
            let pos=temp.position;
            let len=temp.length;
            let sta=temp.statement;
            if(sta){
                for(i=pos/10;i<=pos/10+len/10;i++){
                    $("#memShow").children().eq(i).attr("class", "table-info");//设置空闲颜色
                }
            }
            else if(sta===false){
                for(i=pos/10;i<=pos/10+len/10;i++){
                    $("#memShow").children().eq(i).attr("class", "table-warning");//设置占用颜色
                }
                
            }
            $("#memShow").children().eq(pos/10).text(pos);
            $("#memShow").children().eq(pos/10+len/10-1).text("|");//前后位置显示
            console.log("show",pos,len,sta);
            temp=temp.next;
        }
    }
   
}

initList=()=>{
    console.log("let's go!!");
    myList = new List;
    let node=new Node(0,640,true);
    myList.addBack(node);
    $("#best" ).attr("disabled", false);
    $("#first" ).attr("disabled", false);
    console.log("my list created!");
    myList.show();
}

setFirstFit=()=>{
    state=stateType['FIRST'];
    console.log("set type:first!");
    $("#best" ).attr("disabled", true);
    console.log("set disable:best!");
}
setBestFit=()=>{
    state=stateType['BEST'];
    console.log("set type:best!");
    $("#first" ).attr("disabled", true);
    console.log("set disable:first!");
}
resetFit=()=>{
    state=10;
    myList.clear();
    $("#best" ).attr("disabled", false);
    $("#first" ).attr("disabled", false);
    let node=new Node(0,640,true);
    myList.addBack(node);
    myList.show();
    console.log("reset function!");
}
allocate=(value)=>{
    //alert(value);
    //allocMem=value;
    if(state===stateType['FIRST']){
        myList.firstFit(value);
        myList.show();
        console.log("firstFit allocated!");
    }
    else if(state===stateType['BEST']){
        myList.bestFit(value);
        myList.show();
        console.log("bestFit allocated!");
    }
    else{
        alert("请设置分配方式!");
    }
}

setFree=(pos)=>{
    let i=myList.findPos(pos);
    if(i===0){
        return alert("不可释放！");
    }
    else{
        myList.setFree(i);
        myList.show();
        console.log("set free succeed!");
        return;
    }
}