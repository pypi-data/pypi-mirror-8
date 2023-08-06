/*globals jQuery, document, portal_url */
/*jslint sloppy: true, vars: true, white: true, maxerr: 50, indent: 4 */
(function (jQuery) {
    /*
     * Add tinymce when needed
     */
    function textareas() {
        function init_textarea(idx, element) {
            var edit, show_box;
            element = jQuery(element);
            edit = jQuery('<img>').attr(
                {
                    src: portal_url+"/edit.png",
                    'data-fire-mce': ''
                }).css({float: 'left'});
            show_box = jQuery('<div>').html(element.text());
            element.after(show_box);
            element.after(edit);
            if (element.html()) {
                element.addClass('hiddenStructure');
            }
            edit.click(
                function(evt) {
                    jQuery.ajax({
                        url: portal_url + '/@@tinymce-jsonconfiguration?field=',
                        success: function(data) {
                            element.removeClass('hiddenStructure');
                            element.attr({
                                'data-mce-config': data
                            });
                            element.addClass('mce_editable');
                            element.addClass('pat-tinymce');
                            window.initTinyMCE(document);
                            edit.remove();
                            show_box.remove();
                        }
                    })
                }
            );
        }
        jQuery('[data-rg-infocard-richtext]').each(init_textarea);

        function handle_new_row(evt, dgf, row) {
            row.find('[data-fire-mce]').remove();
            row.find('[data-rg-infocard-richtext]').each(init_textarea);
        }
        // Bind all DGF handlers on the page
        $(document.body).delegate(
                ".datagridwidget-table-view", "afteraddrow afteraddrowauto",
            handle_new_row
        );
    }
    jQuery(document).ready(textareas);
}(jQuery));
