/**
 * Copyright (c) 2009-2012 Mapgears Inc.
 * 
 * Published under the BSD license.
 * See http://geoprisma.org/license for the full text of the license. 
 */

Ext.namespace("org.GeoPrisma.ApplyFilter");

if (org.GeoPrisma.ApplyFilter.Manager) {
    Ext.apply(org.GeoPrisma.ApplyFilter.Manager.prototype, {
        progressBarText: "complété",
        progressBoxTitleText: "Veuillez patienter..."
    });
}

if (org.GeoPrisma.ApplyFilter.WFSFeatureGrid) {
    Ext.apply(org.GeoPrisma.ApplyFilter.WFSFeatureGrid.prototype, {
        zoomButtonTooltipText: "Recentrer la carte sur cet élément"
    });
}

if (org.GeoPrisma.ApplyFilter.MessagePanel) {
    Ext.apply(org.GeoPrisma.ApplyFilter.MessagePanel.prototype, {
        title: "Message",
        noResultText: "Aucun enregistrement ne correspond aux termes de recherche spécifiés.",
        queryFirstText: "Veuillez d'abord exécuter votre requête."
    });
}

if (org.GeoPrisma.ApplyFilter.TabPanelContainer) {
    Ext.apply(org.GeoPrisma.ApplyFilter.TabPanelContainer.prototype, {
        title: "Résultat du filtre"
    });
}
