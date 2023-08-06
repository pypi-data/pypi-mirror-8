Ext.namespace("Ext.form.FormPanel");

Ext.form.FormPanel.prototype.enableFormContent = function(enable) {
    if(enable)
	{
		this.startMonitoring();
		this.cascade(function()
		{
			switch(true)
			{
				case this instanceof Ext.form.CheckboxGroup:
					this.preventMark = false;
					this.removeClass('field-readonly');
					this.enable();
					break;

				case this instanceof Ext.form.TextField :
					this.preventMark = false;
					this.removeClass('field-readonly');
					this.setReadOnly(false);
					break;

				case this instanceof Ext.Button :
					this.show();
					break;
			}
		});
	}
	else
	{
		this.stopMonitoring();
		this.cascade(function()
		{
			switch(true)
			{
				case this instanceof Ext.form.CheckboxGroup:
					this.clearInvalid();
					this.preventMark = true;
					this.addClass('field-readonly');
					this.disable();
					break;

				case this instanceof Ext.form.TextField :
					this.clearInvalid();
					this.preventMark = true;
					this.addClass('field-readonly');
					this.setReadOnly(true);
					break;

				case this instanceof Ext.Button :
					this.hide();
					break;
			}
		});
	}
};