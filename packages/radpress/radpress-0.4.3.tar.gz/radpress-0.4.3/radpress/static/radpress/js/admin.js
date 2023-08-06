$(document).ready(function() {
    // get markup description
    var markupSelect = $('select#id_markup');

    markupSelect.on('change', function() {
        var className = '.radpress-description.' + $(this).val();
        var html = $(className).clone();
        html.removeAttr('style');

        $(this).parent().find('.radpress-description').remove();
        $(this).after(html);
    });

    markupSelect.trigger('change');
});
