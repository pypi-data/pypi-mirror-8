/**
 * @class Ext4.ux.DataView.Draggable
 * @extends Object
 * @author Ed Spencer
 *
<pre><code>
Ext4.create('Ext4.view.View', {
    mixins: {
        draggable: 'Ext4.ux.DataView.Draggable'
    },

    initComponent: function() {
        this.mixins.draggable.init(this, {
            ddConfig: {
                ddGroup: 'someGroup'
            }
        });

        this.callParent(arguments);
    }
});
</code></pre>
 *
 */
Ext4.define('Ext4.ux.DataView.Draggable', {
    requires: 'Ext4.dd.DragZone',

    /**
     * @cfg {String} ghostCls The CSS class added to the outermost element of the created ghost proxy
     * (defaults to 'x-dataview-draggable-ghost')
     */
    ghostCls: 'x-dataview-draggable-ghost',

    /**
     * @cfg {Ext4.XTemplate/Array} ghostTpl The template used in the ghost DataView
     */
    ghostTpl: [
        '<tpl for=".">',
            '{title}',
        '</tpl>'
    ],

    /**
     * @cfg {Object} ddConfig Config object that is applied to the internally created DragZone
     */

    /**
     * @cfg {String} ghostConfig Config object that is used to configure the internally created DataView
     */

    init: function(dataview, config) {
        /**
         * @property dataview
         * @type Ext4.view.View
         * The Ext4.view.View instance that this DragZone is attached to
         */
        this.dataview = dataview;

        dataview.on('render', this.onRender, this);

        Ext4.apply(this, {
            itemSelector: dataview.itemSelector,
            ghostConfig : {}
        }, config || {});

        Ext4.applyIf(this.ghostConfig, {
            itemSelector: 'img',
            cls: this.ghostCls,
            tpl: this.ghostTpl
        });
    },

    /**
     * @private
     * Called when the attached DataView is rendered. Sets up the internal DragZone
     */
    onRender: function() {
        var config = Ext4.apply({}, this.ddConfig || {}, {
            dvDraggable: this,
            dataview   : this.dataview,
            getDragData: this.getDragData,
            getTreeNode: this.getTreeNode,
            afterRepair: this.afterRepair,
            getRepairXY: this.getRepairXY
        });

        /**
         * @property dragZone
         * @type Ext4.dd.DragZone
         * The attached DragZone instane
         */
        this.dragZone = Ext4.create('Ext4.dd.DragZone', this.dataview.getEl(), config);
    },

    getDragData: function(e) {
        var draggable = this.dvDraggable,
            dataview  = this.dataview,
            selModel  = dataview.getSelectionModel(),
            target    = e.getTarget(draggable.itemSelector),
            selected, dragData;

        if (target) {
            if (!dataview.isSelected(target)) {
                selModel.select(dataview.getRecord(target));
            }

            selected = dataview.getSelectedNodes();
            dragData = {
                copy: true,
                nodes: selected,
                records: selModel.getSelection(),
                item: true
            };

            if (selected.length == 1) {
                dragData.single = true;
                dragData.ddel = target;
            } else {
                dragData.multi = true;
                dragData.ddel = draggable.prepareGhost(selModel.getSelection()).dom;
            }

            return dragData;
        }

        return false;
    },

    getTreeNode: function() {
        // console.log('test');
    },

    afterRepair: function() {
        this.dragging = false;

        var nodes  = this.dragData.nodes,
            length = nodes.length,
            i;

        //FIXME: Ext4.fly does not work here for some reason, only frames the last node
        for (i = 0; i < length; i++) {
            Ext4.get(nodes[i]).frame('#8db2e3', 1);
        }
    },

    /**
     * @private
     * Returns the x and y co-ordinates that the dragged item should be animated back to if it was dropped on an
     * invalid drop target. If we're dragging more than one item we don't animate back and just allow afterRepair
     * to frame each dropped item.
     */
    getRepairXY: function(e) {
        if (this.dragData.multi) {
            return false;
        } else {
            var repairEl = Ext4.get(this.dragData.ddel),
                repairXY = repairEl.getXY();

            //take the item's margins and padding into account to make the repair animation line up perfectly
            repairXY[0] += repairEl.getPadding('t') + repairEl.getMargin('t');
            repairXY[1] += repairEl.getPadding('l') + repairEl.getMargin('l');

            return repairXY;
        }
    },

    /**
     * Updates the internal ghost DataView by ensuring it is rendered and contains the correct records
     * @param {Array} records The set of records that is currently selected in the parent DataView
     * @return {Ext4.view.View} The Ghost DataView
     */
    prepareGhost: function(records) {
        var ghost = this.createGhost(records),
            store = ghost.store;

        store.removeAll();
        store.add(records);

        return ghost.getEl();
    },

    /**
     * @private
     * Creates the 'ghost' DataView that follows the mouse cursor during the drag operation. This div is usually a
     * lighter-weight representation of just the nodes that are selected in the parent DataView.
     */
    createGhost: function(records) {
        if (!this.ghost) {
            var ghostConfig = Ext4.apply({}, this.ghostConfig, {
                store: Ext4.create('Ext4.data.Store', {
                    model: records[0].modelName
                })
            });

            this.ghost = Ext4.create('Ext4.view.View', ghostConfig);

            this.ghost.render(document.createElement('div'));
        }

        return this.ghost;
    }
});
