/*
   Copyright (c) 2011- Solution Globale, published under the BSD license.
   See http://geoprisma.org/license for the full text of the license.
*/

Ext.namespace("org.GeoPrisma");

/** api: (define)
 *  module = org.GeoPrisma
 *  class = KeepActiveSession
 */

/** api: constructor
 *  .. class:: KeepActiveSession
 */
org.GeoPrisma.KeepActiveSession = Ext.extend(Ext.util.Observable, {

    /* API Properties */

    /** api: property[error_text]
     * ``String``
     * error_text to be displayed before the reloading of the page
     */
    error_text: "There is something wrong with your session, the application will be reloaded.",

    /** api: property[url]
     * ``String``
     * url of proxy to call
     */
    url: null,

    /** api: property[delay]
     * ``Integer``
     * number of second between each call
     */
    delay: 5* 60,

    /** api: property[retry]
     * ``Integer``
     * number of retry before failing
     */
    retry: 5,

    /** api: property[retry_counter]
     * ``Integer``
     * counter of retry
     */
    try_counter: 0,

    /** private: method[constructor]
     *  This class is a superconstructor only.
     */
    constructor: function(config) {
        Ext.apply(this, config);
        arguments.callee.superclass.constructor.call(this, config);

        // start keep session active and use createDelegate to preserve scope
        setInterval(this.sendRequest.createDelegate(this), this.delay*1000);
    },

    /** private: method[sendRequest]
     *  Send a request to server to keep session active
     */
    sendRequest: function(){
        Ext.Ajax.request({
            url: this.url,
            success: function(record, opts) {
                if (record.status == 0){
                    if(this.try_counter >= this.retry){
                        alert(this.error_text);
                        window.location.reload(true);
                    }else{
                        setTimeout(function(){that.sendRequest()},5000);
                        return false;
                    }
                }
                this.try_counter = 0;
                return true;
            },
            failure: function(record, opts) {
                this.try_counter++;
                if(this.try_counter >= this.retry){
                    alert(this.error_text);
                    window.location.reload(true);
                    return false;
                }else{
                    var that = this;
                    setTimeout(function(){that.sendRequest()},5000);
                }
            },
            scope:this
        });
    }
});
