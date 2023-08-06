Ext.form.BasicForm.override ({
	setValues : function(values){
		if(Ext.isArray(values)){ // array of objects
			for(var i = 0, len = values.length; i < len; i++){
				var v = values[i];
				var f = this.findField(v.id);
				if(f){
					f.setValue(v.value);
					if (this.trackResetOnLoad) {
						if (f instanceof Ext.form.CheckboxGroup) {
							f.eachItem(function(item){
								if (item instanceof Ext.form.Checkbox) item.originalValue = item.getValue();
							});
						} else {
							f.originalValue = f.getValue();
						}
					}
				}
			}
		}else{ // object hash
			var field, id;
			for(id in values){
				if(!Ext.isFunction(values[id]) && (field = this.findField(id))){
					field.setValue(values[id]);
					if (this.trackResetOnLoad) {
						if (field instanceof Ext.form.CheckboxGroup) {
							field.eachItem(function(item){
								if (item instanceof Ext.form.Checkbox) item.originalValue = item.getValue();
							});
						} else {
							field.originalValue = field.getValue();
						}
					}
				}
			}
		}
		return this;
	}
});