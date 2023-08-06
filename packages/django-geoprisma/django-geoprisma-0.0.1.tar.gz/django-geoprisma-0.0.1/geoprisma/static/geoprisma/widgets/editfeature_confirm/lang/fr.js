if (org.GeoPrisma.EditFeature && org.GeoPrisma.EditFeature.Confirm) {
    Ext.apply(org.GeoPrisma.EditFeature.Confirm.prototype, {
        popupTitleText: "Confirmation",
        popupText: "Confirmer les modifications ?",
        confirmButtonText: "Ok",
        cancelButtonText: "Annuler"
    });
}
