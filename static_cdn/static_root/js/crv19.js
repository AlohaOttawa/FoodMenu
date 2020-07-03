$(document).ready(function(){
    // contact form handler

    // pull from templates-> contact-> view.html
    var contactForm = $(".contact-form")
    var contactFormMethod = contactForm.attr("method")
    var contactFormEndpoint = contactForm.attr("action")    // get the url endpoint


    function displaySubmitting(submitBtn, defaultText, doSubmit){

        if (doSubmit){
            submitBtn.addClass("disabled")
            submitBtn.html("<i class='fa fa-spin fa-spinner'></i> Sending ...")
        } else {
            submitBtn.removeClass("disabled")
            submitBtn.html(defaultText)
        }
    }
    // handle submits which can happen anywhere
    contactForm.submit(function(event){
        event.preventDefault()
        var contactFormSubmitBtn = contactForm.find("[type='submit']")
        var contactFormSubmitBtnTxt = contactFormSubmitBtn.text()
        var contactFormData = contactForm.serialize()
        displaySubmitting(contactFormSubmitBtn, "", true)
        $.ajax({
            method: contactFormMethod,
            url: contactFormEndpoint,
            data: contactFormData,
            success: function(data){
                contactForm[0].reset()
                $.alert({
                    title: 'Success!!',
                    content: data.message,
                    theme: "modern",
                })
                setTimeout(function(){
                    displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false)
                }, 500)
            },
            error: function(error){
                console.log(error.responseJSON)
                var jsonData = error.responseJSON
                var msg = ""
                $.each(jsonData, function(key, value){  // returns py dict vs array so key, value vs index, obj
                    msg += key + ": " + value[0].message + "<br/>"
                })
                $.alert({
                    title: 'Alert!',
                    content: msg,
                    theme: "dark",
                })
                setTimeout(function(){
                    displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false)
                }, 500)
            }
        })
    })


    // Auto search
    var searchForm =$(".search-form")
    var searchInput = searchForm.find("[name='q']")     // find the input name='q'
    var typingTimer;
    var typingInterval = 500   // 1 second
    var searchBTN = searchForm.find("[type='submit']")

    searchInput.keyup(function(event){
        // key released
        clearTimeout(typingTimer)
        typingTimer = setTimeout(performSearch, typingInterval)
    })

    searchInput.keydown(function(event){
        // key pressed down
        clearTimeout(typingTimer)
    })

    function displaySearching(){
        searchBTN.addClass("disabled")
        searchBTN.html("<i class='fa fa-spin fa-spinner'></i> Searching ...")
    }

    function performSearch(){
        displaySearching()
        var query = searchInput.val()
        setTimeout(function(){
            window.location.href = "/search/?q=" + query
        }, 1000)
    }

    // Cart + add Menuitems

    var menuitemForm = $(".form-menuitem-ajax")    // if html id then us #form-menuitem-ajax

    menuitemForm.submit(function(event){
        event.preventDefault();
        // console.log("Form is not sending")
        var thisForm = $(this)
        // var actionEndpoint = thisForm.attr("action");   // API endpoint
        var actionEndpoint = thisForm.attr("data-endpoint")
        var httpMethod = thisForm.attr("method");
        var formData = thisForm.serialize();    // data into backend package format

        $.ajax({
            url: actionEndpoint,
            method: httpMethod,
            data: formData,
            success: function (data) {
                var submitSpan = thisForm.find(".submit-span")
                if(data.added){
                    submitSpan.html("In cart <button type=\"submit\" class=\"btn btn-link\"> Remove this dish?</button>")
                } else {
                    submitSpan.html(" <button type=\"submit\" class=\"btn btn-success\"> Add to cart </button>")
                }
                var navbarCount = $(".navbar-cart-count")
                navbarCount.text(data.cartItemCount)

                var currentPath = window.location.href
                if (currentPath.indexOf("cart") != -1){
                    refreshCart()
                }
            },
            error: function(errorData){
                $.alert({
                    title: 'Alert!',
                    content: 'Something is wrong!',
                    theme: "dark",
                })
            }
        })

    })

    function refreshCart(){
        console.log("In current cart")
        var cartTable = $(".cart-table")
        var cartBody = cartTable.find(".cart-body")
        //cartBody.html("<h1>Its Changed</h1>")
        var menuitemRows = cartBody.find(".cart-menuitem")
        var currentURL = window.location.href

        var refreshCartURL = "/api/cart/";
        var refreshCartMethod = "GET";
        var data = {};
        $.ajax({
            url: refreshCartURL,
            method: refreshCartMethod,
            data: data,
            success: function(data){
                var hiddenCartMenuitemRemoveForm = $(".cart-menuitem-remove-form")
                console.log(hiddenCartMenuitemRemoveForm)
                if (data.menuitems.length > 0) {
                    menuitemRows.html("")
                    counter = data.menuitems.length
                    $.each(data.menuitems, function(index, value){
                        var newCartMenuitemRemove = hiddenCartMenuitemRemoveForm.clone()
                        newCartMenuitemRemove.css("display", "block")
                        newCartMenuitemRemove.find(".cart-menuitem-id").val(value.id)
                        // newCartMenuitemRemove.removeClass("hidden-class") if class based. Later maybe
                        cartBody.prepend("<tr><th scope=\"row\">" + counter + "</th><td><a href=" + "'" + value.url + "'>" + value.name + "</a>" + newCartMenuitemRemove.html()  + "</td><td>" + value.price + "</td></tr>")
                        counter --
                    })

                    cartBody.find(".cart-subtotal").text(data.subtotal)
                    cartBody.find(".cart-total").text(data.total)
                } else{
                    window.location.href = currentURL
                }

            },
            error: function(errorData){
                $.alert({
                    title: 'Alert!',
                    content: 'Refresh error!',
                    theme: "dark",
                })
            }
        })
    }
})