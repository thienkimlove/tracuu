if(!jQuery){
    var jQuery = django.jQuery;
}

/**
 * Created by sune on 04/02/2016.
 */
function CustomFileBrowser(input_id, input_value, type, win){
    var cmsURL = '/admin/filebrowser/browse/?pop=4';
    cmsURL = cmsURL + '&type=' + type;

    tinymce.activeEditor.windowManager.open({
        file: cmsURL,
        width: 800,  // Your dimensions may differ - toy around with them!
        height: 500,
        resizable: 'yes',
        scrollbars: 'yes',
        inline: 'yes',  // This parameter only has an effect if you use the inlinepopups plugin!
        close_previous: 'no'
    }, {
        window: win,
        input: input_id,
    });
    return false;
}

tinymce.init({
    mode : "specific_textareas",
    editor_selector : "editor",
    file_browser_callback: CustomFileBrowser,
    convert_urls : false,
    themes : 'inlite',
    width: "auto",
    plugins: 'print preview searchreplace autolink directionality visualblocks visualchars fullscreen image link media template codesample table charmap hr pagebreak nonbreaking anchor toc insertdatetime advlist lists textcolor wordcount  imagetools contextmenu colorpicker textpattern help',
    toolbar1: 'formatselect | bold italic strikethrough forecolor backcolor | link | alignleft aligncenter alignright alignjustify  | numlist bullist outdent indent  | removeformat',
    image_advtab: true,
});