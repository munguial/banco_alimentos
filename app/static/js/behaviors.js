
$(document).ready(
	function() 
	{ 							
		$("#filterBtn").click(function(){ $("#filterBox").toggle("slow","swing") } );
		$("#busquedaBtn").click(function(){ $("#leftMenu").show("slow","swing", function(){ $("#leftMenuMin").hide(); })  } );
		$("#collapse").click(function(){ $("#leftMenu").hide( function(){ $("#leftMenuMin").show("slow","swing"); }) } );
		$("#maximize").click(function(){ $("#leftMenu").show( function(){ $("#leftMenuMin").hide()  ; }) } );
	}									
)