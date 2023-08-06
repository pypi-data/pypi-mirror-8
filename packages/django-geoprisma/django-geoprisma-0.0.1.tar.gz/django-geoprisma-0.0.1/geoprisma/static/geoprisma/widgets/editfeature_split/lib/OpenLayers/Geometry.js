/**
 * Function: OpenLayers.Geometry.pointOnSegment
 * Note that the OpenLayers.Geometry.segmentsIntersect doesn't work with points
 *
 * Parameters:
 * point - {Object} An object with x and y properties representing the
 *     point coordinates.
 * segment - {Object} An object with x1, y1, x2, and y2 properties
 *     representing endpoint coordinates.
 *
 * Returns:
 * {Boolean} Returns true if the point is on the segment.
 */
OpenLayers.Geometry.pointOnSegment = function(point, segment) {
    // Is the point inside the BBox of the segment
    if(point.x < Math.min(segment.x1, segment.x2) || point.x > Math.max(segment.x1, segment.x2) ||
       point.y < Math.min(segment.y1, segment.y2) || point.y > Math.max(segment.y1, segment.y2))
    {
        return false;
    }

    // Avoid dividing by zero
    if( segment.x1 == segment.x2 || segment.y1 == segment.y2 || 
        (point.x == segment.x1 && point.y == segment.y1) || 
        (point.x == segment.x2 && point.y == segment.y2) )
    {
        return true;
    }

    // Is the point on the line
    if(((segment.x1 - point.x) / (segment.y1 - point.y)).toFixed(5) == 
       ((segment.x2 - point.x) / (segment.y2 - point.y)).toFixed(5))
    {
        return true;
    }

    return false;
};
