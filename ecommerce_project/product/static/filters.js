$(document).ready(function(){
	$(".ajaxLoader").hide();
	// Product Filter Start
	$(".filter-checkbox,#priceFilterBtn").on('click',function(){
		var _filterObj={};

		var select = document.getElementById("price");
		var value = select.value;
		_filterObj.price = value;
		
	
		$(".filter-checkbox").each(function(index,ele){
			var _filterVal=$(this).val();
			var _filterKey=$(this).data('filter');
			_filterObj[_filterKey]=Array.from(document.querySelectorAll('input[data-filter='+_filterKey+']:checked')).map(function(el){
			 	return el.value;
			});
		});

		// Run Ajax
		$.ajax({
			url:'product_filter',
			data:_filterObj,
			dataType:'json',
			beforeSend:function(){
				$(".ajaxLoader").show();
			},
			success:function(res){
				
				$("#filteredProducts").html(res.data);
				$(".ajaxLoader").hide();
			}
		});
	});
	// End

	// Filter Product According to the price
	$("#maxPrice").on('blur',function(){
		var _min=$(this).attr('min');
		var _max=$(this).attr('max');
		var _value=$(this).val();
		
		if(_value < parseInt(_min) || _value > parseInt(_max)){
			alert('Values should be '+_min+'-'+_max);
			$(this).val(_min);
			$(this).focus();
			$("#rangeInput").val(_min);
			return false;
		}
	});
	// End
});