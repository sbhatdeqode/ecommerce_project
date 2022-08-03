$(document).ready(function(){
	$("#loadMore").on('click',function(){
		var _currentProducts=$(".product-box").length;
		var _limit=$(this).attr('data-limit');
		var _total=$(this).attr('data-total');
		// Start Ajax
		$.ajax({
			url:'load_more_data',
			data:{
				limit:_limit,
				offset:_currentProducts
			},
			dataType:'json',
			beforeSend:function(){
				$("#loadMore").attr('disabled',true);
				$(".load-more-icon").addClass('fa-spin');
				
			},
			success:function(res){
				$("#filteredProducts").append(res.data);
				$("#loadMore").attr('disabled',false);
				$(".load-more-icon").removeClass('fa-spin');

				var _totalShowing=$(".product-box").length;
				if(_totalShowing==_total){
					$("#loadMore").remove();
				}
			}
		});
		// End
	});

	
	//publish-unpblish
	$(document).on('click',".publish-unpublish-product",function(){
		var _vm=$(this);
		var _index=_vm.attr('data-index');
		var _productId=$(".product-id-"+_index).val();

		let toastElement = document.getElementById("toast")
        let toastBody = document.getElementById("toast-body")
        let toast = new bootstrap.Toast(toastElement, { delay: 4000 })

		// Ajax
		$.ajax({
			url:'/shopuser/publish_unpublish',
			data:{
				'product_id':_productId,
		
			},
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
				console.log(_productId)
			},
			success:function(res){
				_vm.attr('disabled',false);
				$("#filteredProducts").html(res.data);
				toastBody.innerText = res.message
            	toast.show()
			}
		});
		// End
	});
	// End

	//delete product
	$(document).on('click',".delete-product",function(){
		var _vm=$(this);
		var _index=_vm.attr('data-index');
		var _productId=$(".product-id-"+_index).val();

		let toastElement = document.getElementById("toast")
        let toastBody = document.getElementById("toast-body")
        let toast = new bootstrap.Toast(toastElement, { delay: 4000 })

		// Ajax
		$.ajax({
			url:'/shopuser/product_delete',
			data:{
				'product_id':_productId,
		
			},
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
				console.log(_productId)
			},
			success:function(res){
				_vm.attr('disabled',false);
				$("#filteredProducts").html(res.data);
				toastBody.innerText = res.message
            	toast.show()
			}
		});
		// End
	});
	// End

	// Add wishlist
	$(document).on('click',".add-to-wishlist",function(){
		var _vm=$(this);
		var _index=_vm.attr('data-index');
		var _productId=$(".product-id-"+_index).val();

		let toastElement = document.getElementById("toast")
        let toastBody = document.getElementById("toast-body")
        let toast = new bootstrap.Toast(toastElement, { delay: 4000 })

		// Ajax
		$.ajax({
			url:'/products/add_to_wishlist',
			data:{
				'product_id':_productId,
		
			},
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
			},
			success:function(res){
				$(".wishlist-list").text(res.totalitems);
				_vm.attr('disabled',false);
				toastBody.innerText = res.message
            	toast.show()
			}
		});
		// End
	});
	// End


	// Delete item from wishlist
	$(document).on('click','.wishlist-delete-item',function(){
		var _pId=$(this).attr('data-item');
		var _vm=$(this);

		let toastElement = document.getElementById("toast")
        let toastBody = document.getElementById("toast-body")
        let toast = new bootstrap.Toast(toastElement, { delay: 4000 })
		// Ajax
		$.ajax({
			url:'/products/delete-from-wishlist',
			data:{
				'id':_pId,
			},
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
			},
			success:function(res){
				$(".wishlist-list").text(res.totalitems);
				_vm.attr('disabled',false);
				$("#wishList").html(res.data);

				toastBody.innerText = "Item successfully deleted"
            	toast.show()
			}
		});
		// End
	});


});
// End Document.Ready

