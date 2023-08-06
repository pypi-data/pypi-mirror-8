<?php
/* 
   Copyright (c) 2010- Mapgears Inc., published under the BSD license.
   See http://geoprisma.org/license for the full text of the license. 
*/ 

class Layer extends org_geoprisma_widget_WidgetBase
{
    static public function getText($pstrMsg, $pstrType = null)
    {
        return parent::getText($pstrMsg, self::getType(), $pstrType);
    }

    static public function getAction()
    {
        return 'read';
    }    
     
    static public function getType()
    {
        return 'layer';
    }

    static public function getServiceType()
    {
        return null;
    }

    static public function getMandatoryResourceOptionList()
    {
        return array();
    }
}
  
?>
