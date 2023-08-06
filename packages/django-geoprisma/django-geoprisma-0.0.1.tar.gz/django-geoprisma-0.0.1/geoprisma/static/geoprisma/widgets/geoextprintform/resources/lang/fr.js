if (org.GeoPrisma.form && org.GeoPrisma.form.MapScaleLabel) {
    Ext.apply(org.GeoPrisma.form.MapScaleLabel.prototype, {
        fieldLabel: "Affichage actuel de la carte",
        differentScalesTooltipText: "<b>Attention</b> : Les échelles " +
            "d'impression et de la carte sont différentes.  La carte " +
            "générée dans le PDF peut être différente de celle présentement " +
            "visible.",
        sameScalesTooltipText: "Les échelles d'impression et de la carte " +
            "sont les mêmes."
    });
}
