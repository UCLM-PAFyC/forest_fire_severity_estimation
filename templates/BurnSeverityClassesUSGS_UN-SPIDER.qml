<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="AllStyleCategories" maxScale="0" hasScaleBasedVisibilityFlag="0" version="3.22.3-Białowieża" minScale="1e+08">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
    <Private>0</Private>
  </flags>
  <temporal enabled="0" mode="0" fetchMode="0">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <customproperties>
    <Option type="Map">
      <Option type="QString" value="false" name="WMSBackgroundLayer"/>
      <Option type="QString" value="false" name="WMSPublishDataSourceUrl"/>
      <Option type="QString" value="0" name="embeddedWidgets/count"/>
      <Option type="QString" value="Value" name="identify/format"/>
    </Option>
  </customproperties>
  <pipe-data-defined-properties>
    <Option type="Map">
      <Option type="QString" value="" name="name"/>
      <Option name="properties"/>
      <Option type="QString" value="collection" name="type"/>
    </Option>
  </pipe-data-defined-properties>
  <pipe>
    <provider>
      <resampling maxOversampling="2" zoomedInResamplingMethod="nearestNeighbour" enabled="false" zoomedOutResamplingMethod="nearestNeighbour"/>
    </provider>
    <rasterrenderer type="singlebandpseudocolor" nodataColor="" band="1" opacity="1" alphaBand="-1" classificationMin="-77.6797638" classificationMax="700.1868286">
      <rasterTransparency/>
      <minMaxOrigin>
        <limits>MinMax</limits>
        <extent>WholeRaster</extent>
        <statAccuracy>Estimated</statAccuracy>
        <cumulativeCutLower>0.02</cumulativeCutLower>
        <cumulativeCutUpper>0.98</cumulativeCutUpper>
        <stdDevFactor>2</stdDevFactor>
      </minMaxOrigin>
      <rastershader>
        <colorrampshader classificationMode="1" minimumValue="-77.679763800000003" colorRampType="DISCRETE" clip="0" maximumValue="700.18682860000001" labelPrecision="4">
          <colorramp type="gradient" name="[source]">
            <Option type="Map">
              <Option type="QString" value="38,126,64,255" name="color1"/>
              <Option type="QString" value="244,81,156,255" name="color2"/>
              <Option type="QString" value="0" name="discrete"/>
              <Option type="QString" value="gradient" name="rampType"/>
              <Option type="QString" value="-0.0299797;50,180,113,255:0.227134;12,242,54,255:0.44568;255,255,0,255:0.664227;253,191,111,255:0.8;255,127,0,255" name="stops"/>
            </Option>
            <prop k="color1" v="38,126,64,255"/>
            <prop k="color2" v="244,81,156,255"/>
            <prop k="discrete" v="0"/>
            <prop k="rampType" v="gradient"/>
            <prop k="stops" v="-0.0299797;50,180,113,255:0.227134;12,242,54,255:0.44568;255,255,0,255:0.664227;253,191,111,255:0.8;255,127,0,255"/>
          </colorramp>
          <item value="-251" color="#267e40" label="Enhanced Regrowth, high (post fire)" alpha="255"/>
          <item value="-101" color="#32b471" label="Enhanced Regrowth, low (post fire)" alpha="255"/>
          <item value="99" color="#0cf236" label="Unburned" alpha="255"/>
          <item value="269" color="#ffff00" label="Low Severity" alpha="255"/>
          <item value="439" color="#fdbf6f" label="Moderate-low Severity" alpha="255"/>
          <item value="544.6135101318359" color="#ff7f00" label="Miderate-hig Severity" alpha="255"/>
          <item value="1300" color="#f4519c" label="High Severity" alpha="255"/>
          <rampLegendSettings minimumLabel="" direction="0" useContinuousLegend="1" orientation="2" maximumLabel="" prefix="" suffix="">
            <numericFormat id="basic">
              <Option type="Map">
                <Option type="QChar" value="" name="decimal_separator"/>
                <Option type="int" value="6" name="decimals"/>
                <Option type="int" value="0" name="rounding_type"/>
                <Option type="bool" value="false" name="show_plus"/>
                <Option type="bool" value="true" name="show_thousand_separator"/>
                <Option type="bool" value="false" name="show_trailing_zeros"/>
                <Option type="QChar" value="" name="thousand_separator"/>
              </Option>
            </numericFormat>
          </rampLegendSettings>
        </colorrampshader>
      </rastershader>
    </rasterrenderer>
    <brightnesscontrast gamma="1" contrast="0" brightness="0"/>
    <huesaturation invertColors="0" colorizeRed="255" colorizeGreen="128" colorizeStrength="100" saturation="0" colorizeBlue="128" grayscaleMode="0" colorizeOn="0"/>
    <rasterresampler maxOversampling="2"/>
    <resamplingStage>resamplingFilter</resamplingStage>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
