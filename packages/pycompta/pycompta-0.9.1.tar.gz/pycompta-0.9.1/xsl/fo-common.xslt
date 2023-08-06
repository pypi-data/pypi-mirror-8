<?xml version="1.0" encoding="ISO-8859-1"?>


<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
                version="1.0"
                xmlns:fo="http://www.w3.org/1999/XSL/Format">

  <xsl:output method="xml" 
              version="1.0"
              encoding="ISO-8859-1" 
              indent="yes"/>

<!-- document ***************************************** -->

<xsl:template match="/">
  <fo:root>
    <fo:layout-master-set>
      <fo:simple-page-master 
            master-name="A4" 
            page-width="21cm" page-height="29.7cm"
            margin-top="1cm" margin-bottom="1cm"
            margin-left="1cm" margin-right="1cm">
        <fo:region-body margin-right="0.5cm"
                        margin-left="0.5cm"
                        margin-top="1.5cm"
                        margin-bottom="1.5cm"/>
        <fo:region-before extent="1cm"/>
        <fo:region-after extent="1cm"/>
      </fo:simple-page-master>
    </fo:layout-master-set>
    <xsl:apply-templates/>
  </fo:root>
</xsl:template>


<!-- page titre ***************************************** -->

<xsl:template name="titlepage">
  <xsl:param name="type-doc" select="'NomManquant'"/>
  <fo:block>
    <xsl:if test="$societe/logo">
      <fo:external-graphic src="file:{$societe/logo}"
                           content-width="4cm"/>
    </xsl:if>
  </fo:block>
  <fo:block font-size="18pt" 
            font-family="sans-serif"
            space-before="6cm"
            font-style="italic"
            text-align="center">
    <xsl:text>Comptabilité </xsl:text><xsl:value-of select="$societe/nom"/>
  </fo:block>
  <fo:block font-size="20pt" 
            font-family="sans-serif"
            space-before="3cm"
            font-weight="bold"
            text-align="center">
    <xsl:choose>
      <xsl:when test="$exercice">
        <xsl:text>Exercice</xsl:text>
      </xsl:when>
      <xsl:otherwise>
        <xsl:text>Période</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
    <xsl:text> du </xsl:text>
    <xsl:value-of select="@debut"/> 
    <xsl:text> au </xsl:text>
    <xsl:value-of select="@fin"/>
  </fo:block>
  <fo:block font-size="20pt" 
            font-family="sans-serif"
            space-before="1cm"
            font-weight="bold"
            text-align="center">
     <xsl:value-of select="$type-doc"/>
  </fo:block>

</xsl:template>

<!-- pied de page ***************************************** -->

<xsl:template name="footer">
<xsl:for-each select="$societe/bas-page/ligne">
  <fo:block font-size="7pt"
            font-style="italic"
            text-align="center">
    <xsl:value-of select="."/>
  </fo:block>
</xsl:for-each>
</xsl:template>


</xsl:stylesheet>
