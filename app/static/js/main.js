/*-----------Utilities-----------*/
/*-----------Searching-----------*/
const sanitizeInput = function(value){
    restrictedChars = ["{", "}", "%", "<", ">", "?", "&", "'", ",", ";",
     "+", "#", "$", "^", "*", "=", "(", ")", "[", "]", "!", "\"", "  "]
     for(var i = 0; i < restrictedChars.length; i++){
         while(value.indexOf(restrictedChars[i])!=-1){
             if(restrictedChars[i]=="  "){
                 value = value.replace(restrictedChars[i], " ")
             }
             value = value.replace(restrictedChars[i],"");
             if(value.indexOf(restrictedChars[i])==-1)
                i++
         }
     }
     return (
         value.trim()
         );
}

$("document").ready(function(){
    $(".search-bar").on("keyup", function(){
        let value = sanitizeInput($(this).val().toLowerCase())
        console.log(value)
        $(".content-container").each(function(){
            if(!$(this).children("div").children("div").children("h4").text().toLowerCase().includes(value)){
                $(this).hide()
            }else{
                $(this).show()
            }
        })
    })
})



