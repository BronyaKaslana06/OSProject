let state=-1;   //选择的排序算法的状态
let taskList;   //任务列表

let stateType={
    "FirstFit": 0,  //首次适应法
    "BestFit": 1,   //最佳适应算法
}

class Node{
    constructor(pos, len, st){
        this.startPos=pos;  //起点
        this.length=len;    //长度
        this.statu=st;   //占用情况，true:未被占用,false:被占用
        this.former=null;  //前一节点
        this.next=null; //下一节点
    }
}

class List{
    //构造一个头尾节点为空节点的列表
    constructor(){
        this.size=0;        //链表大小
        this.allocTimes=0;   //分配次数(块id)
        this.head=new Node; //头节点
        this.tail=new Node; //尾结点
        this.head.next=this.tail;  
        this.tail.former=this.head; //头尾节点相连
        this.head.former=null;
        this.tail.next=null;
    }

    //找到pos位置
    findNode=(pos)=>{
        let tempPtr=this.head.next;
        for(let i=1;i<pos;i++){
            tempPtr=tempPtr.next;
        }
        return tempPtr;
    }

    //按起点寻找，若返回0说明未找到或找到但未被占用不可释放
    findStartPosFree=(startPosition)=>{
        let tempPtr=this.head.next;
        for(let i=1;i<=this.size;i++){
            //找到且被占用
            if(tempPtr.startPos===startPosition && tempPtr.statu===false){
                console.log("找到且被占用");
                return i;
            }
            tempPtr=tempPtr.next;
        }
        return 0;
    }

    //尾插
    insertBack=(node)=>{
        let tempPtr=this.tail.former;
        tempPtr.next=node;
        node.former=tempPtr;
        node.next=this.tail;
        this.tail.former=node;
        this.size+=1;
    }

    //释放节点
    remove=(node)=>{
        node.former.next=node.next;
        node.next.former=node.former
        node=null;
        this.size-=1;
    }

    //清空重置链表
    clearList=()=>{
        let tempPtr=this.head.next;
        while(this.size!=0){
            let tempPtr2=tempPtr.next;
            this.remove(tempPtr);
            tempPtr=tempPtr2;
            //this.size-=1;
        }
    }

    //首次适应算法，参数:块大小
    firstFit=(blockSize)=>{
        console.log("调用首次适应算法分配内存,待分配内存块大小为",blockSize);
        let tempPtr=this.head.next;
        for(let i=1;i<=this.size;i++){
            if(tempPtr.statu===true && tempPtr.length>=blockSize){
                let startPosition=tempPtr.startPos;
                let newNode=new Node(startPosition,blockSize,false);
                if(tempPtr.length>blockSize){
                    tempPtr.startPos+=blockSize;
                    tempPtr.length-=blockSize;
                    //头插法
                    tempPtr.former.next=newNode;
                    newNode.former=tempPtr.former;
                    newNode.next=tempPtr;
                    tempPtr.former=newNode;
                    this.size+=1;
                    console.log("当前数目变为",this.size);
                }
                //若块的大小刚好能放下待申请的块，则不需申请新的节点，直接改变该节点的状态即可
                else if(tempPtr.length===blockSize){
                    tempPtr.statu=false;
                }
                document.getElementById("intro").textContent="新作业id为"+this.allocTimes+"，起始地址为："+newNode.startPos +"，大小为："+newNode.length;
                this.allocTimes+=1;
                console.log("首次适应算法插入块大小为",blockSize);
                return;
            }
            tempPtr=tempPtr.next;
        }
        //遍历全部空间后未找到一个合适的块
        alert("空间不足,请释放一部分空间");
        return;
    }

    //最佳适应算法
    bestFit=(blockSize)=>{
        let tempFitNode=new Node();   //暂时记录最适应块
        tempFitNode=null;
        let tempPtr=this.head.next;
        for(let i=1;i<=this.size;i++){
            if(tempPtr.statu===true && tempPtr.length>=blockSize){  //找到可以合适的块
                if(tempFitNode===null){    //第一次找到
                    tempFitNode=tempPtr;
                }
                else if(tempPtr.length<=tempFitNode.length){    //找到更小的合适的块
                    tempFitNode=tempPtr;
                }
            }
            tempPtr=tempPtr.next;
            /*if(tempPtr===null)
                break;*/
        }
        //未找到合适的块
        if(tempFitNode===null){
            alert("空间不足,请释放一部分空间");
            return;
        }
        //新建块
        if(tempFitNode.length>blockSize){   //最小长度大于块大小
            let newNode=new Node(tempFitNode.startPos,blockSize,false);
            tempFitNode.startPos+=blockSize;
            tempFitNode.length-=blockSize;
            tempFitNode.former.next=newNode;
            newNode.former=tempFitNode.former;
            newNode.next=tempFitNode;
            tempFitNode.former=newNode;
            this.size+=1;
            document.getElementById("intro").textContent="新作业id为"+this.allocTimes+"，起始地址为："+newNode.startPos +"，大小为："+newNode.length;
            this.allocTimes+=1;
        }
        else if(tempFitNode.length===blockSize){   //最小长度等于块大小
            tempFitNode.statu=false;
            document.getElementById("intro").textContent="新作业id为"+this.allocTimes+"，起始地址为："+tempFitNode.startPos +"，大小为："+tempFitNode.length;
            this.allocTimes+=1;
        }
        
        console.log("最佳适应算法插入块大小为",blockSize);
        return;
    }

