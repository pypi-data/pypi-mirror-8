Ext.namespace("org.GeoPrisma");

if (org.GeoPrisma.KeepActiveSession) {
    Ext.apply(org.GeoPrisma.KeepActiveSession.prototype, {
        error_text: "Une erreur c'est produite avec votre session, l'application va être relancé.",
    });
}