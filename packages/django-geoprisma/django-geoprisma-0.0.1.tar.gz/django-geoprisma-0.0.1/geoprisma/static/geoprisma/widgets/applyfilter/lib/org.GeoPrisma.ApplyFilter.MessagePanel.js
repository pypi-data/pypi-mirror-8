/**
 * Copyright (c) 2009-2012 Mapgears Inc.
 * 
 * Published under the BSD license.
 * See http://geoprisma.org/license for the full text of the license. 
 */

Ext.namespace("org.GeoPrisma.ApplyFilter");

/** api: (define)
 *  module = org.GeoPrisma.ApplyFilter
 *  class = MessagePanel
 */

/** api: constructor
 *  .. class:: MessagePanel
 */
org.GeoPrisma.ApplyFilter.MessagePanel = Ext.extend(Ext.Panel, {

    // i18n

    /** api: property[title] ``String`` i18n */
    title: "Message",

    /** api: property[noResultText] ``String`` i18n */
    noResultText: "Your search did not match any records.",

    /** api: property[queryFirstText] ``String`` i18n */
    queryFirstText: "Please, make a query first.",

    // API Properties, default values

    /** api: property[border]
     *  ``Boolean``
     *  Default value for this parameter.
     */
    border: false,

    /** api: property[style]
     *  ``String``
     *  Default value for this parameter.
     */
    style: 'padding:10px 0 10px 10px',

    // Private Properties

    currentMessage: null,

    /** private: method[constructor]
     */
    constructor: function(config) {
        Ext.apply(this, config);
        arguments.callee.superclass.constructor.call(this, config);
        this.setQueryFirstMessage();
    },

    /** public: method[setNoResultMessage]
     *  Display the "noResultText" as content of this panel.
     */
    setNoResultMessage: function() {
        this.updateMessage(this.noResultText);
    },

    /** public: method[setQueryFirstMessage]
     *  Display the "queryFirstText" as content of this panel.
     */
    setQueryFirstMessage: function() {
        this.updateMessage(this.queryFirstText);
    },

    /** private: method[updateMessage]
     *  :arg msg: ``String`` A text to set as panel content
     *  Update or set panel content with message if not already set.
     */
    updateMessage: function(msg) {
        if (msg == this.currentMessage) {
            return;
        }
        if (this.rendered) {
            this.update(msg);
        } else {
            this.html = msg;
        }
        this.currentMessage = msg;
    }
});
