$(document).ready(function(){
	bindEventos();
	$('#add').click(function() {
		return !$('#sall option:selected').remove().appendTo('#sowned');
	});
	$('#remove').click(function() {
		return !$('#sowned option:selected').remove().appendTo('#sall');
	});
	
	$("#bt_ok").click(function(){
		$("#sowned").append('<option value="'+$("#novoGrupo").val().toUpperCase()+'" selected="selected">'+ $("#novoGrupo").val().toUpperCase()+ '</option>');
		$('#novoGrupo').val('Crie um novo grupo');
		$('#novoGrupo').css('color','#ccc');
	});
	
	$("#bt_save").click(function(){
		grupos = Array()
		$('#sowned option').each(function(k, v){
			grupos[k] =  '"' + $(this).text() + '"';
		});
		params = '{"grupos":['+ grupos.join(",")+ '], "mail":"'+ $("#mail").val()+'"}';
		$.ajax({
		  type: 'POST',
		  url: '/adm/grupos/add',
		  data: {"json" : params},
		  success: function(response){
		  	Notifier.success('Grupos salvos com sucesso');
		  },
		  dataType: 'json',
		});
	});
	 
});

function bindEventos(){
	$('#novoGrupo').bind({
		focus : function(){
			if($(this).val() == 'Crie um novo grupo'){
				$(this).val('');
				$(this).css('color','#666');
			}
		},
		blur : function(){
			if($(this).val() == ''){
				$(this).val('Crie um novo grupo');
				$(this).css('color','#ccc');
			}
		}
	});
}