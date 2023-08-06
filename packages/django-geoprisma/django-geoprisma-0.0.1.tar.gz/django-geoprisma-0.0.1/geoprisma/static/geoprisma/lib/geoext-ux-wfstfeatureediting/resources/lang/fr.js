Ext.namespace("GeoExt.ux");
GeoExt.ux.WFSTFeatureEditingManager &&
Ext.apply(GeoExt.ux.WFSTFeatureEditingManager.prototype, {
    drawMenuButtonText: "Ajouter",
    drawMenuButtonTooltipText: "Outil d'ajout: Choisir une couche dans la liste et dessiner un nouvel élément en cliquant sur la carte.",
    editMenuButtonText: "Éditer",
    editMenuButtonTooltipText: "Outil d'édition: Choisir une couche dans la liste et cliquer sur un élément dans la carte à éditer.",
    featureGridContainerTitleText: "Features",
    featureEditorGridContainerTitleText: "Élément en cours d'édition",
    returnToSelectionText: "Retourner à la sélection",
    commitSuccessText: "Modifications sauvegardées avec succès",
    commitFailText: "Une erreur est survenue.  Les modifications n'ont pas été sauvegardées"
});

GeoExt.ux.WFSTFeatureEditingStatusBar &&
Ext.apply(GeoExt.ux.WFSTFeatureEditingStatusBar.prototype, {
    text: 'Prêt',
    defaultText: 'Prêt',
    busyText: 'Sauvegarde en cours.  Veuillez patienter...'
});

GeoExt.ux.FeatureEditorGrid &&
Ext.apply(GeoExt.ux.FeatureEditorGrid.prototype, {
    deleteMsgTitle: "Supprimer l'élément?",
    deleteMsg: "Etes-vous certain de vouloir supprimer cet élément?",
    deleteButtonText: "Supprimer",
    deleteButtonTooltip: "Supprimer cet élément",
    cancelMsgTitle: "Annuler les modifications?",
    cancelMsg: "L'élément contient des changements non sauvegardés.  Annuler les modifications?",
    cancelButtonText: "Annuler",
    cancelButtonTooltip: "Arrête l'édition, annule les changements",
    saveButtonText: "Sauvegarder",
    saveButtonTooltip: "Sauvegarder les changements",
    nameHeader: "Attribut",
    valueHeader: "Valeur"
});
