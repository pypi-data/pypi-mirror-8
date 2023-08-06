/**
 * @author Nicolas Ferrero
 * @class Ext4.ux.GroupTabPanel
 * @extends Ext4.Container
 * A TabPanel with grouping support.
 */
Ext4.define('Ext4.ux.GroupTabPanel', {
    extend: 'Ext4.Container',

    alias: 'widget.grouptabpanel',

    requires:[
        'Ext4.data.*',
        'Ext4.tree.*',
        'Ext4.layout.*'
    ],

    baseCls : Ext4.baseCSSPrefix + 'grouptabpanel',

    initComponent: function(config) {
        var me = this;

        Ext4.apply(me, config);

        // Processes items to create the TreeStore and also set up
        // "this.cards" containing the actual card items.
        me.store = me.createTreeStore();

        me.layout = {
            type: 'hbox',
            align: 'stretch'
        };
        me.defaults = {
            border: false
        };

        me.items = [{
            xtype: 'treepanel',
            cls: 'x-tree-panel x-grouptabbar',
            width: 150,
            rootVisible: false,
            store: me.store,
            hideHeaders: true,
            animate: false,
            processEvent: Ext4.emptyFn,
            viewConfig: {
                overItemCls: '',
                getRowClass: me.getRowClass,
                itemSelector: 'div.' + Ext4.baseCSSPrefix + 'grouptab-row',
                cellSelector: 'div.' + Ext4.baseCSSPrefix + 'grouptab',
                getTableChunker: function() {
                    return Ext4.ux.GroupTreeChunker;
                },
                onHeaderResize: function(header, w, suppressFocus) {
                    var me = this,
                        el = me.el;

                    if (el) {
                        el.select('div.' + Ext4.baseCSSPrefix + 'grid-table-resizer').setWidth(me.headerCt.getFullWidth());
                        if (!me.ignoreTemplate) {
                            me.setNewTemplate();
                        }
                        if (!suppressFocus) {
                            me.el.focus();
                        }
                        me.forceReflow();
                    }
                }
            },
            columns: [{
                xtype: 'treecolumn',
                sortable: false,
                dataIndex: 'text',
                flex: 1,
                renderer: function (value, cell, node, idx1, idx2, store, tree) {
                    var cls = '';

                    if (node.parentNode && node.parentNode.parentNode === null) {
                        cls += ' x-grouptab-first';
                        if (node.previousSibling) {
                            cls += ' x-grouptab-prev';
                        }
                        if (!node.get('expanded') || node.firstChild == null) {
                            cls += ' x-grouptab-last';
                        }
                    } else if (node.nextSibling === null) {
                        cls += ' x-grouptab-last';
                    } else {
                        cls += ' x-grouptab-center';
                    }
                    if (node.data.activeTab) {
                        cls += ' x-active-tab';
                    }
                    cell.tdCls= 'x-grouptab'+ cls;

                    return value;
                }
             }]
        },{
            xtype: 'container',
            flex: 1,
            layout: 'card',
            activeItem: me.mainItem,
            baseCls: Ext4.baseCSSPrefix + 'grouptabcontainer',
            items: me.cards
        }];

        me.addEvents(
            /**
             * @event beforetabchange
             * Fires before a tab change (activated by {@link #setActiveTab}). Return false in any listener to cancel
             * the tabchange
             * @param {Ext4.ux.GroupTabPanel} grouptabPanel The GroupTabPanel
             * @param {Ext4.Component} newCard The card that is about to be activated
             * @param {Ext4.Component} oldCard The card that is currently active
             */
            'beforetabchange',

            /**
             * @event tabchange
             * Fires when a new tab has been activated (activated by {@link #setActiveTab}).
             * @param {Ext4.ux.GroupTabPanel} grouptabPanel The GroupTabPanel
             * @param {Ext4.Component} newCard The newly activated item
             * @param {Ext4.Component} oldCard The previously active item
             */
            'tabchange',

            /**
             * @event beforegroupchange
             * Fires before a group change (activated by {@link #setActiveGroup}). Return false in any listener to cancel
             * the groupchange
             * @param {Ext4.ux.GroupTabPanel} grouptabPanel The GroupTabPanel
             * @param {Ext4.Component} newGroup The root group card that is about to be activated
             * @param {Ext4.Component} oldGroup The root group card that is currently active
             */
            'beforegroupchange',

            /**
             * @event groupchange
             * Fires when a new group has been activated (activated by {@link #setActiveGroup}).
             * @param {Ext4.ux.GroupTabPanel} grouptabPanel The GroupTabPanel
             * @param {Ext4.Component} newGroup The newly activated root group item
             * @param {Ext4.Component} oldGroup The previously active root group item
             */
            'groupchange'
        );

        me.callParent(arguments);
        me.setActiveTab(me.activeTab);
        me.setActiveGroup(me.activeGroup);
        me.mon(me.down('treepanel').getSelectionModel(), 'select', me.onNodeSelect, me);
    },

    getRowClass: function(node, rowIndex, rowParams, store) {
        var cls = '';
        if (node.data.activeGroup) {
           cls += ' x-active-group';
        }
        return cls;
    },

    /**
     * @private
     * Node selection listener.
     */
    onNodeSelect: function (selModel, node) {
        var me = this,
            currentNode = me.store.getRootNode(),
            parent;

        if (node.parentNode && node.parentNode.parentNode === null) {
            parent = node;
        } else {
            parent = node.parentNode;
        }

        if (me.setActiveGroup(parent.get('id')) === false || me.setActiveTab(node.get('id')) === false) {
            return false;
        }

        while (currentNode) {
            currentNode.set('activeTab', false);
            currentNode.set('activeGroup', false);
            currentNode = currentNode.firstChild || currentNode.nextSibling || currentNode.parentNode.nextSibling;
        }

        parent.set('activeGroup', true);
        parent.eachChild(function(child) {
            child.set('activeGroup', true);
        });
        node.set('activeTab', true);
        selModel.view.refresh();
    },

    /**
     * Makes the given component active (makes it the visible card in the GroupTabPanel's CardLayout)
     * @param {Ext4.Component} cmp The component to make active
     */
    setActiveTab: function(cmp) {
        var me = this,
            newTab = cmp,
            oldTab;

        if(Ext4.isString(cmp)) {
            newTab = Ext4.getCmp(newTab);
        }

        if (newTab === me.activeTab) {
            return false;
        }

        oldTab = me.activeTab;
        if (me.fireEvent('beforetabchange', me, newTab, oldTab) !== false) {
             me.activeTab = newTab;
             if (me.rendered) {
                 me.down('container[baseCls=' + Ext4.baseCSSPrefix + 'grouptabcontainer' + ']').getLayout().setActiveItem(newTab);
             }
             me.fireEvent('tabchange', me, newTab, oldTab);
         }
         return true;
    },

    /**
     * Makes the given group active
     * @param {Ext4.Component} cmp The root component to make active.
     */
    setActiveGroup: function(cmp) {
        var me = this,
            newGroup = cmp,
            oldGroup;

        if(Ext4.isString(cmp)) {
            newGroup = Ext4.getCmp(newGroup);
        }

        if (newGroup === me.activeGroup) {
            return true;
        }

        oldGroup = me.activeGroup;
        if (me.fireEvent('beforegroupchange', me, newGroup, oldGroup) !== false) {
             me.activeGroup = newGroup;
             me.fireEvent('groupchange', me, newGroup, oldGroup);
         } else {
             return false;
         }
         return true;
    },

    /**
     * @private
     * Creates the TreeStore used by the GroupTabBar.
     */
    createTreeStore: function() {
        var me = this,
            groups = me.prepareItems(me.items),
            data = {
                text: '.',
                children: []
            },
            cards = me.cards = [];
        me.activeGroup = me.activeGroup || 0;
        
        Ext4.each(groups, function(groupItem, idx) {
            var leafItems = groupItem.items.items,
                rootItem = (leafItems[groupItem.mainItem] || leafItems[0]),
                groupRoot = {
                    children: []
                };

            // Create the root node of the group
            groupRoot.id = rootItem.id;
            groupRoot.text = rootItem.title;
            groupRoot.iconCls = rootItem.iconCls;

            groupRoot.expanded = true;
            groupRoot.activeGroup = (me.activeGroup === idx);
            groupRoot.activeTab = groupRoot.activeGroup ? true : false;
            if (groupRoot.activeTab) {
                me.activeTab = groupRoot.id;
            }

            if (groupRoot.activeGroup) {
                me.mainItem = groupItem.mainItem || 0;
                me.activeGroup = groupRoot.id;
            }

            Ext4.each(leafItems, function(leafItem) {
                // First node has been done
                if (leafItem.id !== groupRoot.id) {
                    var child = {
                        id: leafItem.id,
                        leaf: true,
                        text: leafItem.title,
                        iconCls: leafItem.iconCls,
                        activeGroup: groupRoot.activeGroup,
                        activeTab: false
                    };
                    groupRoot.children.push(child);
                }

                // Ensure the items do not get headers
                delete leafItem.title;
                delete leafItem.iconCls;
                cards.push(leafItem);
            });

            data.children.push(groupRoot);
      });

       return Ext4.create('Ext4.data.TreeStore', {
            fields: ['id', 'text', 'activeGroup', 'activeTab'],
            root: {
                expanded: true
            },
            proxy: {
                type: 'memory',
                data: data
            }
        });
    },

    /**
     * Returns the item that is currently active inside this GroupTabPanel.
     * @return {Ext4.Component/Number} The currently active item
     */
    getActiveTab: function() {
        return this.activeTab;
    },

    /**
     * Returns the root group item that is currently active inside this GroupTabPanel.
     * @return {Ext4.Component/Number} The currently active root group item
     */
    getActiveGroup: function() {
        return this.activeGroup;
    }
});

