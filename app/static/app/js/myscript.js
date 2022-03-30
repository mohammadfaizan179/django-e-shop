$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

$('.plus-cart').click(function(){
    var id = $(this).attr('pid').toString();
    var eml = this.parentNode.children[2]
    $.ajax({
        type : "GET",
        url : "/pluscart",
        data : {
            prod_id: id
        }, 
        success: function(data){
            console.log('success plus')
            console.log("Test : ", document.getElementById('quantity'));
            document.getElementById('quantity').innertText = data.quantity
            document.getElementById('amount').innertText = data.amount
            document.getElementById('totalamount').innertText = data.total_amount
            console.log(data)
        }
    })
})

$('.minus-cart').click(function(){
    var id = $(this).attr('pid').toString()
    var eml = this.parentNode.children[2]
    $.ajax({
        type : "GET",
        url : "/minuscart",
        data : {
            prod_id : id
        },
        success: function(data){
            eml.innertText = data.quantity
            document.getElementById('amount').innertText = amount
            document.getElementById('totalamount').innertText = total_amount
        }
    })
})

$('.remove-cart').click(function(){
    var id = $(this).attr('pid').toString()
    var eml = this
    console.log("id: ", id);
    $.ajax({    
        type : "GET",
        url : "/deletecart",
        data : {
            "prod_id" : id
        },
        success: function(data){
            console.log("Delete");
            document.getElementById('amount').innertText = data.amount
            document.getElementById('totalamount').innertText = data.total_amount
            eml.parentNode.parentNode.parentNode.parentNode.remove()
        }
    })
})