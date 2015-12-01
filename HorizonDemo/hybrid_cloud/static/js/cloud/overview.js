$(document).ready(function(){
	//get endpoint
	var endpoint = $("#id_region").val();
	getOverview(endpoint);
})


function getOverview(endpoint)
{
    var myname=new Array();
    myname[0]="instance";
    myname[1]="core";
    myname[2]="ram";
    myname[3]="floatingIP";
    myname[4]="volume";
	$.ajax({
		url:"/action/overviewAction",
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
				if("usages" == name){
					$.each(value,function(i,usage){
						//alert(i+":"+usage["name"]+";"+usage["id"]+";"+usage["vcpus"]+";"+usage["disk"]+";"+usage["createTime"]+";"+usage["ram"]);
						var tmpTr = "";
						tmpTr += "<tr  bgcolor=\"#F5F5F5\">";
						tmpTr += "<td><p><a href=\"/detail/?id="+usage["id"]+"&endpoint="+endpoint+"\">"+usage["name"]+"</a></p></td>";
						tmpTr += "<td><p>"+usage["vcpus"]+"</p></td>";
						tmpTr += "<td><p>"+usage["disk"]+"GB</p></td>";
						tmpTr += "<td><p>"+usage["ram"]+"MB</p></td>";
						tmpTr += "<td><p>"+usage["createTime"]+"</p></td>";
                  		tmpTr += "</tr>"
                  $("#id_table_usage").append(tmpTr);
                
					});
				}
				else if("limits" == name){
				    $.each(value,function(j,limit){
						//alert(i+":"+usage["name"]+";"+usage["id"]+";"+usage["vcpus"]+";"+usage["disk"]+";"+usage["createTime"]+";"+usage["ram"]);

						//alert(j);
					    circle('#container'+(j+1),limit,myname[j]);

					});
				}			
			}				
			);
		},
		error:function(xhr,type){
			alert("fail to get overview!");
		}
	});
}

