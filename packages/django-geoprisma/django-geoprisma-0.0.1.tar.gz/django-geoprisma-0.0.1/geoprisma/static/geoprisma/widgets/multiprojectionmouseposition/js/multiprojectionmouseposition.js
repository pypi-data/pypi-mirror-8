/*
   Copyright (c) 2010- Groupe Nippour, published under the BSD license.
   See http://geoprisma.org/license for the full text of the license. 
*/
  /**
   * Decimal to DMS conversion
   */
 MultiProjectionMousePosition__convertDMS = function(coordinate, type) {
    var coords = new Array();

    abscoordinate = Math.abs(coordinate)
    coordinatedegrees = Math.floor(abscoordinate);

    coordinateminutes = (abscoordinate - coordinatedegrees)/(1/60);
    tempcoordinateminutes = coordinateminutes;
    coordinateminutes = Math.floor(coordinateminutes);
    coordinateseconds = (tempcoordinateminutes - coordinateminutes)/(1/60);
    coordinateseconds =  Math.round(coordinateseconds*10);
    coordinateseconds /= 10;

    if( coordinatedegrees < 10 )
      coordinatedegrees = "0" + coordinatedegrees;

    if( coordinateminutes < 10 )
      coordinateminutes = "0" + coordinateminutes;

    if( coordinateseconds < 10 )
      coordinateseconds = "0" + coordinateseconds;

    coords[0] = coordinatedegrees+'°';
    coords[1] = coordinateminutes+'\'';
    coords[2] = coordinateseconds+'" '+this.MultiProjectionMousePosition__getHemi(coordinate, type);
    //coords[3] = '  '+this.MultiProjectionMousePosition__getHemi(coordinate, type);
    return coordinatedegrees+'° '+coordinateminutes+'\' '+coordinateseconds+'" '+this.MultiProjectionMousePosition__getHemi(coordinate, type);// coords;
  }
 
  /**
   * Return the hemisphere abbreviation for this coordinate.
   */
  MultiProjectionMousePosition__getHemi = function(coordinate, type) {
    var coordinatehemi = "";
    if (type == 'LAT') {
      if (coordinate >= 0) {
        coordinatehemi = "N";
      }
      else {
        coordinatehemi = "S";
      }
    }
    else if (type == 'LON') {
      if (coordinate >= 0) {
        coordinatehemi = "E";
      } else {
        coordinatehemi = "O";
      }
    }

    return coordinatehemi;
  }

  
Ext.namespace('OpenLayers.Control.MultiProjectionMousePosition');

