/*-----------Utilities-----------*/
/*-----------Searching-----------*/
$("document").ready(function(){
    $(".search-bar").on("keyup", function(){
        let value = $(this).val().toLowerCase()
        $(".content-container").each(function(){
            if(!$(this).children("div").children("div").children("h4").html().toLowerCase().includes(value)){
                $(this).hide()
            }else{
                $(this).show()
            }
        })
    })
})

