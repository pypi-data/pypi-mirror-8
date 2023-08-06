/**
 * Copyright (c) 2008-2009 The Open Source Geospatial Foundation
 *
 * Published under the BSD license.
 * See http://svn.geoext.org/core/trunk/geoext/license.txt for the full text
 * of the license.
 */

/** api: (define)
 *  module = GeoExt.ux
 *  class = ShortcutCombo
 *  base_link = `Ext.form.ComboBox <http://extjs.com/deploy/dev/docs/?class=Ext.form.ComboBox>`_
 */

Ext.namespace("GeoExt.ux");

GeoExt.ux.ShortcutCombo = Ext.extend(Ext.form.ComboBox, {
    /** api: config[map]
     *  ``OpenLayers.Map or Object``  A configured map or a configuration object
     *  for the map constructor, required only if :attr:`zoom` is set to
     *  value greater than or equal to 0.
     */
    /** private: property[map]
     *  ``OpenLayers.Map``  The map object.
     */
    map: null,

    /** api: config[width]
     *  ``String`` Width of the combo. Default: 200
     */
    width: 200,

    /** api: config[store]
     *  ``Ext.data.Store``: Store containing the data.
     */
    store: null,

    /** api: config[valueField]
     *  ``String``Value field of the combo. Default: value
     */
    valueField: 'value',

    /** api: config[valueField]
     *  ``String`` Display field of the combo. Default: text
     */
    displayField:'text',

    /** api: config[bboxField]
     *  ``String`` Name of the bbox field of the store. Default: bbox
     */
    bboxField: 'bbox',

    /** api: config[bboxSrs]
     *  ``String`` EPSG code of the bbox bounds. Default: EPSG:900913
     */
    bboxSrs: 'EPSG:900913',

    /** private: property[name]
     *  ``String`` Name of the shortcut combo. Default: shortcutcombo
     */
    name: 'shortcutcombo',

    /** private: property[mode]
     *  ``String`` mode. Default: local
     */
    mode: 'local',

    /** private: property[triggerAction]
     *  ``String`` triggerAction. Default: all
     */
    triggerAction: 'all',

    /** private: property[emptyText]
     *  ``String`` Empty text. Default: Select a shortcut ...
     */
    emptyText:OpenLayers.i18n('Select a shortcut ...'),

    /** private: property[typeAhead]
     *  ``Boolean`` typeAhead. Default: true
     */
    typeAhead: true,

    /** private: property[minChars]
     *  ``Number`` Minimal number of characters
     */
    minChars: 1,

    /** private: constructor
     */
    initComponent: function() {
        GeoExt.ux.ShortcutCombo.superclass.initComponent.apply(this, arguments);
        if (!this.store) {
            this.store = GeoExt.ux.ShortcutCombo.countryStore;
        }
        this.on("select", function(combo, record, index) {
            var position = record.get(this.bboxField);
            position.transform(
                    new OpenLayers.Projection(this.bboxSrs),
                    this.map.getProjectionObject()
                    );
            this.map.zoomToExtent(position);
        }, this);
    }
});


