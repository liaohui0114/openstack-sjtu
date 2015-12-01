$(document).ready(function(){
	//get endpoint
	//alert('hello');
	var endpoint = "http://192.168.1.164:5000/v2.0";
	getInstanceDetail(endpoint);
})


function getInstanceDetail(endpoint)
{
	$.ajax({
		url:"/action/instanceDetailAction",
		//async: false, //if we want to lock the screen
		data:{
			"url":endpoint,
			
			//form:$("#id_form_node").serialize()  //using & to connetion,style:startNode=192.168.1.152&endNode=192.168.1.152
		},
		type:'POST',//action:post or get
		dataType:'json',
		beforeSend:function(){
			//alert("beforeSend!");
		},
		success:function(data){
			//success
			//alert("get overview success");
			//do something here with data
			$.each(data,function(name,value){
				//alert("name="+name);				
				if("details" == name){
					$.each(value,function(i,detail){
						//alert(i+":"+usage["name"]+";"+usage["id"]+";"+usage["vcpus"]+";"+usage["disk"]+";"+usage["createTime"]+";"+usage["ram"]);
						var tmpTr = "";
						tmpTr += "<tr style=\"width: 100%\" bgcolor=\"#FCFCFC\">";
						tmpTr += "<td><input type=\"checkbox\"></td>";
						tmpTr += "<td><p>"+detail["name"]+"</p></td>";
						tmpTr += "<td><p>"+detail["image"]+"</p></td>";
						tmpTr += "<td><p>"+detail["address"]+"</p></td>";
						tmpTr += "<td></td>";
						tmpTr += "<td><p>"+detail["status"]+"</p></td>";
						tmpTr += "<td><p>"+detail["availability_zone"]+"</p></td>";
						tmpTr += "<td><p>"+detail["power_state"]+"</p></td>";
						tmpTr += "<td><p>"+detail["created"]+"</p></td>";
						tmpTr += "<td></td>";
                  		tmpTr += "</tr>"
                  $("#details_list").append(tmpTr);
                
					});
				}
				// else if("limits" == name){
				// 	//do something here
				// }			
			}				
			);
		},
		error:function(xhr,type){
			//alert("fail to get overview!");
		}
	});
}

