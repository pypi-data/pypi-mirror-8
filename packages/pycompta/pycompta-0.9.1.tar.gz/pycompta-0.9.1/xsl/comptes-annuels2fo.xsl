<?xml version="1.0" encoding="UTF-8"?>


<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
                version="1.0"
                xmlns:fo="http://www.w3.org/1999/XSL/Format"
		xmlns:ldg="http://www.logilab.org/2005/DocGenerator"
		exclude-result-prefixes="ldg">

  <xsl:import href="bilan2fo.xsl"/>
  <xsl:import href="compte-resultat-1col2fo.xsl"/>
  <xsl:import href="immo2fo.xsl"/>

  <xsl:output method="xml" 
              version="1.0"
              encoding="ISO-8859-1" 
              indent="yes"/>

  <xsl:param name="societe.def" select="'../xml/societe.xml'"/>
  <xsl:param name="exercice" select="true()"/>

  <xsl:variable name="societe" select="document($societe.def)/societe"/>
  <xsl:variable name="plan_comptable" select="document($societe/plan-comptable/text())/plan-comptable"/>

<!-- <comptes-annuels> ****************************** -->
<xsl:template match="comptes-annuels">
  <fo:page-sequence master-reference="A4">

    <fo:static-content flow-name="xsl-region-after">
      <xsl:call-template name="footer"/>
    </fo:static-content>

    <fo:flow flow-name="xsl-region-body">
      <xsl:call-template name="comptes-annuels.titlepage"/>
    </fo:flow>

  </fo:page-sequence>

  <fo:page-sequence master-reference="A4">

    <fo:static-content flow-name="xsl-region-before">
      <fo:table table-layout="fixed" width="18cm">
        <fo:table-column column-number="1"
                         column-width="2cm"/>
        <fo:table-column column-number="2"
                         column-width="14cm"/>
        <fo:table-column column-number="3"
                         column-width="2cm"/>
        <fo:table-body>
          <fo:table-row>
            <fo:table-cell>
              <fo:block>
                <xsl:if test="$societe/logo">
                <fo:external-graphic src="file:{$societe/logo}"
                                     content-width="1.5cm"/>
                </xsl:if>
              </fo:block>
            </fo:table-cell>
            <fo:table-cell>
              <fo:block font-size="7pt"
                        font-style="italic"
                        text-align="center"
                        space-before="0.5cm">
                <xsl:text>Exercice du </xsl:text>
                <xsl:value-of select="@debut"/>
                <xsl:text> au </xsl:text>
                <xsl:value-of select="@fin"/>
                <xsl:text> - Comptes Annuels</xsl:text>
              </fo:block>
            </fo:table-cell>
            <fo:table-cell>
              <fo:block font-size="7pt"
                        text-align="end"
                        space-before="0.5cm">
                <fo:page-number/>
              </fo:block>
            </fo:table-cell>
          </fo:table-row>
        </fo:table-body>
      </fo:table>
    </fo:static-content>

    <fo:static-content flow-name="xsl-region-after">
      <xsl:call-template name="footer"/>
    </fo:static-content>

    <fo:flow flow-name="xsl-region-body">
      <xsl:call-template name="comptes-annuels.content"/>
    </fo:flow>

  </fo:page-sequence>

</xsl:template>


<!-- Page de titre de <comptes-annuels> ******************************* -->
<xsl:template name="comptes-annuels.titlepage">
  <xsl:call-template name="titlepage">
    <xsl:with-param name="type-doc" select="'Comptes Annuels'"/>
  </xsl:call-template>
</xsl:template>

<!-- contenu de <comptes-annuels> ****************************** -->
<xsl:template name="comptes-annuels.content">
  <xsl:apply-templates select="compte-resultat"/>
  <xsl:apply-templates select="bilan"/>
  <xsl:apply-templates select="appendix"/>
</xsl:template>


<!-- <bilan> ****************************************************** -->
<xsl:template match="bilan">
  <xsl:call-template name="bilan.content"/>
</xsl:template>


<!-- <compte-resultat> ******************************************** -->
<xsl:template match="compte-resultat">
  <xsl:call-template name="compte-resultat.content"/>
</xsl:template>


