(function ($){

$(document).ready(function (){
    $('.subjectTree > ul').keywordtree('#subject, #form-widgets-IAdvancedKeyword-advanced_keyword').collapsedtree();

    $('.subjectTree ul').each(function (){
        $(this).children().children(':checkbox').shiftcheckbox();
    });


});
}(jQuery));
