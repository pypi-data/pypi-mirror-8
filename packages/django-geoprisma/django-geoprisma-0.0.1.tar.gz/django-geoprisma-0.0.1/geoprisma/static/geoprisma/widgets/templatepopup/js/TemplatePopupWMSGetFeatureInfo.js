/*
   Copyright (c) 2009- Boreal - Information Strategies, published under the BSD license.
   See http://geoprisma.org/license for the full text of the license.
*/

/**
 * Class: OpenLayers.Control.TemplatePopupWMSGetFeatureInfo
 *
 * Inherits From:
 *  - <OpenLayers.Control.WMSGetFeatureInfo>
 */
OpenLayers.Control.TemplatePopupWMSGetFeatureInfo = OpenLayers.Class(OpenLayers.Control.WMSGetFeatureInfo, {

    /**
     * Method: urlMatches
     * Override url matching to always return true, as this causes issues with proxy alliases.
     * Layer url matches must be controlled on another level.
     *
     * Parameters:
     * url - {String} The url to test.
     *
     * Returns:
     * {Boolean} true.
     */
    urlMatches: function(url) {
        return true;
    },

    CLASS_NAME: "OpenLayers.Control.WMSGetFeatureInfo"
});
/*
   Copyright (c) 2009- Boreal - Information Strategies, published under the BSD license.
   See http://geoprisma.org/license for the full text of the license.
*/

/**
 * Class: OpenLayers.Control.TemplatePopupWMSGetFeatureInfo
 *
 * Inherits From:
 *  - <OpenLayers.Control.WMSGetFeatureInfo>
 */
OpenLayers.Control.TemplatePopupWMSGetFeatureInfo = OpenLayers.Class(OpenLayers.Control.WMSGetFeatureInfo, {

    /**
     * Method: urlMatches
     * Override url matching to always return true, as this causes issues with proxy alliases.
     * Layer url matches must be controlled on another level.
     *
     * Parameters:
     * url - {String} The url to test.
     *
     * Returns:
     * {Boolean} true.
     */
    urlMatches: function(url) {
        return true;
    },

    CLASS_NAME: "OpenLayers.Control.WMSGetFeatureInfo"
});
