$(document).ready(function(){
    $("#quick_view , #quick_view_2").on('click','.open_view',function(){
        console.log("Hello there");
        // product id
        let id = $(this).attr('data-sid');
        let store_username = $(this).attr('data-sname');
        console.log(id);
        console.log(store_username);
        
        // hide the modal data
        $('#modalContent').hide();
        $('#modalSpinner').show();

        mydata={'store_username': store_username,'product_id':id}
        mythis=this;
        //

        //ajax request
        $.ajax({
            url:"{% url 'vendors:api_store_product_detail' %}",
            type:'GET',
            data:mydata,
            success:function(data){
                // converts string of json to object
                data = JSON.parse(data);
                console.log(data);

                if(data.status == '200'){
                    // show modal data place after successfully data get 
                    $('#modalContent').show();
                    $('#modalSpinner').hide();

                    //add data to html fields
                    $('#modalTitle').append(data.title);
                    $('#pro-1').html('<img src="'+ data.image+ '" alt="image Loading "/>');
                    $('#description').text(data.description);

                    $('#takaicon').html('<img id="takaicon" class="taka-icon" src="/static/favicon_io/taka-gold.svg" alt="img..." /> <span id="sup-price">'+data.sup_price+'</span> ');
                    $('#takaicon2').html('<img id="takaicon2" class="taka-icon" src="/static/favicon_io/taka-gold.svg" alt="img..." /> <span id="sup-price">'+data.selling_price+'</span> ');
                    

                    //modal button for rediect
                    $('#update-id').on('click', function(){
                        console.log("update id clicked");
                        let aval=$('#update-id').attr("href");

                        var Obj={
                            0: store_username, 
                            1: id, 
                        }
                        var url = "{% url 'vendors:store_product_update' store_username=0 product_id=1 %}";
                        
                        //replace
                        var urlLink = url.replace(/0|1/gi, function(matched){ 
                            return Obj[matched]; 
                        }); 
                        console.log(urlLink);
                        $(this).attr("href",urlLink)
                    });

                    //add product modal button
                    $('#addproduct-id').on('click', function(){
                        console.log("add product id clicked");
                        var url = "{% url 'vendors:store_product_add' store_username=0  %}".replace('0',store_username);
                        $(this).attr("href",url)
                    });

                    $('#removeproduct-id').on('click', function(){
                        console.log("remove id clicked");
                        var Obj={
                            0: store_username, 
                            1: id, 
                        }
                        var url = "{% url 'vendors:store_product_remove' store_username=0 product_id=1 %}";
                        
                        //replace
                        var urlLink = url.replace(/0|1/gi, function(matched){ 
                            return Obj[matched]; 
                        }); 
                        console.log(urlLink);
                        $(this).attr("href",urlLink)
                    });
                }
                else if(data.status=='404'){
                    $('#modalContent').show();
                    $('#modalContent').html('<h1>Please Reload!</h1>');
                    $('#modalSpinner').hide();
                }
                
            }
        })
    })
    

    //function that preview confirm
    function Alert(){
        alert("Are You Sure Delete The Product!");
    }

    // store open and close 
    $("#open-id").click(function(e){
        e.preventDefault();
        //get csrf token
        let csrf = $("input[name=csrfmiddlewaretoken]").val();
        
        console.log("store name : "+csrf)
        
        if($("#open-btn-text").text() == "open"){
            console.log("open clicked")
            
            
            let store_username = $("#openClose-input").attr("data-store");
            data={store_username:store_username,curr_state:'open',csrfmiddlewaretoken:csrf}
            
            $.ajax({
                url:"{% url 'vendors:api_store_status_update' %}",
                method:'POST',
                data,
                success:function(data){
                    data = JSON.parse(data)
                    console.log(data)
                    if(data.status == '200'){
                        //remove btn
                        $("#open-id").fadeOut(200);
                        setTimeout(function(){
                            // add css
                            $("#open-id").removeClass('open-btn').addClass("close-btn");
                            $("#open-id").removeAttr("style");
                            //change opacity
                            $(".close-btn").css({'opacity': '1 !important'});

                            //disappear loading
                            $("#open-btn-loading").removeClass("openbtn-loading-open").addClass("openbtn-loading-close");
                            $("#open-btn-text").attr("id","close-btn-text")
                            //add OPEN text to CLOSE text
                            $("#close-btn-text").append("close");

                        },300)
                        
                        $("#open-id").animate({ opacity: 1 });
                        $("#open-id").removeAttr("style");
                        //show messages
                        $("#msg").show()
                        $("#msg").prepend("<div id='message' class='container' style='position: absolute;z-index: 100;margin: -66px 0px;text-align: center; padding:0px 80px;'><div class='alert alert-danger alert-dismissible' role='alert'></button>"+data.msg+"</div></div>");
                        setTimeout(function(){
                            $("#msg").hide()
                        },3000);
                    }
                    else{
                        $("#msg").show()
                        $("#msg").prepend("<div id='message' class='container' style='position: absolute;z-index: 100;margin: -66px 0px;text-align: center; padding:0px 80px;'><div class='alert alert-danger alert-dismissible' role='alert'></button>"+data.msg+"</div></div>");
                        setTimeout(function(){
                            $("#msg").hide()
                        },3000)
                    }
                    
                },
                error: function (jqXHR, exception) {
                    console.log("hello error?")

                    var msg = '';
                    if (jqXHR.status === 0) {
                        msg = 'Not connect.\n Verify Network.';
                    } else if (jqXHR.status == 404) {
                        msg = 'Requested page not found. [404]';
                    } else if (jqXHR.status == 500) {
                        msg = 'Internal Server Error [500].';
                    } else if (exception === 'parsererror') {
                        msg = 'Requested JSON parse failed.';
                    } else if (exception === 'timeout') {
                        msg = 'Time out error.';
                    } else if (exception === 'abort') {
                        msg = 'Ajax request aborted.';
                    } else {
                        msg = 'Uncaught Error.\n' + jqXHR.responseText;
                    }
                    //
                    $("#open-btn-loading").removeClass("openbtn-loading-open").addClass("openbtn-loading-close");
                    $("#open-btn-text").append('open');
                    $('#open-id').animate({opacity:1})

                    
                    //show error message
                    $("#msg1").show();
                    $("#msg1").prepend("<div id='message' class='container' style='position: absolute;z-index: 100;margin: -66px 0px;text-align: center; padding:0px 80px;'><div class='alert alert-danger alert-dismissible' role='alert'></button>"+msg+"</div></div>");
                    setTimeout(function(){
                        $("#msg1").hide();
                    },2500);
                },
            })

            // let's work with css and btn
            $("#open-btn-text").empty();
            $("#open-btn-loading").removeClass("openbtn-loading-close").addClass("openbtn-loading-open");
            $(".open-btn").css({"opacity":'.5 '})

            
        }
        else if($("#close-btn-text").text() == "close" ){
            console.log("close clicked")

            let store_username = $("#openClose-input").attr("data-store");
            data={store_username:store_username,curr_state:'close',csrfmiddlewaretoken:csrf}
            $.ajax({
                url:"{% url 'vendors:api_store_status_update' %}",
                method:'POST',
                data,
                success:function(data){
                    data = JSON.parse(data)
                    console.log(data);
                    if(data.status == '200'){
                        //
                        //remove btn
                        $("#open-id").fadeOut(200);
                        setTimeout(function(){
                            // add css
                            $("#open-id").removeClass('close-btn').addClass("open-btn");
                            $("#open-id").removeAttr("style");
                            //change opacity
                            $(".open-btn").css({'opacity': '1 !important'});

                            //disappear loading
                            $("#open-btn-loading").removeClass("openbtn-loading-open").addClass("openbtn-loading-close");
                            $("#close-btn-text").attr("id","open-btn-text");
                            //add OPEN text to CLOSE text
                            $("#open-btn-text").append("open");

                        },300)
                        
                        $("#open-id").animate({ opacity: 1 });
                        $("#open-id").removeAttr("style");
                        
                        // show messages
                        $("#msg1").show()
                        $("#msg1").prepend("<div id='message' class='container' style='position: absolute;z-index: 100;margin: -66px 0px;text-align: center; padding:0px 80px;'><div class='alert alert-success alert-dismissible' role='alert'></button>"+data.msg+"</div></div>");
                        setTimeout(function(){
                            $("#msg1").hide()
                        },2500);
                    }
                    else{
                        $("#msg1").show()
                        $("#msg1").prepend("<div id='message' class='container' style='position: absolute;z-index: 100;margin: -66px 0px;text-align: center; padding:0px 80px;'><div class='alert alert-success alert-dismissible' role='alert'></button>"+data.msg+"</div></div>");
                        setTimeout(function(){
                            $("#msg1").hide()
                        },2500);
                    }
                    
                },
                error: function (jqXHR, exception) {
                    console.log("hello error?")
                    var msg = '';
                    if (jqXHR.status === 0) {
                        msg = 'Not connect.\n Verify Network.';
                    } else if (jqXHR.status == 404) {
                        msg = 'Requested page not found. [404]';
                    } else if (jqXHR.status == 500) {
                        msg = 'Internal Server Error [500].';
                    } else if (exception === 'parsererror') {
                        msg = 'Requested JSON parse failed.';
                    } else if (exception === 'timeout') {
                        msg = 'Time out error.';
                    } else if (exception === 'abort') {
                        msg = 'Ajax request aborted.';
                    } else {
                        msg = 'Uncaught Error.\n' + jqXHR.responseText;
                    }
                    //
                    $("#open-btn-loading").removeClass("openbtn-loading-open").addClass("openbtn-loading-close");
                    $("#open-btn-text").append('close');
                    $('#open-id').animate({opacity:1});
                    //show message
                    $("#msg1").show();
                    $("#msg1").prepend("<div id='message' class='container' style='position: absolute;z-index: 100;margin: -66px 0px;text-align: center; padding:0px 80px;'><div class='alert alert-danger alert-dismissible' role='alert'></button>"+msg+"</div></div>");
                    setTimeout(function(){
                        $("#msg1").hide();
                    },2500);
                },
            })
            //
            $("#open-btn-loading").removeClass("openbtn-loading-close").addClass("openbtn-loading-open");
            $("#close-btn-text").empty();
            $('#open-id').animate({opacity:.5})
        }
    });

    $(document).ready(function(){
        let title = $("#title-id").text();
        console.log(title.length);
        let len = (title.length/7)+2;
        let text_size = (63- Math.ceil((len*4)+25))+25;
        console.log(text_size)
        $("#title-id").css({"font-size": ""+text_size+"px","text-align": "start", "padding-right": "10px"})
    });
});
