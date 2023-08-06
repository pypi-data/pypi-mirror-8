/* 
   Copyright (c) 2011- MapGears Inc., published under the BSD license.
   See http://geoprisma.org/license for the full text of the license. 
*/ 

/**
 * IMPORTANT NOTE ABOUT THIS FILE
 *
 * This file contains a fixes to allow update and delete requests with the HTTP
 * protocol using the geoprisma proxy.
 */

OpenLayers.Protocol.HTTP.prototype.update = function(feature, options) {
    options = options || {};
    var url = options.url ||
              feature.url ||
              ((this.options.url.indexOf('?')>-1)?this.options.url.replace(/\?/, '/' + feature.fid + '?'):this.options.url + '/' + feature.fid);
    options = OpenLayers.Util.applyDefaults(options, this.options);

    var resp = new OpenLayers.Protocol.Response({
        reqFeatures: feature,
        requestType: "update"
    });

    resp.priv = OpenLayers.Request.PUT({
        url: url,
        callback: this.createCallback(this.handleUpdate, resp, options),
        headers: options.headers,
        data: this.format.write(feature)
    });

    return resp;
};

OpenLayers.Protocol.HTTP.prototype["delete"] = function(feature, options) {
    options = options || {};
    var url = options.url ||
              feature.url ||
              (( this.options.url.indexOf('?')>-1)?this.options.url.replace(/\?/, '/' + feature.fid + '?'):this.options.url + '/' + feature.fid);
    options = OpenLayers.Util.applyDefaults(options, this.options);

    var resp = new OpenLayers.Protocol.Response({
        reqFeatures: feature,
        requestType: "delete"
    });

    resp.priv = OpenLayers.Request.DELETE({
        url: url,
        callback: this.createCallback(this.handleDelete, resp, options),
        headers: options.headers
    });

    return resp;
};