<!-- <immo-amort> ******************************************** -->
<xsl:template match="immo-amort">
  <xsl:call-template name="immo-amort.content.notitle"/>
</xsl:template>


<!-- <appendix> *************************************************** -->
<xsl:template match="appendix">
  <xsl:apply-templates select="title"/>
  <xsl:apply-templates select="*[not(self::title)]"/>
</xsl:template>


<!-- <title> de <appendix> ******************************************* -->
<xsl:template match="appendix/title">
  <fo:block font-size="18pt" 
            font-family="sans-serif"
            space-before="1em"
            space-after="1.5em"
            font-weight="bold"
            text-align="center"
            break-before="page">
    <xsl:apply-templates/>
  </fo:block>
</xsl:template>


<!-- <section> **************************************************** -->
<xsl:template match="section">
  <xsl:apply-templates select="title"/>
  <xsl:apply-templates select="*[not(self::title)]"/>
</xsl:template>


<!-- <title> de <section> *************************************** -->
<xsl:template match="section/title">
  <fo:block font-size="14pt" 
            font-family="sans-serif"
            space-before="1em"
            space-after="0.5em"
            font-weight="bold"
            text-align="start">
    <xsl:if test="parent::*/@ldg:break='page'">
      <xsl:attribute name="break-before">page</xsl:attribute>
    </xsl:if>
    <xsl:number count="section" format="I-"/>
    <xsl:text> </xsl:text>
    <xsl:apply-templates/>
  </fo:block>
</xsl:template>


<!-- <para> ****************************************************** -->
<xsl:template match="para">
  <fo:block font-size="11pt" 
            font-family="serif"
            space-before="0.5em"
            text-align="justify"
            start-indent="0.5cm"
            text-indent="0.5cm">
    <xsl:if test="@ldg:break='page'">
      <xsl:attribute name="break-before">page</xsl:attribute>
    </xsl:if>
    <xsl:apply-templates/>
  </fo:block>  
</xsl:template>


<!-- <formalpara> ************************************************** -->
<xsl:template match="formalpara">
  <fo:block font-size="11pt" 
            font-family="serif"
            space-before="0.5em"
            text-align="justify"
            start-indent="0.5cm"
            text-indent="0.5cm">
    <xsl:if test="@ldg:break='page'">
      <xsl:attribute name="break-before">page</xsl:attribute>
    </xsl:if>
    <xsl:apply-templates select="title"/>
    <xsl:apply-templates select="para"/>
  </fo:block>  
</xsl:template>


<!-- <title> de <formalpara> ************************************** -->
<xsl:template match="formalpara/title">
  <fo:inline font-weight="bold">
    <xsl:apply-templates/>
    <xsl:text>&#xA0;</xsl:text>
  </fo:inline>
  <xsl:text>: </xsl:text>
</xsl:template>


<!-- <para> de <formalpara> **************************************** -->
<xsl:template match="formalpara/para">
  <xsl:apply-templates/>
</xsl:template>


<!-- <itemizedlist> *********************************************** -->
<xsl:template match="itemizedlist">
  <fo:list-block provisional-distance-between-starts="1em"
                 provisional-label-separation="0.5em"
                 space-before="0.15em"
                 start-indent="1.5cm">
    <xsl:if test="@ldg:break='page'">
      <xsl:attribute name="break-before">page</xsl:attribute>
    </xsl:if>
    <xsl:apply-templates select="listitem"/>
  </fo:list-block>
</xsl:template>


<!-- <listitem> *************************************************** -->
<xsl:template match="listitem">
  <fo:list-item space-before="0.1em"> 
    <xsl:if test="@ldg:break='page'">
      <xsl:attribute name="break-before">page</xsl:attribute>
    </xsl:if>
    <fo:list-item-label end-indent="label-end()">
      <fo:block>
        <xsl:text>&#x2022;</xsl:text>
      </fo:block>
    </fo:list-item-label>
    <fo:list-item-body start-indent="body-start()">
      <xsl:apply-templates select="*"/>
    </fo:list-item-body>
  </fo:list-item>
</xsl:template>


<!-- <para> de <listitem> ********************************************** -->
<xsl:template match="listitem/para">
  <fo:block font-size="11pt" 
            font-family="serif"
            text-align="justify">
    <xsl:apply-templates/>
  </fo:block>  
