/*globals jQuery, document */
/*jslint sloppy: true, vars: true, white: true, maxerr: 50, indent: 4 */
(function (jQuery) {
    /*
     * docs ...
     */
    function prepOverlay() {
        return jQuery('[data-rg-infocard-overlay]').prepOverlay({
            subtype: 'ajax',
        });
    }


    function prepDataTables() {
        function initDataTable(idx, element) {
            var table;
            element = jQuery(element);
            element.removeClass(['listing', 'collection-listing']);
            element.find('tr.odd').removeClass('odd');
            element.find('tr.even').removeClass('even');
            table = element.dataTable({
                'iDisplayLength': 500,
                'sDom': 'ft',
                "oLanguage": {
                    "sSearch": "Restringi la ricerca",
                }
            });
            jQuery('.dataTables_filter input').focus();
        }
        return jQuery('[data-rg-infocard-datatables]').each(initDataTable);
    }
    /* jQuery(document).ready(prepOverlay); */
    jQuery(document).ready(prepDataTables);


}(jQuery));
