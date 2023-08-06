/** api-sorting_desk-live.js --- Sorting Desk's live API
 *
 * Copyright (C) 2014 Diffeo
 *
 * Author: Miguel Guedes <miguel@miguelguedes.org>
 *
 * Comments:
 *
 *
 */


var _Api = function(window, $, DossierJS) {
    // This initialization is highly suspect.
    var api = new DossierJS.API(DOSSIER_STACK_API_URL),
        qitems = new DossierJS.SortingQueueItems(
            api, 'index_scan', 'p|kb|Jeremy_Hammond', 'unknown');

    var getRandomItem = function() {
        return api.fcRandomGet().then(function(cobj) {
            var fc = cobj[1];

            return {
                content_id: cobj[0],
                fc: fc,
                node_id: cobj.content_id,
                name: fc.value('NAME') || '',
                text: fc.value('sentences')
                    || (fc.value('NAME') + ' (profile)'),
                url: fc.value('abs_url')
            };
        });
    };

    var setQueryContentId = function (id) {
        if(!id)
            throw "Invalid engine content id";

        qitems.query_content_id = id;
    };

    var itemDroppedInBin = function (item, bin) {
        return api.addLabel(bin.id, item.content.content_id, qitems.annotator, 1);
    };

    var mergeBins = function (ibin, jbin) {
        return api.addLabel(ibin.id, jbin.id, qitems.annotator, 1);
    };

    return $.extend({}, qitems.callbacks(), {
        getRandomItem: getRandomItem,
        setQueryContentId: setQueryContentId,
        itemDroppedInBin: itemDroppedInBin,
        mergeBins: mergeBins
    });
};

if(typeof define === "function" && define.amd) {
    define("API-SortingDesk", ["jquery", "DossierJS"], function($, DossierJS) {
        return _Api(window, $, DossierJS);
    });
} else {
    var Api = _Api(window, $, DossierJS);
}