</xsl:template>


<!-- <formalpara> de <listitem> ************************************* -->
<xsl:template match="listitem/formalpara">
  <fo:block font-size="11pt" 
            font-family="serif"
            text-align="justify">
    <xsl:apply-templates select="title"/>
    <xsl:apply-templates select="para"/>
  </fo:block>  
</xsl:template>


<!-- <orgname> ***************************************************** -->
<xsl:template match="orgname">
  <fo:inline font-weight="bold">
    <xsl:apply-templates/>
  </fo:inline>
</xsl:template>


<!-- <emphasis> ***************************************************** -->
<xsl:template match="emphasis|i">
  <fo:inline font-style="italic">
    <xsl:apply-templates/>
  </fo:inline>
</xsl:template>


<!-- <emphasis> avec attribut 'role' a "bold" *********************** -->
<xsl:template match="emphasis[@role='bold']|b">
  <fo:inline font-weight="bold">
    <xsl:apply-templates/>
  </fo:inline>
</xsl:template>


<!-- <informaltable> ********************************************** -->
<xsl:template match="informaltable">
  <xsl:apply-templates select="*"/>
</xsl:template>


<!-- <tgroup> ********************************************** -->
<xsl:template match="tgroup">
  <fo:table table-layout="fixed"
	    width="18cm"
            border-top-width="0.5pt"
            border-top-style="solid"
            border-left-width="0.5pt"
            border-left-style="solid"
            border-bottom-width="0.5pt"
            border-bottom-style="solid">
    <xsl:apply-templates select="colspec"/>
    <xsl:apply-templates select="*[not(self::colspec)]"/>
  </fo:table>
</xsl:template>


<!-- <colspec> **************************************************** -->
<xsl:template match="colspec">
  <fo:table-column column-number="{@colnum}"
                   column-width="{@colwidth}"/>
</xsl:template>


<!-- <thead> ******************************************************* -->
<xsl:template match="thead">
  <fo:table-header>
    <xsl:apply-templates select="row"/>
  </fo:table-header>
</xsl:template>


<!-- <tbody> ******************************************************* -->
<xsl:template match="tbody">
  <fo:table-body>
    <xsl:apply-templates select="row"/>
  </fo:table-body>
</xsl:template>


<!-- <tfoot> ******************************************************* -->
<xsl:template match="tfoot">
  <fo:table-footer>
    <xsl:apply-templates select="row"/>
  </fo:table-footer>
</xsl:template>


<!-- <row> ******************************************************* -->
<xsl:template match="row">
  <fo:table-row>
    <xsl:apply-templates select="entry"/>
  </fo:table-row>
</xsl:template>


<!-- <entry> ******************************************************* -->
<xsl:template match="entry">
  <fo:table-cell padding="0.1cm"
                 border-right-width="0.5pt"
                 border-right-style="solid">
    <xsl:if test="parent::row/@ldg:border-bottom='yes'">
      <xsl:attribute name="border-bottom-width">0.5pt</xsl:attribute>
      <xsl:attribute name="border-bottom-style">solid</xsl:attribute>
    </xsl:if>
    <xsl:if test="parent::row/@ldg:border-top='yes'">
      <xsl:attribute name="border-top-width">0.5pt</xsl:attribute>
      <xsl:attribute name="border-top-style">solid</xsl:attribute>
    </xsl:if>
    <fo:block font-size="7.5pt">
      <xsl:if test="@align">
        <xsl:attribute name="text-align">
          <xsl:value-of select="@align"/>
        </xsl:attribute>
      </xsl:if>
      <xsl:if test="@valign">
        <xsl:attribute name="vertical-align">
          <xsl:value-of select="@valign"/>
        </xsl:attribute>
      </xsl:if>
      <xsl:if test="@colspan">
        <xsl:attribute name="number-columns-spanned">
          <xsl:value-of select="@colspan"/>
        </xsl:attribute>
      </xsl:if>
      <xsl:if test="@rowspan">
        <xsl:attribute name="number-rows-spanned">
          <xsl:value-of select="@rowspan"/>
        </xsl:attribute>
      </xsl:if>
      <xsl:apply-templates/>
    </fo:block>
  </fo:table-cell>
</xsl:template>

</xsl:stylesheet>