    //释放节点
    FreeNode=(num)=>{
        console.log("释放第",num,"个节点")
        let tempNode=this.findNode(num);
        document.getElementById("intro").textContent="释放了起始地址为"+tempNode.startPos+"的内存空间";
        //前一个节点未被占用，可以释放
        if(tempNode.former.statu===true){
            tempNode.former.length+=tempNode.length;
            tempNode.former.next=tempNode.next;
            tempNode.next.former=tempNode.former;
            tempNode=tempNode.former;
            tempNode.statu=true;
            this.size-=1;
        }
        //后一个节点也未被占用，可以合并
        if(tempNode.next.statu===true){
            tempNode.length+=tempNode.next.length;
            tempNode.next=tempNode.next.next;
            tempNode.next.former=tempNode;
            tempNode.statu=true;
            this.size-=1;
        }
        tempNode.statu=true;
        return;
    }

    //更新界面显示
    renewInterface=()=>{
        //遍历现有的每一个色块
        for(let i=1;i<64;i++){
            $("#memShow").children().eq(i).attr("class", "table-primary");
            $("#memShow").children().eq(i).text(" ");
        }
        console.log("目前共划分了",this.size,"块");
        let tempPtr=this.head.next;
        for(let j=1;j<=this.size;j++){
            if(tempPtr.statu===true){
                //设置空闲颜色
                for(let k=tempPtr.startPos/10;k<=tempPtr.startPos/10+tempPtr.length/10;k++){
                    $("#memShow").children().eq(k).attr("class", "table-info");
                }
            }
            else if(tempPtr.statu===false){
                //设置占用颜色
                for(let cnt=tempPtr.startPos/10;cnt<=tempPtr.startPos/10+tempPtr.length/10;cnt++){
                    $("#memShow").children().eq(cnt).attr("class", "table-warning");
                }
            }
            $("#memShow").children().eq(tempPtr.startPos/10).text(tempPtr.startPos);
            $("#memShow").children().eq(tempPtr.startPos/10+tempPtr.length/10-1).text("|");//前后位置显示
            tempPtr=tempPtr.next;
            if(tempPtr===null){
                break;
            }
        }
        document.getElementById("textId").value="";
        document.getElementById("free").value="";
        console.log("更新显示");     
    }

}
//初始化列表
initList=()=>{
    console.log("运行开始");
    taskList=new List;
    let node=new Node(0,640,true);
    taskList.insertBack(node);
    //启用选择按钮
    $("#best").attr("disabled", false);
    $("#first").attr("disabled", false);
    console.log("创建任务列表");
    taskList.renewInterface();
}

//选择最先适配算法
chooseFirstFit=()=>{
    state=stateType['FirstFit'];
    alert("你选择了首次适应算法");
    $("#first" ).attr("disabled", true);
    $("#best" ).attr("disabled", true);
}

//选择最佳适应算法
chooseBestFit=()=>{
    state=stateType['BestFit'];
    alert("你选择了最佳适应算法");
    $("#first" ).attr("disabled", true);
    $("#best" ).attr("disabled", true);
}

//重置方法
resetMethod=()=>{
    state=-1;
    taskList.clearList();
    $("#best" ).attr("disabled", false);
    $("#first" ).attr("disabled", false);
    let node=new Node(0,640,true);
    taskList.insertBack(node);
    taskList.renewInterface();
    document.getElementById("intro").textContent="";
    taskList.allocTimes=0;
    console.log("已重置");
}

//申请空间
allocateBlock=(blockSize)=>{
    if(state===stateType['FirstFit']){
        taskList.firstFit(blockSize);
        taskList.renewInterface();
    }
    else if(state===stateType['BestFit']){
        taskList.bestFit(blockSize);
        taskList.renewInterface();
    }
    else{
        alert("请设置分配方式!");
    }
}

//释放空间
FreeBlock=(startPosition)=>{
    let i=taskList.findStartPosFree(startPosition);
    if(i===0){
        alert("不可释放！");
        return;
    }
    else{
        taskList.FreeNode(i);
        taskList.renewInterface();
        console.log("成功释放");
        return;
    }
}