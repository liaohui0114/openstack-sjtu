$(document).ready(function(){
	//get endpoint
	//alert('hello');
	//var v = $("#details_list").find("tr").eq(1).find("td").eq(0).html();
	//alert(v);
	var endpoint = "http://192.168.1.123:5000/v2.0";
	getInstanceDetail("cloud1");
	getInstanceDetail("cloud2");

})

function getInstanceDetail(cloudName)
{
	$.ajax({
		url:"/action/instanceDetailAction",
		//async: false, //if we want to lock the screen
		data:{
			"url":"http://192.168.1.1:5000/v2.0",
			"cloud":cloudName
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

						tmpTr += "<td style=\"display:none\">"+detail["id"]+"</td>"
						tmpTr += "<td><p>"+cloudName+"</p></td>";


						//tmpTr += "<td><p>"+detail["name"]+"</p></td>";
						tmpTr += "<td><p><a href=\"/detail/?id="+detail["id"]+"&cloud="+cloudName+"\">"+detail["name"]+"</a></p></td>";
						
						tmpTr += "<td><p>"+detail["image"]+"</p></td>";
						tmpTr += "<td><p>"+detail["address"]+"</p></td>";
						tmpTr += "<td><p>"+detail["flavor"]+"</p></td>";
						tmpTr += "<td><p>"+detail["status"]+"</p></td>";
						tmpTr += "<td><p>"+detail["availability_zone"]+"</p></td>";
						tmpTr += "<td><p>"+detail["power_state"]+"</p></td>";
						tmpTr += "<td><p>"+detail["created"]+"</p></td>";
						tmpTr += "<td><select class= \"dfinput2\" onchange=\"instanceAction(this)\" >\
						                <option value =\"floatingip\">Associate Floating IP</option>\
						                <option value =\"start\">Start</option>\
						                <option value =\"stop\">Stop</option>\
						                <option value =\"terminate\">Terminate</option>\
						                </select></td>";
                  		tmpTr += "</tr>";
                  		$("#details_list").append(tmpTr);
                
					});
					
					//var tmpTr1 = "";
                    //tmpTr1 += "<tr style=\"width: 100%\" bgcolor=\"#FCFCFC\">";
                    //tmpTr1 += "<td colspan=\"11\"></td>";
                    //tmpTr1 += "</tr>";
                    //$("#details_list").append(tmpTr1);

				}			
			}				
			);
		},
		error:function(xhr,type){
			//alert("fail to get overview!");
		}
	});
}
/*
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

						tmpTr += "<td style=\"display:none\">"+detail["id"]+"</td>"
						tmpTr += "<td><p>"+couldName"+</p></td>";


						tmpTr += "<td><p>"+detail["name"]+"</p></td>";
						tmpTr += "<td><p>"+detail["image"]+"</p></td>";
						tmpTr += "<td><p>"+detail["address"]+"</p></td>";
						tmpTr += "<td><p>"+detail["flavor"]+"</p></td>";
						tmpTr += "<td><p>"+detail["status"]+"</p></td>";
						tmpTr += "<td><p>"+detail["availability_zone"]+"</p></td>";
						tmpTr += "<td><p>"+detail["power_state"]+"</p></td>";
						tmpTr += "<td><p>"+detail["created"]+"</p></td>";
						tmpTr += "<td></td>";
                  		tmpTr += "</tr>";
                  $("#details_list").append(tmpTr);
                
					});
					var tmpTr1 = "";
                    tmpTr1 += "<tr style=\"width: 100%\" bgcolor=\"#FCFCFC\">";
                    tmpTr1 += "<td colspan=\"10\"></td>";
                    tmpTr1 += "</tr>";
                    $("#details_list").append(tmpTr1);

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
*/
function instanceAction(obj){
	//alert("instanceAction changed!");
	var action = obj.value;//$(obj).val()
	var instanceId = $(obj).parent().parent().find("td").eq(1).html();
	var cloudName = $(obj).parent().parent().find("td").eq(2).find("p").html();
	//alert("action:"+action+";instanceId:"+instanceId+";cloudName:"+cloudName);
	/*
	switch(action){
		case "addfloatingip":
			alert("addfloatingip");
			//do something about associate floating ips here!
			break;
		case "start":
			alert("start");
			break;
		case "stop":
			alert("stop");
			break;
		case "terminate":
			alert("terminate");
			break;
	}
	*/
	$.ajax({
		url:"/action/instanceActionsAction",
		//async: false, //if we want to lock the screen
		data:{
			"cloud":cloudName,
			"actions":action,
			"serverid":instanceId,
		},
		type:'POST',//action:post or get
		dataType:'json',
		beforeSend:function(){
			//alert("beforeSend!");
		},
		success:function(data){
			//success
			alert("successed!");
			location.reload(); //F5,refresh
		},
		error:function(xhr,type){
			//do nothing
			alert("status is already exist!");
		}
	});
}