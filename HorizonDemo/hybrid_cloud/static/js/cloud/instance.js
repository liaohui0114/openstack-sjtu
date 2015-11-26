$(document).ready(function(){
	$("#id_create_instance").on("click",function(){
		alert("create instance!");
		//do something here
	});
});

//protocol: protocol type;1.TCP;2.UDP;3.ICMP;
//startIp:ip of startNode
//endIp:ip of endNode
//startNodeName:name of start node
//endNodeName:name of end node
function createInstance()
{
	//alert("Udp_ajax_post_single!\n");
	$.ajax({
		url:"/action/createInstanceAction",
		//async: false, //if we want to lock the screen
		data:{
			"startNodeIp":startIp,
			
			//form:$("#id_form_node").serialize()  //using & to connetion,style:startNode=192.168.1.152&endNode=192.168.1.152
		},
		type:'POST',//action:post or get
		dataType:'json',
		beforeSend:function(){
			//alert("beforeSend!");
		},
		success:function(data){
			//success

		},
		error:function(xhr,type){
			
			//alert("fail!");
		}
	});
}

