/*-----------Utilities-----------*/
/*-----------Searching-----------*/
function searching(){
    let input = $('.search-bar').val().toLowerCase();
    let articles = $('h4')
    if(input.length>2){
        input = input.slice(0,input.length-1)
    }

    articles.each(function(){
        if(!$(this).html().toLowerCase().includes(input)){
            $(this).parent().parent().siblings('hr').hide();
            $(this).parent().hide();
        } else {
            $(this).parent().parent().siblings('hr').show();
            $(this).parent().show();

        }
    })

}
console.log("aesfh")
$('.search-bar').on('keyup', searching);

