/**
 * JSON Simlet.
 */
Ext4.define('Ext4.ux.ajax.JsonSimlet', {
    extend: 'Ext4.ux.ajax.DataSimlet',
    alias: 'simlet.json',

    doGet: function (ctx) {
        var me = this,
            data = me.getData(ctx),
            page = me.getPage(ctx, data),
            reader = ctx.xhr.options.proxy.reader,
            ret = me.callParent(arguments), // pick up status/statusText
            response = {};

        if (reader.root) {
            response[reader.root] = page;
            response[reader.totalProperty] = data.length;
        } else {
            response = page;
        }

        if (ctx.groupSpec) {
            response.summaryData = me.getSummary(ctx, data, page);
        }

        ret.responseText = Ext4.encode(response);
        return ret;
    }
});
