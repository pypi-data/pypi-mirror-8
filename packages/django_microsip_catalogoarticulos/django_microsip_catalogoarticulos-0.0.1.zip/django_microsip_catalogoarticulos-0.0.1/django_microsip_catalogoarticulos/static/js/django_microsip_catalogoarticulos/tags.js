$(document).ready(function() {
	
	$("#agregar_tag_articulo").on("click", agregar_tag_articulo);
	$(".tag1").on("click", eliminar_tag_articulo);
	
	function agregar_tag_articulo(){

		if ( $("#id_tag").val() != null ) {
			// debugger;
			$("#id_tag-deck").hide();
			$("#id_tag_text").show();
			$.ajax({
		 	   	url:'/catalogo/agregar_tag_articulo/',
		 	   	type : 'get',
		 	   	data : {'tag_id':parseInt($("#id_tag").val()[0]),
		 	   			'articulo_id':parseInt($("#id_art").val()),
		 	   			},
		 	   	success: function(data){
		 	   		//alert(data.tag_id + "" + data.articulo_id);
		 	   		$(".tags").append("<div class='tag1'><span style='color:white;'>"+data.tag_name+"</span><i class='glyphicon glyphicon-remove borrar'></i><input type='hidden' value="+data.tagarticulo+" class='hidden_tag'/></div>");
		 	   		$(".tag1").on("click", eliminar_tag_articulo);
		 	   		
				},
			});
		}
		else{
			alert("Selecciona Un Tag Existente por Favor.");			
		};
	}


	function eliminar_tag_articulo(){	
		// debugger;
		var tag_id = parseInt($(this).find("input")[0].value);
		var tag_name = $(this).find("span").text();
		$(this).remove();

		$.ajax({
	 	   	url:'/catalogo/eliminar_tag_articulo/',
	 	   	type : 'get',
	 	   	data : { 'tag_id':tag_id,
	 	   			 'tag_name':tag_name,
	 	   			 'articulo_id':parseInt($("#id_art").val()),
	 	   		 	   			},
	 	   	success: function(data){
	 	   		//alert(data.tag_id + "" + data.articulo_id);
	 	   		$(this).remove();
			},
		});
	}
});