if (org.GeoPrisma.FileTreeFileUpload) {
    Ext.apply(org.GeoPrisma.FileTreeFileUpload.prototype, {
        actionText: "Ajouter",
        actionTooltipText: "Ajouter des fichiers dans le répertoire" +
            " sélectionné",
        windowTitleText: "Ajouter"
    });
}

if (org.GeoPrisma.FileTreeNewFolder) {
    Ext.apply(org.GeoPrisma.FileTreeNewFolder.prototype, {
        actionText: "Nouveau dossier",
        actionTooltipText: "Créer un dossier dans le répertoire sélectionné"
    });
}

if (org.GeoPrisma.form.FileUploadFormPanel) {
    Ext.apply(org.GeoPrisma.form.FileUploadFormPanel.prototype, {
        selectFileText: "Choisir un fichier",
        fileText: "Fichier",
        uploadText: "Importer",
        resetText: "Effacer",
        uploadingText: "Importation de votre fichier",
        commitSuccessText: "Succès",
        commitSuccessMessageText: "Importation complétée avec succès.",
        commitFailText: "Erreur",
        commitFailMessageText: "Une erreur est survenue." +
            " Le serveur a répondu : ",
        unknownFailMessageText: "Une erreur inconnue est survenue.",
        pleaseWaitText: "Veuillez patienter..."
    });
}