GeoExt.ux.ShortcutCombo.countryStore = new Ext.data.SimpleStore({
    fields: ['value', 'text', 'bbox'],
    data : [
        ['AFG', 'Afghanistan', new OpenLayers.Bounds(6735414.78555975, 3425909.97755412, 8337699.23802785, 4643624.49667922)],
        ['ALB', 'Albania', new OpenLayers.Bounds(2146516.94315888, 4817778.7243703, 2343614.70406901, 5260570.02372219)],
        ['DZA', 'Algeria', new OpenLayers.Bounds(-965061.433391614, 2152155.16882998, 1334325.53216112, 4450765.83721996)],
        ['AND', 'Andorra', new OpenLayers.Bounds(159770.95901627, 5226530.62300972, 198334.262545821, 5259434.79931378)],
        ['AGO', 'Angola', new OpenLayers.Bounds(1305901.14924281, -2038921.58899498, 2678592.9738012, -489047.363957466)],
        ['ATA', 'Antarctica', new OpenLayers.Bounds(-19923956.89077, -111719615.046147, 20037508.3427892, -8516817.20787766)],
        ['ATG', 'Antigua and Barbuda', new OpenLayers.Bounds(-6889685.94114709, 1919626.12976076, -6864672.34829092, 2005385.27293209)],
        ['ARG', 'Argentina', new OpenLayers.Bounds(-8191075.18247029, -7370659.09034602, -5972321.85038066, -2486032.29977276)],
        ['ARM', 'Armenia', new OpenLayers.Bounds(4839418.92865506, 4699381.81211984, 5189993.11238345, 5056485.25211816)],
        ['AUS', 'Australia', new OpenLayers.Bounds(8152418.42936553, -7019924.134872, 17100899.6321105, -1199299.37857328)],
        ['AUT', 'Austria', new OpenLayers.Bounds(1062033.58781322, 5842663.58835182, 1912457.63257129, 6277546.0669919)],
        ['AZE', 'Azerbaijan', new OpenLayers.Bounds(4984729.11662644, 4634744.02523644, 5608831.50747271, 5145499.01708946)],
        ['BHS', 'Bahamas, The', new OpenLayers.Bounds(-8772317.63295642, 2542402.13434844, -8218657.05947683, 3114520.31320961)],
        ['BHR', 'Bahrain', new OpenLayers.Bounds(5617860.41911381, 2973162.73381166, 5634217.94316684, 3028871.23317532)],
        ['BGD', 'Bangladesh', new OpenLayers.Bounds(9800934.96909161, 2361926.94548579, 10315912.4611567, 3076731.79557665)],
        ['BRB', 'Barbados', new OpenLayers.Bounds(-6641229.50395691, 1466238.28955883, -6615624.798082, 1497681.19922562)],
        ['BEL', 'Belgium', new OpenLayers.Bounds(282937.074487083, 6361176.3332932, 712475.591910867, 6710714.34126541)],
        ['BLZ', 'Belize', new OpenLayers.Bounds(-9931677.10877215, 1791955.23510781, -9805268.94859538, 2094948.66035162)],
        ['BEN', 'Benin', new OpenLayers.Bounds(86458.1283832827, 692727.537247236, 429136.63913132, 1390503.80608573)],
        ['BMU', 'Bermuda', new OpenLayers.Bounds(-7219992.84682566, 3797567.38595641, -7199220.65973901, 3813585.32291059)],
        ['BTN', 'Bhutan', new OpenLayers.Bounds(9879665.95752566, 3086212.38082462, 10254129.2604941, 3289799.79320557)],
        ['BOL', 'Bolivia', new OpenLayers.Bounds(-7753680.42481434, -2620065.05325333, -6396263.26640826, -1083049.46496239)],
        ['BIH', 'Bosnia and Herzegovina', new OpenLayers.Bounds(1751767.99602132, 5245920.78452227, 2184054.95542465, 5664744.85106723)],
        ['BWA', 'Botswana', new OpenLayers.Bounds(2225924.39929325, -3110319.56057869, 3269512.35206824, -2013878.62909478)],
        ['BRA', 'Brazil', new OpenLayers.Bounds(-8238694.60179164, -3994978.453817, -3873857.04505326, 587886.139436941)],
        ['BRN', 'Brunei', new OpenLayers.Bounds(12700552.4045819, 448739.696580572, 12841838.6076642, 563233.986181674)],
        ['BGR', 'Bulgaria', new OpenLayers.Bounds(2489041.45850852, 5049942.60668954, 3184447.70654046, 5503133.81391586)],
        ['BFA', 'Burkina Faso', new OpenLayers.Bounds(-614557.051532805, 1050721.34029423, 267340.762381364, 1698773.19104567)],
        ['BDI', 'Burundi', new OpenLayers.Bounds(3226872.59281459, -496397.855648315, 3434638.20264732, -256041.778361828)],
        ['BLR', 'Byelarus', new OpenLayers.Bounds(2579147.97535203, 6666133.52769684, 3644388.41498943, 7591772.34074647)],
        ['KHM', 'Cambodia', new OpenLayers.Bounds(11393705.9840893, 1119988.69162323, 11982029.0512956, 1655221.10796262)],
        ['CMR', 'Cameroon', new OpenLayers.Bounds(946493.605270673, 184166.50094135, 1804089.24804506, 1469412.94973122)],
        ['CAN', 'Canada', new OpenLayers.Bounds(-15696204.4731094, 5112500.2791808, -5857260.76705283, 17926271.5198502)],
        ['CPV', 'Cape Verde', new OpenLayers.Bounds(-2823124.56570946, 1667568.5815754, -2523891.22295452, 1943146.83953034)],
        ['CAF', 'Central African Republic', new OpenLayers.Bounds(1604608.13812798, 247313.893859037, 3056616.11903696, 1232264.48431426)],
        ['TCD', 'Chad', new OpenLayers.Bounds(1498607.49671542, 832550.056350839, 2671635.50562662, 2686596.74984576)],
        ['CHL', 'Chile', new OpenLayers.Bounds(-8428617.68597182, -7502988.88849293, -7458529.0316949, -1979722.74582924)],
        ['CHN', 'China', new OpenLayers.Bounds(8195770.96390794, 2057325.20585299, 15002772.8483082, 7086113.53060628)],
        ['COL', 'Colombia', new OpenLayers.Bounds(-8799992.93299754, -470665.48621325, -7444310.89513354, 1397914.28199205)],
        ['COM', 'Comoros', new OpenLayers.Bounds(4810608.53874391, -1387941.74765406, 4956685.22024892, -1274218.60366986)],
        ['COG', 'Congo', new OpenLayers.Bounds(1240267.22095527, -559608.922114981, 2075242.38683405, 413377.145808743)],
        ['CRI', 'Costa Rica', new OpenLayers.Bounds(-9562190.70564538, 896466.256771488, -9191115.26163059, 1256339.625077)],
        ['HRV', 'Croatia', new OpenLayers.Bounds(1502411.300498, 5220833.74583371, 2162258.72448405, 5867440.11816035)],
        ['CUB', 'Cuba', new OpenLayers.Bounds(-9456962.39670612, 2251949.09957548, -8252330.1183374, 2654573.80793335)],
        ['CYP', 'Cyprus', new OpenLayers.Bounds(3592186.59582239, 4104695.31226274, 3849612.91828183, 4255534.46097832)],
        ['CZE', 'Czech Republic', new OpenLayers.Bounds(1346238.8799946, 6203145.61668524, 2098743.16350541, 6626844.28077261)],
        ['DNK', 'Denmark', new OpenLayers.Bounds(900729.270160788, 7278907.12516432, 1686490.24305308, 7913764.41420483)],
        ['DJI', 'Djibouti', new OpenLayers.Bounds(4648669.47526909, 1228798.99510308, 4833491.23711155, 1426485.20621399)],
        ['DMA', 'Dominica', new OpenLayers.Bounds(-6845036.52502478, 1712260.23385931, -6818721.80408713, 1761688.59383014)],
        ['DOM', 'Dominican Republic', new OpenLayers.Bounds(-8014059.76446653, 1992922.69070469, -7605597.27131684, 2264542.49854002)],
        ['ECU', 'Ecuador', new OpenLayers.Bounds(-10204226.0726277, -557677.926739779, -8373297.66070089, 160085.975131334)],
        ['EGY', 'Egypt', new OpenLayers.Bounds(2750301.7349117, 2511124.26061263, 3986689.56435642, 3716059.6310848)],
        ['SLV', 'El Salvador', new OpenLayers.Bounds(-10030534.816054, 1477635.991718, -9762192.43665511, 1626085.86378217)],
        ['GNQ', 'Equatorial Guinea', new OpenLayers.Bounds(1041671.93126598, 111541.574960176, 1263909.29996641, 261235.775199839)],
        ['ERI', 'Eritrea', new OpenLayers.Bounds(4056853.23587017, 1387149.6540853, 4800508.23475634, 2038590.26393837)],
        ['EST', 'Estonia', new OpenLayers.Bounds(2430320.41012906, 7867733.85807103, 3138530.497374, 8326260.27291218)],
        ['ETH', 'Ethiopia', new OpenLayers.Bounds(3672366.49059259, 379451.967866755, 5342158.8524917, 1675790.22282219)],
        ['FLK', 'Falkland Islands (Islas Malvinas)', new OpenLayers.Bounds(-6793918.83770891, -7340492.54088633, -3983322.0886103, -6667166.91670909)],
        ['FRO', 'Faroe Islands', new OpenLayers.Bounds(-805118.225655354, 8843348.92663514, -731090.768524329, 8937883.04809889)],
        ['FJI', 'Fiji', new OpenLayers.Bounds(19732081.2651673, -2173947.3778138, 20036339.7055568, -1822412.00717268)],
        ['FIN', 'Finland', new OpenLayers.Bounds(2187242.16717906, 8356448.20034725, 3516282.07883426, 11094615.0047243)],
        ['FRA', 'France', new OpenLayers.Bounds(-533282.249413682, 5066533.57806705, 1062327.97653466, 6637423.89052797)],
        ['GUF', 'French Guiana', new OpenLayers.Bounds(-6079754.09363548, 235277.545810234, -5749589.44575954, 641195.21169742)],
        ['PYF', 'French Polynesia', new OpenLayers.Bounds(-16658037.0790312, -2022436.12376713, -16603179.0731312, -1979042.38266098)],
        ['GAB', 'Gabon', new OpenLayers.Bounds(969190.519194564, -437036.603803325, 1616204.27229407, 258028.337943903)],
        ['GMB', 'Gambia, The', new OpenLayers.Bounds(-1873105.09018406, 1463970.06866895, -1536054.20919741, 1554305.04438309)],
        ['ISR', 'Gaza Strip', new OpenLayers.Bounds(3809072.41708, 3660866.70239163, 3847044.63413145, 3710481.73688768)],
        ['GEO', 'Georgia', new OpenLayers.Bounds(4453504.50954918, 5019719.33948443, 5199822.48957077, 5401058.85799866)],
        ['DEU', 'Germany', new OpenLayers.Bounds(653383.399294069, 5988078.25696614, 1674028.0348915, 7345851.68180831)],
        ['GHA', 'Ghana', new OpenLayers.Bounds(-361695.505937534, 526891.982866847, 134011.972431149, 1251011.95658533)],
        ['GRC', 'Greece', new OpenLayers.Bounds(2184923.364996, 4154370.97544745, 3143909.54091449, 5122772.92486363)],
        ['GRL', 'Greenland', new OpenLayers.Bounds(-8131118.82678371, 8353374.64315889, -1353119.59265328, 18417816.4578079)],
        ['GRD', 'Grenada', new OpenLayers.Bounds(-6878397.89067, 1345298.69426215, -6856880.01790741, 1372783.56030264)],
        ['GLP', 'Guadeloupe', new OpenLayers.Bounds(-6877720.99831952, 1798933.18760379, -6802725.23266767, 1864279.15364723)],
        ['GTM', 'Guatemala', new OpenLayers.Bounds(-10268771.1979123, 1545031.05653343, -9819832.75038465, 2016620.33823832)],
        ['GIN', 'Guinea', new OpenLayers.Bounds(-1678543.23384982, 357925.135121425, 997576.895923814, 1421602.41012783)],
        ['GNB', 'Guinea-Bissau', new OpenLayers.Bounds(-1856565.39121362, 1223476.82224995, -1518862.03526052, 1423734.95598374)],
        ['GUY', 'Guyana', new OpenLayers.Bounds(-6833903.47185504, 131984.795416641, -6286312.84772161, 953487.516984117)],
        ['HTI', 'Haiti', new OpenLayers.Bounds(-8290737.17714976, 2040213.89688907, -7973752.82085113, 2265068.28235278)],
        ['HND', 'Honduras', new OpenLayers.Bounds(-9946939.03541975, 1458293.88378247, -9254085.78413255, 1807070.19476634)],
        ['HGK', 'Hong Kong', new OpenLayers.Bounds(12670595.8838966, 2528808.63530496, 12746360.2663329, 2584687.15936697)],
        ['HUN', 'Hungary', new OpenLayers.Bounds(1792989.74223774, 5742027.84279893, 2548644.0806142, 6203191.18619581)],
        ['ISL', 'Iceland', new OpenLayers.Bounds(-2728997.24885308, 9199696.84916062, -1502565.97931774, 10024665.9191822)],
        ['IND', 'India', new OpenLayers.Bounds(7585307.48680869, 753026.007010671, 10841864.6118829, 4298708.81787947)],
        ['IDN', 'Indonesia', new OpenLayers.Bounds(10597458.9125417, -1224169.56529549, 15696972.2405935, 630411.900132674)],
        ['IRN', 'Iran', new OpenLayers.Bounds(4901860.33706122, 2884992.64649026, 7051191.43681147, 4834102.08013569)],
        ['IRQ', 'Iraq', new OpenLayers.Bounds(4318589.75742459, 3388909.99976076, 5404024.85993493, 4492827.68740911)],
        ['ISA', 'Iraq-Saudi Arabia Neutral Zone', new OpenLayers.Bounds(4977638.73295268, 3347003.9692606, 5180988.4058013, 3436170.05190589)],
        ['IRL', 'Ireland', new OpenLayers.Bounds(-1165824.5621331, 6700536.21871318, -605083.318852093, 7435421.5026687)],
        ['XIM', 'Isle of Man', new OpenLayers.Bounds(-532571.013481742, 7180945.63843105, -479632.479373328, 7248030.42320779)],
        ['ISR', 'Israel', new OpenLayers.Bounds(3814593.71842314, 3438645.77712569, 3970733.75935205, 3933896.36962391)],
        ['ITA', 'Italy', new OpenLayers.Bounds(736954.178650307, 4390548.00942443, 2060616.16147168, 5956865.34760555)],
        ['CIV', 'Ivory Coast', new OpenLayers.Bounds(-958089.73943677, 484457.362849457, -276969.120800544, 1202062.73658205)],
        ['JAM', 'Jamaica', new OpenLayers.Bounds(-8724418.79383167, 2002073.36327263, -8481276.8533581, 2098732.16958627)],
        ['SJM', 'Jan Mayen', new OpenLayers.Bounds(-1015233.84945769, 11336479.760051, -883010.901597936, 11464382.8399251)],
        ['JPN', 'Japan', new OpenLayers.Bounds(14210244.8628368, 3008853.8921796, 16232418.7195331, 5701459.44916573)],
        ['JOR', 'Jordan', new OpenLayers.Bounds(3883316.97660387, 3399708.37901213, 4375199.02057259, 3945482.86205498)],
        ['KAZ', 'Kazakhstan', new OpenLayers.Bounds(5176267.14535422, 4952214.6346537, 9723237.57914004, 7448655.7693652)],
        ['KEN', 'Kenya', new OpenLayers.Bounds(3774532.22259856, -520787.275814044, 4665804.95841, 515086.659271984)],
        ['KGL', 'Kerguelen', new OpenLayers.Bounds(7653367.86609413, -6398021.34868423, 7855659.31075116, -6216149.24907839)],
        ['KIR', 'Kiribati', new OpenLayers.Bounds(-17540400.6545459, 189827.75502545, -17498433.328816, 225654.479445488)],
        ['PRK', 'Korea, Peoples Republic of', new OpenLayers.Bounds(13839639.9311961, 4534356.79103051, 14548877.8841464, 5309010.49247087)],
        ['KOR', 'Korea, Republic of', new OpenLayers.Bounds(14040014.5050438, 3920586.37119338, 14425425.2890633, 4667745.83202913)],
        ['KWT', 'Kuwait', new OpenLayers.Bounds(5180988.4058013, 3317780.00871377, 5390059.81486723, 3514336.33038399)],
        ['KGZ', 'Kyrgyzstan', new OpenLayers.Bounds(7708785.5609012, 4749196.75904311, 8937338.3826216, 5352945.35182865)],
        ['LAO', 'Laos', new OpenLayers.Bounds(11142223.9145295, 1565039.96039652, 11988574.6088178, 2571763.01874238)],
        ['LVA', 'Latvia', new OpenLayers.Bounds(2336255.51684578, 7494194.48008548, 3143417.58370745, 7984794.41329412)],
        ['LBN', 'Lebanon', new OpenLayers.Bounds(3906986.97636284, 3903674.6855732, 4077074.22705286, 4121717.93910171)],
        ['LSO', 'Lesotho', new OpenLayers.Bounds(3007264.97637479, -3588528.27266605, 3278976.7424455, -3320960.01601648)],
        ['LBR', 'Liberia', new OpenLayers.Bounds(-1280029.4445816, 484867.641866224, -820177.275690388, 957549.012940726)],
        ['LBY', 'Libya', new OpenLayers.Bounds(1035703.89795754, 2213627.74731368, 2797929.6472362, 3917329.09776394)],
        ['LIE', 'Liechtenstein', new OpenLayers.Bounds(1054844.57914046, 5950181.08150514, 1073225.56119226, 5985760.64946456)],
        ['LTU', 'Lithuania', new OpenLayers.Bounds(2185926.38866716, 7149086.51974605, 2985555.37406625, 7648645.28391285)],
        ['LUX', 'Luxembourg', new OpenLayers.Bounds(637984.363726975, 6351276.87610028, 726050.436565427, 6476153.2868145)],
        ['MAC', 'Macau', new OpenLayers.Bounds(12637823.0833692, 2522538.43240082, 12646327.9767164, 2537285.9732333)],
        ['MKD', 'Macedonia', new OpenLayers.Bounds(2277873.97626695, 4991275.16218432, 2563842.52206332, 5215270.17856485)],
        ['MDG', 'Madagascar', new OpenLayers.Bounds(4811350.82721859, -2949657.64075287, 5621571.86148722, -1339765.97195739)],
        ['MWI', 'Malawi', new OpenLayers.Bounds(3639000.8784458, -1936639.96723567, 3999059.19878375, -1048120.58128271)],
        ['MYS', 'Malaysia', new OpenLayers.Bounds(11092645.1593831, 94996.1199037307, 13277721.6107608, 821199.824615211)],
        ['MDV', 'Maldives', new OpenLayers.Bounds(8091101.49457548, -76901.3686306621, 8210213.31575227, 791995.100341978)],
        ['MLI', 'Mali', new OpenLayers.Bounds(-1363190.70194255, 1134937.9493826, 473386.140968148, 2875777.89141098)],
        ['MLT', 'Malta', new OpenLayers.Bounds(1578599.48379109, 4273136.35767069, 1621924.94688598, 4310946.27484736)],
        ['MTQ', 'Martinique', new OpenLayers.Bounds(-6816031.22069149, 1620498.44989119, -6769339.23731334, 1675406.63662633)],
        ['MRT', 'Mauritania', new OpenLayers.Bounds(-1898481.5465995, 1657590.8855335, -535044.759890891, 3158522.74542855)],
        ['MUS', 'Mauritius', new OpenLayers.Bounds(6379317.17723744, -2333051.92074832, 6432688.05828709, -2273163.56106568)],
        ['MEX', 'Mexico', new OpenLayers.Bounds(-13038139.0879043, 1637172.45024535, -9656410.38391094, 3857974.92132223)],
        ['MDA', 'Moldova', new OpenLayers.Bounds(2964994.66275785, 5692359.59327221, 3354523.70400131, 6188209.40517125)],
        ['MCO', 'Monaco', new OpenLayers.Bounds(822250.311595005, 5423450.39062993, 828294.888094273, 5430396.04368589)],
        ['MNG', 'Mongolia', new OpenLayers.Bounds(9769332.50439726, 5098476.85004068, 13350324.048127, 6825843.47749356)],
        ['MAR', 'Morocco', new OpenLayers.Bounds(-1466849.1854134, 3206813.17457209, -112494.577399984, 4288969.15096743)],
        ['MOZ', 'Mozambique', new OpenLayers.Bounds(3363270.22328792, -3106026.28560258, 4546194.59794873, -1173239.28296739)],
        ['MMR', 'Myanmar (Burma)', new OpenLayers.Bounds(10262911.0257438, 1117256.83709456, 11261257.6000774, 3318107.03949792)],
        ['NAM', 'Namibia', new OpenLayers.Bounds(1306148.29563426, -3370661.60320647, 2812570.52302899, -1917203.86514446)],
        ['NPL', 'Nepal', new OpenLayers.Bounds(8911771.04596053, 3042217.98082958, 9817911.63307375, 3557614.56324198)],
        ['NLD', 'Netherlands', new OpenLayers.Bounds(374466.408222724, 6578258.08561513, 802551.640105601, 7069631.21592828)],
        ['NCL', 'New Caledonia', new OpenLayers.Bounds(18255528.5051757, -2558983.69343876, 18717938.5542884, -2283367.46695268)],
        ['NZL', 'New Zealand', new OpenLayers.Bounds(-19686796.5724099, -6595587.92424221, 19877174.0322583, -4082416.9118648)],
        ['NIC', 'Nicaragua', new OpenLayers.Bounds(-9761638.6928502, 1199204.19120491, -9254085.78413255, 1692049.21794143)],
        ['NER', 'Niger', new OpenLayers.Bounds(18553.2523360548, 1310640.67895566, 1780740.0714798, 2695307.78944936)],
        ['NGA', 'Nigeria', new OpenLayers.Bounds(298573.22408567, 477108.025632299, 1633520.01942669, 1561958.51027947)],
        ['MNP', 'Northern Mariana Islands', new OpenLayers.Bounds(16099358.8392948, 1486879.18014148, 16136126.7485006, 1532341.90039579)],
        ['NOR', 'Norway', new OpenLayers.Bounds(550907.778835929, 7966498.6011469, 3458046.40558442, 11455374.1064673)],
        ['OMN', 'Oman', new OpenLayers.Bounds(5777943.33675177, 1879407.31194106, 6660924.3535949, 2880562.78653552)],
        ['PAK', 'Pakistan', new OpenLayers.Bounds(6775669.07255566, 2715441.37172695, 8664153.2928307, 4447858.25220322)],
        ['PAN', 'Panama', new OpenLayers.Bounds(-9243044.0307466, 804272.544192601, -8587927.74032378, 1075992.10413412)],
        ['PNG', 'Papua New Guinea', new OpenLayers.Bounds(15679339.0674684, -1302523.95295372, 17118300.0969495, -217176.859354612)],
        ['PRY', 'Paraguay', new OpenLayers.Bounds(-6972903.78314148, -3196892.56827088, -6038309.93689925, -2189895.43784222)],
        ['PER', 'Peru', new OpenLayers.Bounds(-9056552.96913642, -2078320.66014749, -7646257.52386298, -4174.48136866249)],
        ['PHL', 'Philippines', new OpenLayers.Bounds(13043794.5786971, 563047.796851762, 14092824.847886, 2113478.27951449)],
        ['POL', 'Poland', new OpenLayers.Bounds(1573315.13723564, 6275939.17446196, 2687776.88274967, 7330227.69689361)],
        ['PRT', 'Portugal', new OpenLayers.Bounds(-3178110.2275953, 3847284.99642961, -689562.371813184, 5183807.1386899)],
        ['PRI', 'Puerto Rico', new OpenLayers.Bounds(-7487256.61482541, 2029128.53259254, -7305435.00634315, 2097493.68485702)],
        ['QAT', 'Qatar', new OpenLayers.Bounds(5649741.45431125, 2821256.76231479, 5745383.71060323, 3018014.38532388)],
        ['REU', 'Reunion', new OpenLayers.Bounds(6147214.86689903, -2436484.83848246, 6217347.11430115, -2375855.3181112)],
        ['ROM', 'Romania', new OpenLayers.Bounds(2255459.87934772, 5407545.93882423, 3306312.53468598, 6149102.00072294)],
        ['RUS', 'Russia', new OpenLayers.Bounds(-20030511.8068002, 5041309.29246384, 20037508.3427892, 16850435.7559737)],
        ['RWA', 'Rwanda', new OpenLayers.Bounds(3211936.79748767, -314790.860132183, 3437143.00159921, -118185.985805185)],
        ['SMR', 'San Marino', new OpenLayers.Bounds(1380762.40695738, 5449300.13345852, 1392796.03694787, 5463771.10213827)],
        ['STP', 'Sao Tome and Principe', new OpenLayers.Bounds(719680.418801981, 2226.38981131462, 830910.945387333, 189482.507846741)],
        ['SAU', 'Saudi Arabia', new OpenLayers.Bounds(3851992.65776244, 1701367.38740766, 6291003.95800753, 3794505.54117183)],
        ['SEN', 'Senegal', new OpenLayers.Bounds(-1950317.52965617, 1380027.84304029, -1264403.48658679, 1885123.36110374)],
        ['SYC', 'Seychelles', new OpenLayers.Bounds(6164283.25531511, -533753.189832485, 6210826.18648811, -476891.167501173)],
        ['SLE', 'Sierra Leone', new OpenLayers.Bounds(-1480374.50524338, 771447.795130719, -1142863.72813655, 1118606.89244609)],
        ['SGP', 'Singapore', new OpenLayers.Bounds(11538042.8739005, 140242.910252002, 11577004.5258181, 158678.590234859)],
        ['SVK', 'Slovakia', new OpenLayers.Bounds(1874712.60335391, 6063844.62579181, 2511145.13616289, 6378192.22940088)],
        ['SVN', 'Slovenia', new OpenLayers.Bounds(1489794.30735414, 5688773.91210348, 1848931.66766379, 5921284.09859519)],
        ['SLB', 'Solomon Islands', new OpenLayers.Bounds(17202601.6461449, -1328169.05392285, 18076793.2540355, -559385.175752547)],
        ['SOM', 'Somalia', new OpenLayers.Bounds(4562575.05311024, -186415.547602249, 6070652.5668175, 1426936.89802737)],
        ['ZAF', 'South Africa', new OpenLayers.Bounds(1833400.93746672, -4138768.5305148, 3661641.95087403, -2527874.76471453)],
        ['ESP', 'Spain', new OpenLayers.Bounds(-2003195.39187339, 3215569.06196124, 482755.462791473, 5430600.70086312)],
        ['LKA', 'Sri Lanka', new OpenLayers.Bounds(8871974.53183401, 662829.413898473, 9116012.48413915, 1099239.11708909)],
        ['STC', 'St. Christopher-Nevis', new OpenLayers.Bounds(-6997977.2516698, 1931502.02942253, -6961275.16323836, 1968697.58082148)],
        ['LCA', 'St. Lucia', new OpenLayers.Bounds(-6799364.55132407, 1541857.93375842, -6778492.14680033, 1586233.55809981)],
        ['VCT', 'St. Vincent and the Grenadines', new OpenLayers.Bounds(-6841619.36521027, 1411451.83375319, -6803880.70574525, 1503660.57105925)],
        ['SDN', 'Sudan', new OpenLayers.Bounds(2429909.77342711, 388984.161784817, 4299305.54448855, 2647505.46074106)],
        ['SUR', 'Suriname', new OpenLayers.Bounds(-6464508.79316221, 205914.929006624, -6009520.3548458, 668861.112860009)],
        ['SJM', 'Svalbard', new OpenLayers.Bounds(1188798.66644706, 12656010.254419, 3743116.60397335, 15876436.3510106)],
        ['SWZ', 'Swaziland', new OpenLayers.Bounds(3428887.37789425, -3163091.42868416, 3577165.02116372, -2965473.42595357)],
        ['SWE', 'Sweden', new OpenLayers.Bounds(1236418.93506873, 7428078.05639065, 2690265.96964574, 10770428.1334595)],
        ['CHE', 'Switzerland', new OpenLayers.Bounds(664113.512545949, 5752170.52507755, 1167586.75412269, 6074701.90679696)],
        ['SYR', 'Syria', new OpenLayers.Bounds(3961920.99464093, 3804546.08217219, 4717035.60266767, 4484110.41415169)],
        ['TWN', 'Taiwan', new OpenLayers.Bounds(13364272.1071884, 2499889.13770255, 13580888.7002464, 2910687.91819459)],
        ['TJK', 'Tajikistan', new OpenLayers.Bounds(7499226.65345487, 4393515.14094811, 8369830.816818, 5019763.82403953)],
        ['TZA', 'Tanzania, United Republic of', new OpenLayers.Bounds(3266267.38789246, -1314649.13719862, 4503242.93315466, -111055.833937885)],
        ['THA', 'Thailand', new OpenLayers.Bounds(10836485.9929926, 627956.938010402, 11759167.5530267, 2327042.70937571)],
        ['TGO', 'Togo', new OpenLayers.Bounds(-16804.2444068111, 680234.824695828, 200370.181372641, 1247904.1694487)],
        ['TON', 'Tonga', new OpenLayers.Bounds(-19521052.218877, -2446120.31310406, -19359138.2097614, -2104152.08319677)],
        ['TTO', 'Trinidad and Tobago', new OpenLayers.Bounds(-6893398.23282081, 1123191.24208842, -6782511.88518781, 1213809.63781971)],
        ['TUN', 'Tunisia', new OpenLayers.Bounds(833968.42651874, 3533929.28315963, 1289450.41448029, 4486330.44788331)],
        ['TUR', 'Turkey', new OpenLayers.Bounds(2898014.80579726, 4276109.60383115, 4989554.41636202, 5177052.2730324)],
        ['TKM', 'Turkmenistan', new OpenLayers.Bounds(5837963.81461208, 4183676.85275867, 7421704.21936804, 5281199.99167912)],
        ['TCA', 'Turks and Caicos Islands', new OpenLayers.Bounds(-8204928.1198965, 2381778.28592368, -8126633.671824, 2431569.02395812)],
        ['UGA', 'Uganda', new OpenLayers.Bounds(3292644.5324032, -163038.917649542, 3899086.36018925, 470389.989589624)],
        ['UKR', 'Ukraine', new OpenLayers.Bounds(2465888.04566571, 5526814.70026639, 4472783.62668333, 6869073.36660457)],
        ['ARE', 'United Arab Emirates', new OpenLayers.Bounds(5657935.50374342, 2518389.29062686, 6275727.59325458, 3009438.73839203)],
        ['GBR', 'United Kingdom', new OpenLayers.Bounds(-837029.835664101, 6438532.79627311, 193974.20686834, 8541605.7994741)],
        ['USA', 'United States', new OpenLayers.Bounds(-19838714.3168264, 2146075.00656018, 19971050.5931969, 11542768.518094)],
        ['URY', 'Uruguay', new OpenLayers.Bounds(-6505357.59037812, -4160861.86156838, -5910508.49955691, -3516482.3555108)],
        ['UZB', 'Uzbekistan', new OpenLayers.Bounds(6233579.79120798, 4464961.30561161, 8145280.90952432, 5711812.05552908)],
        ['VUT', 'Vanuatu', new OpenLayers.Bounds(18454266.4773178, -2230465.46310148, 18866861.6657967, -1194893.70067342)],
        ['VEN', 'Venezuela', new OpenLayers.Bounds(-8169058.77042321, 72328.2701228347, -6657060.46181508, 1367940.63458753)],
        ['VNM', 'Vietnam', new OpenLayers.Bounds(11370228.7755017, 958054.042939614, 12184931.1428786, 2677531.44427983)],
        ['ESH', 'Western Sahara', new OpenLayers.Bounds(-1900625.6052429, 2364482.80974544, -964830.848356287, 3207287.13294365)],
        ['WSM', 'Western Samoa', new OpenLayers.Bounds(-19233224.3423676, -1580304.63850573, -19084246.8756392, -1512399.60434513)],
        ['YEM', 'Yemen', new OpenLayers.Bounds(4743755.43985522, 1414037.6911714, 5908643.86071691, 2154804.09916493)],
        ['KOS', 'Kosovo', new OpenLayers.Bounds(2054367.85905953, 5138434.88528812, 2269943.61538574, 5397002.49305309)],
        ['ZAR', 'Zaire', new OpenLayers.Bounds(1359173.08680585, -1511414.11516366, 3484608.48523859, 596146.858993261)],
        ['ZMB', 'Zambia', new OpenLayers.Bounds(2448842.80068319, -2046361.73062326, 3750691.93812657, -914921.134426212)],
        ['ZWE', 'Zimbabwe', new OpenLayers.Bounds(2809332.14093064, -2561561.65292428, 3681673.97273679, -1760308.45493511)],
        ['SMO', 'Serbia and Montenegro', new OpenLayers.Bounds(2095934.52736608, 5139403.49214837, 2561120.93920621, 5808436.23052965)]
    ]
});

/** api: xtype = gxux_shortcutcombo */
Ext.reg('gxux_shortcutcombo', GeoExt.ux.ShortcutCombo);