/**
 * Allows GroupTab to render a table structure.
 */
Ext4.define('Ext4.ux.GroupTreeChunker', {
    singleton: true,
    requires: ['Ext4.XTemplate'],
    metaTableTpl: [
        '{%if (this.openTableWrap)out.push(this.openTableWrap())%}',
        '<table class="' + Ext4.baseCSSPrefix + 'grid-table-resizer" border="0" cellspacing="0" cellpadding="0" {[this.embedFullWidth(values)]}><tr><td>',
            '{[this.openRows()]}',
                '{row}',
            '{[this.closeRows()]}',
        '</td></tr><table>',
        '{%if (this.closeTableWrap)out.push(this.closeTableWrap())%}'
    ],

    constructor: function() {
        Ext4.XTemplate.prototype.recurse = function(values, reference) {
            return this.apply(reference ? values[reference] : values);
        };
    },

    embedFullWidth: function(values) {
        var result = 'style="width:{fullWidth}px;';

        // If there are no records, we need to give the table a height so that it
        // is displayed and causes q scrollbar if the width exceeds the View's width.
        if (!values.rowCount) {
            result += 'height:1px;';
        }
        return result + '"';
    },

    openRows: function() {
        return '<tpl for="rows">';
    },

    closeRows: function() {
        return '</tpl>';
    },

    metaRowTpl: [
        '<div class="' + Ext4.baseCSSPrefix + 'grouptab-row {[this.embedRowCls()]}" {[this.embedRowAttr()]}>',
            '<tpl for="columns">',
                '<div class="{cls} ' + Ext4.baseCSSPrefix + 'grouptab-cell ' + Ext4.baseCSSPrefix + 'grid-cell-{columnId} {{id}-modified} {{id}-tdCls} {[this.firstOrLastCls(xindex, xcount)]}" {{id}-tdAttr}>',
                    '<div {unselectableAttr} class="' + Ext4.baseCSSPrefix + 'grid-cell-inner {unselectableCls}" style="text-align: {align}; {{id}-style};">{{id}}</div>',
                    '<div class="x-grouptabs-corner x-grouptabs-corner-top-left" id="ext-gen25"></div>',
                    '<div class="x-grouptabs-corner x-grouptabs-corner-bottom-left" id="ext-gen26"></div>',
                '</div>',
            '</tpl>',
        '</div>'
    ],

    firstOrLastCls: function(xindex, xcount) {
        if (xindex === 1) {
            return Ext4.view.Table.prototype.firstCls;
        } else if (xindex === xcount) {
            return Ext4.view.Table.prototype.lastCls;
        }
    },
    
    embedRowCls: function() {
        return '{rowCls}';
    },
    
    embedRowAttr: function() {
        return '{rowAttr}';
    },

    getTableTpl: function(cfg, textOnly) {
        var tpl,
            tableTplMemberFns = {
                openRows: this.openRows,
                closeRows: this.closeRows,
                embedFullWidth: this.embedFullWidth
            },
            tplMemberFns = {},
            features = cfg.features || [],
            ln = features.length,
            i  = 0,
            memberFns = {
                embedRowCls: this.embedRowCls,
                embedRowAttr: this.embedRowAttr,
                firstOrLastCls: this.firstOrLastCls,
                unselectableAttr: cfg.enableTextSelection ? '' : 'unselectable="on"',
                unselectableCls: cfg.enableTextSelection ? '' : Ext4.baseCSSPrefix + 'unselectable'
            },
            // copy the default
            metaRowTpl = Array.prototype.slice.call(this.metaRowTpl, 0),
            metaTableTpl;
            
        for (; i < ln; i++) {
            if (!features[i].disabled) {
                features[i].mutateMetaRowTpl(metaRowTpl);
                Ext4.apply(memberFns, features[i].getMetaRowTplFragments());
                Ext4.apply(tplMemberFns, features[i].getFragmentTpl());
                Ext4.apply(tableTplMemberFns, features[i].getTableFragments());
            }
        }
        
        metaRowTpl = new Ext4.XTemplate(metaRowTpl.join(''), memberFns);
        cfg.row = metaRowTpl.applyTemplate(cfg);
        
        metaTableTpl = new Ext4.XTemplate(this.metaTableTpl.join(''), tableTplMemberFns);
        
        tpl = metaTableTpl.applyTemplate(cfg);
        
        // TODO: Investigate eliminating.
        if (!textOnly) {
            tpl = new Ext4.XTemplate(tpl, tplMemberFns);
        }
        return tpl;
        
    }
});
