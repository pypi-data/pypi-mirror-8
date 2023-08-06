Ext.util.Format.date = function(v, format){
  if(!v) return "";
  if(!(v instanceof Date)) v = new Date(Date.parse(v));
  return v.dateFormat(format || "Y-m-d");
};

Ext.apply(Ext.grid.PropertyColumnModel.prototype, {
  nameText   : "Propriété",
  valueText  : "Valeur",
  dateFormat : "Y-m-d"
});

Ext.apply(Ext.form.DateField.prototype, {
  disabledDaysText  : "Désactivé",
  disabledDatesText : "Désactivé",
  minText           : "La date de ce champ doit être avant le {0}",
  maxText           : "La date de ce champ doit être après le {0}",
  invalidText       : "{0} n'est pas une date valide - il doit être au format suivant: {1}",
  format            : "Y-m-d"
});