$(document).ready(function () {
    var clickMenu = 0;
    $(".btnMenu").unbind().click(function () {
       if(clickMenu == 0){
           $(this).removeClass('btnClose');
           $(this).addClass('btnOpen');
           $('.menuTop').css('right','0');
           clickMenu++;
       }else{
           $(this).removeClass('btnOpen');
           $(this).addClass('btnClose');
           $('.menuTop').css('right','-200px');
           clickMenu--;
       }
    });
    var clickSubMenu = 0;
    $(".menuTop li").click(function () {
        if(clickSubMenu == 0){
            $(this).find('.subMenu').addClass('active');
            clickSubMenu++;
        }else{
            $(this).find('.subMenu').removeClass('active');
            clickSubMenu--;
        }
    });
    if($(".img-thumbs").length > 0){
        $('.img-thumbs').click(function () {
            var bigImg = $(this).data('img');
            var imgInfo = $(this).data('infos');
           $(this).siblings().removeClass('active');
           $(this).addClass('active');
           $(bigImg).siblings().removeClass('active');
           $(bigImg).addClass('active');
           $(imgInfo).siblings().removeClass('active');
           $(imgInfo).addClass('active');
        });
    }
});//end document

function showPopupNotify(popupName, message) {
    $(popupName).fadeIn();
    $(popupName).find('.message').html(message);
    $(popupName + ' .close-popup').click(function () {
        $(popupName).fadeOut();
    });
}