OpenLayers.Control.MultiProjectionMousePosition = OpenLayers.Class(OpenLayers.Control.MousePosition, {
	
	/**
	 * 
	 */
	 activate: function(){
	    OpenLayers.Control.MousePosition.prototype.activate.apply(this,arguments);
	 }, 
	 
	 /**
	  * 
	  */
	 draw: function(){
		
		//Create the coordonate div
	    coordDiv = OpenLayers.Control.MousePosition.prototype.draw.apply(this, arguments);
	    coordDiv.className = coordDiv.className+' olControlMultiProjectionMousePositionCoord';
	    
	    //Create the selector div
	    selector = document.createElement('div');
	    selector.id = this.id + '_selector';
	    selector.className ='olControlMultiProjectionMousePositionSelector';
	    
	    //Create input element    
	    for (i=0; i<=this.widgetOptions.projections.length-1; i++){
	    	
	    	// create input element
            var inputElem = document.createElement("input");
            inputElem.name = 'MultiProjectionMousePosition_'+ this.id
            inputElem.type = 'radio';
            if(this.widgetOptions.projections[i].projection == this.widgetOptions.defaultprojection){
                
                inputElem.setAttribute('defaultChecked', 'defaultChecked');//ie
                inputElem.setAttribute("checked","checked");//FF
                //set map default projection
                this.MultiProjectionMousePosition_change(null,this.widgetOptions.projections[i].displayprojection, this.widgetOptions.projections[i].format)
            }
            selector.appendChild(inputElem);
            selector.innerHTML += this.widgetOptions.projections[i].label+'<br>';
	    } 
	    
	    //Create cancel button
	    selector.innerHTML += '<div style="float:left;"><input type="button" onclick="this.parentNode.parentNode.style.display=\'none\'" value="Annuler" style="font-size:10px"></div><div style="float:right;">NAD83</div>';
	    
	    //Create the output div
	    outputDiv = document.createElement('div');
	    outputDiv.id = this.id + '_mother';
	    outputDiv.unselectable = 'on';
	    outputDiv.className= 'olControlMultiProjectionMousePosition olControlNoSelect';
	    outputDiv.appendChild(coordDiv);
	    outputDiv.appendChild(selector); 
	    
        var j=0;
        for (i=0;i<selector.childNodes.length;i++) {
            if (selector.childNodes[i].type == "radio"){
                
                var context = {
                    'inputElem': selector.childNodes[i],
                    'config': this.widgetOptions.projections[j],
                    'oWidgetMMP': this
                    };
                    
                OpenLayers.Event.observe(selector.childNodes[i], "mouseup",
                        OpenLayers.Function.bindAsEventListener(this.onInputClick,
                                context)
                    );
                j++;
            }
        }
        OpenLayers.Event.observe(selector, "click", this.ignoreEvent);
        OpenLayers.Event.observe(selector, "mousedown", this.ignoreEvent);
        OpenLayers.Event.observe(selector, "mouseup", this.ignoreEvent);
		OpenLayers.Event.observe(outputDiv, "mouseup", this.ignoreEvent);
        OpenLayers.Event.observe(outputDiv, "click", this.ignoreEvent);
        OpenLayers.Event.observe(outputDiv, "dblclick", this.ignoreEvent);
        OpenLayers.Event.observe(coordDiv, "mousedown", OpenLayers.Function.bindAsEventListener(this.mouseDown, this));
        OpenLayers.Event.observe(coordDiv, "mouseup", OpenLayers.Function.bindAsEventListener(this.mouseUp, this));

	    
	    return outputDiv;
	 },
	 
	 /**
	  * 
	  */
	 ignoreEvent: function(evt) {
	        OpenLayers.Event.stop(evt);
	    },

	 /**
	  * 
	  */
    mouseDown: function(evt) {
        this.isMouseDown = true;
        MultiProjectionMousePosition__openSelector(this.id + '_selector');
        this.ignoreEvent(evt);
    },
	 /**
	  * 
	  */
    mouseUp: function(evt) {
        if (this.isMouseDown) {
            this.isMouseDown = false;
            this.ignoreEvent(evt);
        }
    },

    /**
     * 
     * @param element
     * @param projection
     * @param format
     */
    MultiProjectionMousePosition_change: function(element, projection, format){
        
        
        //Hide the ouput div
        try{element.parentNode.style.display='none';}catch(e){}
        
        objMMP = this.map.getControlsByClass('OpenLayers.Control.MultiProjectionMousePosition')[0];

        
        //change projection
        objMMP.displayProjection = new OpenLayers.Projection(projection);
        
        //if ouput type = 'DMS', format ouput will be Degree,Minutes,Seconds
        if (format == 'DMS'){
            objMMP.formatOutput =function(lonLat) {
                   var markup = MultiProjectionMousePosition__convertDMS(lonLat.lon, "LON");
                   markup += "&nbsp;&nbsp;&nbsp;&nbsp;" + MultiProjectionMousePosition__convertDMS(lonLat.lat, "LAT");
                   return markup
                 };
        }
        //Else, format output will be default
        else{
            //objMMP.formatOutput = OpenLayers.Control.MousePosition.prototype.formatOutput.apply(objMMP, arguments);
            objMMP.formatOutput = function(lonLat) {
                var digits = parseInt(this.numDigits);
                var newHtml =
                    this.prefix +
                    lonLat.lon.toFixed(digits) +
                    this.separator + 
                    lonLat.lat.toFixed(digits) +
                    this.suffix;
                return newHtml;	    
            }
        }
    },
    /**
     * 
     */
    onInputClick: function(e) {
        if (!this.inputElem.disabled) {            
            if (this.inputElem.type == "radio") {
                //fix IE; uncheck radio boxes
                for (i=0;i<this.inputElem.parentNode.childNodes.length;i++) {
                    if(this.inputElem.parentNode.childNodes[i].type == "radio"){
                        this.inputElem.parentNode.childNodes[i].checked = false;                        
                    }          
                }
                this.inputElem.checked = true;
                //do stuff
                this.oWidgetMMP.MultiProjectionMousePosition_change(this.inputElem,this.config.displayprojection, this.config.format);
            } else {
                this.inputElem.checked = !this.inputElem.checked;
            }
        }
        OpenLayers.Event.stop(e);
    },
	CLASS_NAME: "OpenLayers.Control.MultiProjectionMousePosition"
});

/**
 * 
 * @param id
 */
function MultiProjectionMousePosition__openSelector(id){
	
	element = document.getElementById(id);
	
	if(element.style.display == 'none' || element.style.display == ''){
		element.style.display = 'block';
	}else{
		element.style.display = 'none';
	}	
}

