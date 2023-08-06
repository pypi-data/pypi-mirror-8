Ext.namespace("GeoExt.ux")
if (GeoExt.ux.ZoomTo) {
    Ext.apply(GeoExt.ux.ZoomTo.prototype, {
        zoomToText: "Zoomer",
        xCoordinateText: "Coordonnée X",
        yCoordinateText: "Coordonnée Y",
        projectionText: "Projection",
        invalidEntryText: "entrée invalide",
        widgetTitleText: "Outil de zoom sur coordonnées",
        destroyMarkerActionText: "Effacer +",
        closeActionText: "Fermer",
        zoomActionText: "Zoomer",
        errorText: "Erreur",
        missingProjectionText: "La projection est manquante.",
        missingCoordsText: "Coordonnées manquantes ou invalides.",
        outOfRangCoordsText: "Coordonnées à l'extérieur de l'extent courant."
    });
}
