<?php
/* 
   Copyright (c) 2010- Groupe Nippour, published under the BSD license.
   See http://geoprisma.org/license for the full text of the license. 
*/ 

class LiveMarker extends org_geoprisma_widget_WidgetBase
{
     static public function getText($pstrMsg)
     {
        return parent::getText($pstrMsg, self::getType());
     }
     
     static public function getAction()
     {
        return 'read';
     }    
     
     static public function getType()
     {
        return 'livemarker';
     }

     static public function getServiceType()
     {
        return null;
     }

	static public function methodManager()
	{
		switch ($_REQUEST['method']){
			case "getdata":
			self::getData(func_get_arg(0));
			break;
		}        
	}
    
    static public function getProcessList()
    {
        return array(
            "getData"
        );	
    }
	
	static public function getData()
	{
        $pobjWidget = func_get_arg(0);
        $url = $pobjWidget->getOption("url")->getValue();//(string)simplexml_load_string($pobjWidget->getOption("url")->getValue());

		if (substr($url,0,4) != "http")
		{
			$url = "http://" . $_SERVER['SERVER_NAME'] . str_replace("proxy.php",$url,$_SERVER['PHP_SELF']);
		}

        ob_start();
        $objCurl = curl_init();
        curl_setopt($objCurl, CURLOPT_URL, $url);
        curl_setopt($objCurl,CURLOPT_RETURNTRANSFER,1);
        $result = curl_exec($objCurl);
        curl_close($objCurl);
        ob_end_flush();

		$result =  str_replace('\n',"",$result);
		$result =  str_replace('\r',"",$result);
//test 2 vehicules        
//echo "[{fid:12028, lon:-71.6369180000, lat:48.733380000, londms:'-71&deg; 38&prime; 12.9&Prime;', latdms:'48&deg; 34&prime; 24.02&Prime;', orgt: '2011-01-13 09:46:30'},{fid:666, lon:-71.6369180000, lat:48.353380000, londms:'-71&deg; 38&prime; 12.9&Prime;', latdms:'48&deg; 34&prime; 24.02&Prime;', orgt: '2091-01-13 09:46:30'}]";
		echo html_entity_decode(htmlentities($result),ENT_QUOTES,"utf-8");

	}
}
  
?>
