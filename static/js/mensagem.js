$(document).ready(function(){
	$("#bsend").click(function(){
		para = $("#para").val()
		
		if(para == '' || para == null){
			Notifier.error('Informe o destinatário!');
			return false;
		}
		
		msg = escape($("#msg").val())
		params = '{"from":"' + $("#from").val() +'","user":"'+ $("#para").val() +'", "tipo":"talk", "message":"' + msg +'"}'
		console.warn(params)
		$.ajax({
		  type: 'POST',
		  url: '/adm/mensagem/send',
		  data: {"json" : params},
		  success: function(response){
		  	if(response.success){
		  		Notifier.success('Mensagem enviada com sucesso');
		  		$("#para").val('');
		  		$("#msg").val('');
		  	}else{
		  		Notifier.error(response.msg);
		  	}
		  },
		  dataType: 'json',
		});
	});	
});