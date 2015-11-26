$(document).ready(function(){
	
	$("#loginBtn").on("click",function(){
		
		var username = $("#inputUser").val();
		var password = $("#inputPwd").val();
		//alert("user:"+username+";pwd:"+password);
		LoginCheck(username,password);
	});
	

})


function LoginCheck(username,password)
{
	//alert("LoginCheck!\n");
	$.ajax({
		url:"/action/loginAction",
		//async: false, //if we want to lock the screen
		data:{
			"username":username,
			"password":password,
		},
		type:'POST',//action:post or get
		dataType:'json',
		beforeSend:function(){
			//alert("beforeSend!");
		},
		success:function(data){
			//do something here
			alert("login success!");
			window.location.href = "/main/"; //jump to main.html
				

		},
		error:function(xhr,type){
			
			$("#loginTips").show();
			
		}
	});
}

