$(document).ready(function(){
	$("#id_create_instance").on("click",function(){
		alert("create instance!");
		var name = document.getElementById('instance_name').value;
		var instance_type = document.getElementById('instance_type').value;
		//alert(name);
		createInstance(name,instance_type);
		//do something here
	});
});


function createInstance()
{
	//alert("Udp_ajax_post_single!\n");
	$.ajax({
		url:"/action/createInstanceAction",
		//async: false, //if we want to lock the screen
		data:{
			"name": arguments[0],
			"type": arguments[1],
			//form:$("#id_form_node").serialize()  //using & to connetion,style:startNode=192.168.1.152&endNode=192.168.1.152
		},
		type:'POST',//action:post or get
		dataType:'json',
		beforeSend:function(){
			//alert("beforeSend!");
		},
		success:function(data){
			//success
			alert("succeed");

		},
		error:function(xhr,type){
			
			alert("fail");
		}
	});
}

