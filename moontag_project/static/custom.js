// This is for the product variation
$(document).ready(function(){
    $(".choose-size").hide();
    
    // Show the size after click the color
    $(".choose-color").on('click',function(){
        $(".choose-size").removeClass('active'); // for remove when i have couple of sizes attribute and dont be two active of them
        $(".choose-color").removeClass('focused'); //to remove the active when i choose something else
        $(this).addClass('focused');
        var _color=$(this).attr('data-color');
        $(".choose-size").hide();
        $(".color"+_color).show();
        $(".color"+_color).first().addClass('active'); // Becuase that show me two first attribute i need this

        var _price=$(".color"+_color).first().attr('data-price');
        $(".product-price").text(_price);
    });

    // Price according to size
    $(".choose-size").on('click',function(){
        $(".choose-size").removeClass('active'); //to remove the active when i choose something else
        $(this).addClass('active');
        

        var _price=$(this).attr('data-price');
        $(".product-price").text(_price); //here
        
    });

    // For show the first size of the first attribuse for dont be blank in the sizes collum, and if the product have obly one attribute she will auto selected.
    $(".choose-color").first().addClass('focused');
    var _color=$(".choose-color").first().attr('data-color');
    var _price=$(".choose-size").first().attr('data-price'); //Fech the price if only one size to the attribute

    $(".color"+_color).show();
    $(".color"+_color).first().addClass('active');
    $(".product-price").text(_price); // here its active the fech of the price if only one size for the product

    // Add to cart - for get the price,color,size i need help of java script 
    $(document).on('click',".add-to-cart",function(){
		var _vm=$(this);
		var _index=_vm.attr('data-index');
		var _qty=$(".product-qty-"+_index).val();
		var _productId=$(".product-id-"+_index).val();
		var _productImage=$(".product-img-"+_index).val();
		var _productTitle=$(".product-title-"+_index).val();
		var _productPrice=$(".product-price-"+_index).text();
        // Help of Ajax for send the request 
        $.ajax({
			url:'/add-to-cart',
			data:{
                'id':_productId,
                'img':_productImage,
                'qty':_qty,
                'title':_productTitle,
                'price':_productPrice
            },
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
			},
			success:function(res){
                $(".cart-list").text(res.total_items);
				_vm.attr('disabled',false);
			}
		});
    });
    //delete items from the cart in the cart page
    $(document).on('click','.delete-item',function(){
        var _pId=$(this).attr('data-item');
        var _vm = $(this);

        $.ajax({
			url:'/delete-from-cart',
			data:{
                'id':_pId,
            },
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
			},
			success:function(res){
                $(".cart-list").text(res.total_items);
				_vm.attr('disabled',false);
                $("#cart_page").html(res.data);
			}
		});
    });

    //Update items from the cart in the cart page
    $(document).on('click','.update-item',function(){
        _pId=$(this).attr('data-item');
        _pQty=$(".product-qty-"+_pId).val();
        var _vm = $(this);

        $.ajax({
			url:'/update-cart',
			data:{
                'id':_pId,
                'qty':_pQty,
            },
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
			},
			success:function(res){
                // $(".cart-list").text(res.total_items);
				_vm.attr('disabled',false);
                $("#cart_page").html(res.data);
			}
		});
    });

});