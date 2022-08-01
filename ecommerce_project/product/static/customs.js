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

	
	// Add to cart
	$(document).on('click',".add-to-cart",function(){
		var _vm=$(this);
		var _index=_vm.attr('data-index');
		var _productId=$(".product-id-"+_index).val();

		let toastElement = document.getElementById("toast")
        let toastBody = document.getElementById("toast-body")
        let toast = new bootstrap.Toast(toastElement, { delay: 4000 })

		// Ajax
		$.ajax({
			url:'/products/add_to_cart',
			data:{
				'product_id':_productId,
		
			},
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
			},
			success:function(res){
				$(".cart-list").text(res.totalitems);
				_vm.attr('disabled',false);
				toastBody.innerText = res.message
            	toast.show()
			}
		});
		// End
	});
	// End

	// Delete item from cart
	$(document).on('click','.delete-item',function(){
		var _pId=$(this).attr('data-item');
		var _vm=$(this);

		let toastElement = document.getElementById("toast")
        let toastBody = document.getElementById("toast-body")
        let toast = new bootstrap.Toast(toastElement, { delay: 4000 })
		// Ajax
		$.ajax({
			url:'/products/delete-from-cart',
			data:{
				'id':_pId,
			},
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
			},
			success:function(res){
				$(".cart-list").text(res.totalitems);
				_vm.attr('disabled',false);
				$("#cartList").html(res.data);

				toastBody.innerText = "Item deleted from cart"
            	toast.show()
			}
		});
		// End
	});


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

