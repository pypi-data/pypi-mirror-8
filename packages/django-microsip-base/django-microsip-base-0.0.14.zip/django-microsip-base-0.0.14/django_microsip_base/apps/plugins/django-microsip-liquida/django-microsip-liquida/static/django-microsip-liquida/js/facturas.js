$(document).ready(function() {
	$("input[name='facturas_all']").on("click", sellect_all);
	function sellect_all(){
		seleccionar = this.checked;

		$("input[type='checkbox'][name='facturas']").each(function(){
			this.checked = seleccionar;
		});
	}
	$("#descargar_facturas_btn").on("click", descargar_facturas);

	var progress = 0;
	var cliente_no_existe = ""
	var documento_ya_existe = ""
	var consecutivo_folio_no_definido = ""

	function descargar_facturas(){
		$.ajax({
	 	   	url:'/enlace_liquida/descargar_facturas/',
	 	   	type : 'get',
	 	   	success: function(data){
	 	   		if (data.errors == ""){
	 	   			if (data.cliente_no_existe != "")
	 	   				cliente_no_existe = cliente_no_existe + ", "+data.cliente_no_existe;
	 	   			
	 	   			if (data.documento_ya_existe != "")
	 	   				documento_ya_existe = documento_ya_existe + ", "+data.documento_ya_existe;
	 	   			
	 	   			if (data.consecutivo_folio_no_definido != "")
	 	   				consecutivo_folio_no_definido = consecutivo_folio_no_definido + ", "+data.consecutivo_folio_no_definido;

		 	   		progress = data.progress;
		 	   		$("#progress-bar-unique").attr("aria-valuenow",progress);
		 	   		$("#progress-bar-unique").attr("style","width:"+progress+"%;");
		 	   		$("#progress-bar-unique").text(progress+"%, Factura de "+data.basedatos_no+ " generada.");
					if (progress < 100)
			 	   		descargar_facturas();
			 	   	else
			 	   	{
			 	   		var msg = "Facturas generadas."
			 	   		if (cliente_no_existe != "")
			 	   			msg = msg + "\n  Cliente no existe en \n["+ cliente_no_existe +"]";
			 	   		if (documento_ya_existe != "")
			 	   			msg = msg + "\n  Documento ya generado en \n["+ documento_ya_existe +"]";
			 	   		if (consecutivo_folio_no_definido != "")
			 	   			msg = msg + "\n  Consecutivo no definido en \n["+ consecutivo_folio_no_definido +"]";

						alert(msg);
			 	   		window.location.href="/enlace_liquida/";
			 	   	}
	 	   		}
	 	   		else
	 	   			alert(data.errors);
	 	   	},	
	 	});	
	}

	$("#certificar_facturas_btn").on("click", certificar_facturas_ajax);
	var factura_selecionadas_obj = [];
	var factura_certificar_indice = 0;
	var errores = "";
	var ids = "";
	var ind= 0;
	function certificar_facturas_ajax(){
		progress = 0;
   		errores = "";
		factura_selecionadas_obj  = $("input:checked[name='facturas']");
		valor_split = factura_selecionadas_obj[0].value.split(";");
		using = valor_split[0];
		factura_id = valor_split[1];
		var msg = "Proceso Completado.\n";
		var facturas_certificadas="";
		var proceso_completado=false;

		$( "input:checked[name='facturas']" ).each(function( index ) {
			valor_split = this.value.split(";");
			using = valor_split[0];
			factura_id = valor_split[1];
			$.ajax({
		 	   	url:'/enlace_liquida/certificar_factura/',
		 	   	type : 'get',
		 		data: {'factura_id':factura_id, 'using':using, },
		 	   	success: function(data){
		 	   		progress = (index+1) * 100 / factura_selecionadas_obj.length;
		 	   		progress=progress.toFixed(2);
		 	   		if (data.errors!= "")
			   			errores = errores + data.errors+"\n";
			   		else{
			   			facturas_certificadas = facturas_certificadas + using +",";	
			   		}
			   				
			   		if (progress < 100){
						$("#progress-bar-unique").attr("aria-valuenow",progress);
				   		$("#progress-bar-unique").attr("style","width:"+progress+"%;");
				   		$("#progress-bar-unique").text(progress+"%, Certificando factura de "+using+ ".");
			   		}else{
			   			progress = 100;
			   			msg = msg + errores+"\n";
			   			$("#progress-bar-unique").attr("aria-valuenow",progress);
			   			$("#progress-bar-unique").attr("style","width:"+progress+"%;");
			   			$("#progress-bar-unique").text(progress+"%, Base de datos ");
			   			alert(msg+facturas_certificadas);
			   			window.location.href="/enlace_liquida/";
			   		}
				},
				error: function (request, status, error) {
     			   	errores=errores+using;
     			   	progress = (index+1) * 100 / factura_selecionadas_obj.length;
     			   	progress=progress.toFixed(2);
					if (progress < 100){
						$("#progress-bar-unique").attr("aria-valuenow",progress);
				   		$("#progress-bar-unique").attr("style","width:"+progress+"%;");
				   		$("#progress-bar-unique").text(progress+"%, Certificando factura de "+using+ ".");
			   		}
			   		else{
			   			progress = 100;
			   			msg = msg + errores+"\n";
			   			$("#progress-bar-unique").attr("aria-valuenow",progress);
			   			$("#progress-bar-unique").attr("style","width:"+progress+"%;");
			   			$("#progress-bar-unique").text(progress+"%, Base de datos ");
			   			alert(msg+facturas_certificadas);
			   			window.location.href="/enlace_liquida/";
			   		}
    			}
			});

		});
		
		

		

	}


});



