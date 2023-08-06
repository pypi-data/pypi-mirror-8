(function ($) {
    $(function () {
        $('input[id^=id_type_], label[for^=id_type_]').dblclick(function () {
            $(this).parents('form').submit();
        });
    });
})(jQuery);
