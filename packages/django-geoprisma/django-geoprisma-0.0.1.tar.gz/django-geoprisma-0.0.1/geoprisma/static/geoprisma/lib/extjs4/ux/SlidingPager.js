/**
* @class Ext4.ux.SlidingPager
* @extends Object
* Plugin for PagingToolbar which replaces the textfield input with a slider
* @constructor
* Create a new ItemSelector
* @param {Object} config Configuration options
*/
Ext4.define('Ext4.ux.SlidingPager', {
    requires: [
        'Ext4.slider.Single',
        'Ext4.slider.Tip'
    ],

    constructor : function(config) {
        if (config) {
            Ext4.apply(this, config);
        }
    },

    init : function(pbar){
        var idx = pbar.items.indexOf(pbar.child("#inputItem")),
            slider;

        Ext4.each(pbar.items.getRange(idx - 2, idx + 2), function(c){
            c.hide();
        });

        slider = Ext4.create('Ext4.slider.Single', {
            width: 114,
            minValue: 1,
            maxValue: 1,
            hideLabel: true,
            tipText: function(thumb) {
                return Ext4.String.format('Page <b>{0}</b> of <b>{1}</b>', thumb.value, thumb.slider.maxValue);
            },
            listeners: {
                changecomplete: function(s, v){
                    pbar.store.loadPage(v);
                }
            }
        });

        pbar.insert(idx + 1, slider);

        pbar.on({
            change: function(pb, data){
                slider.setMaxValue(data.pageCount);
                slider.setValue(data.currentPage);
            }
        });
    }
});
