/* 
   Copyright (c) 2009-2012 Boreal - Information Strategies
   Published under the BSD license.
   See http://geoprisma.org/license for the full text of the license. 
*/ 

Ext.namespace("org.GeoPrisma");

/** api: (define)
 *  module = org.GeoPrisma
 *  class = MySampleClass
 */

/** api: constructor
 *  .. class:: MySampleClass
 */
org.GeoPrisma.MySampleClass = Ext.extend(Ext.util.Observable, {

    /** api: property[foo]
     * ``String``
     * A sample api property named 'foo'
     */
    foo: null,

    /** private: property[bar]
     *  ``String``
     *  A sample private property named 'bar'
     */
    bar: null,

    /** private: method[constructor]
     *  Private constructor override.
     */
    constructor: function(config) {
        Ext.apply(this, config);
        arguments.callee.superclass.constructor.call(this, config);
    }
});
