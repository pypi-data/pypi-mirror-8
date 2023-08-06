<?xml version="1.0" encoding="ISO-8859-1"?>


<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
                version="1.0"
                xmlns:fo="http://www.w3.org/1999/XSL/Format">

  <xsl:import href="common.xslt"/>
  <xsl:import href="fo-common.xslt"/>

  <xsl:output method="xml" 
              version="1.0" 
              encoding="ISO-8859-1" 
              indent="yes"/>

  <xsl:param name="societe.def" select="'../xml/societe.xml'"/>
  <xsl:param name="exercice" select="true()"/>

  <xsl:variable name="societe" select="document($societe.def)/societe"/>
  <xsl:variable name="plan_comptable" select="document($societe/plan-comptable/text())/plan-comptable"/>

<!-- <immo-amort> ****************************** -->
<xsl:template match="immo-amort">
  <fo:page-sequence master-reference="A4">

    <fo:static-content flow-name="xsl-region-after">
      <xsl:call-template name="footer"/>
    </fo:static-content>

    <fo:flow flow-name="xsl-region-body">
      <xsl:call-template name="immo-amort.titlepage"/>
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
                <xsl:text>Livre des immobilisations au </xsl:text>
                <xsl:value-of select="@fin"/>
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
      <xsl:call-template name="immo-amort.content"/>
    </fo:flow>

  </fo:page-sequence>

</xsl:template>


<!-- Page de titre de <immo-amort> *********************************** -->
<xsl:template name="immo-amort.titlepage">
  <xsl:call-template name="titlepage">
    <xsl:with-param name="type-doc" select="'Livre des Immobilisations'"/>
  </xsl:call-template>
</xsl:template>


<!-- contenu de <immo-amort> ****************************** -->
<xsl:template name="immo-amort.content">
  <fo:block font-size="18pt" 
            font-family="sans-serif"
            space-before="1em"
            space-after="1.5em"
            font-weight="bold"
            text-align="center"
            break-before="page">
    <xsl:text>Livre des immobilisations au </xsl:text>
    <xsl:value-of select="@fin"/>
  </fo:block>
  <xsl:call-template name="immo-amort.content.notitle"/>
</xsl:template>


<!-- contenu de <immo-amort> sans titre ********************* -->
<xsl:template name="immo-amort.content.notitle">
  <fo:table table-layout="fixed" width="18cm"
            border-top-width="0.5pt" 
            border-top-style="solid"
            border-right-width="0.5pt" 
            border-right-style="solid"
            border-left-width="0.5pt" 
            border-left-style="solid">

    <fo:table-column column-number="1" 
                     column-width="1.75cm"/>
    <fo:table-column column-number="2" 
                     column-width="1.25cm"/>
    <fo:table-column column-number="3" 
                     column-width="9cm"/>
    <fo:table-column column-number="4" 
                     column-width="2cm"/>
    <fo:table-column column-number="5" 
                     column-width="2cm"/>
    <fo:table-column column-number="6" 
                     column-width="2cm"/>

    <fo:table-header>
      <fo:table-row>
        <fo:table-cell padding="0.1cm"
                       border-bottom-width="0.5pt"
                       border-bottom-style="solid"
                       border-right-width="0.5pt"
                       border-right-style="solid">
          <fo:block font-size="8pt"
                    text-align="center"
                    vertical-align="middle">Date</fo:block>
        </fo:table-cell>
        <fo:table-cell padding="0.1cm"
                       border-bottom-width="0.5pt"
                       border-bottom-style="solid"
                       border-right-width="0.5pt"
                       border-right-style="solid">
          <fo:block font-size="8pt"
                    text-align="center"
                    vertical-align="middle">Compte</fo:block>
        </fo:table-cell>
        <fo:table-cell padding="0.1cm"
                       border-bottom-width="0.5pt"
                       border-bottom-style="solid"
                       border-right-width="0.5pt"
                       border-right-style="solid">
          <fo:block font-size="8pt"
                    text-align="center"
                    vertical-align="middle">Libellé</fo:block>
        </fo:table-cell>
        <fo:table-cell padding="0.1cm"
                       border-bottom-width="0.5pt"
                       border-bottom-style="solid"
                       border-right-width="0.5pt"
                       border-right-style="solid">
          <fo:block font-size="8pt"
                    text-align="center"
                    vertical-align="middle">Montant brut</fo:block>
        </fo:table-cell>
        <fo:table-cell padding="0.1cm"
                       border-bottom-width="0.5pt"
                       border-bottom-style="solid"
                       border-right-width="0.5pt"
                       border-right-style="solid">
          <fo:block font-size="8pt"
                    text-align="center"
                    vertical-align="middle">Amortiss.</fo:block>
        </fo:table-cell>
        <fo:table-cell padding="0.1cm"
                       border-bottom-width="0.5pt"
                       border-bottom-style="solid">
          <fo:block font-size="8pt"
                    text-align="center"
                    vertical-align="middle">Montant net</fo:block>
        </fo:table-cell>
      </fo:table-row>
    </fo:table-header>

    <fo:table-body>

      <xsl:apply-templates select="immo">
        <xsl:sort select="@entree" order="descending"/>
      </xsl:apply-templates>
        
      <!-- Insère le total -->
      <fo:table-row>
        <fo:table-cell border-top-width="0.5pt"
                       border-top-style="solid"
                       border-bottom-width="0.5pt"
                       border-bottom-style="solid"
                       number-columns-spanned="6">
          <fo:block space-before="0.25cm"/>
        </fo:table-cell>
      </fo:table-row>

      <fo:table-row>
        <fo:table-cell padding="0.1cm"
                       border-right-width="0.5pt"
                       border-right-style="solid"
                       border-bottom-width="0.5pt"
                       border-bottom-style="solid"
                       number-columns-spanned="2">
	  <fo:block/>
        </fo:table-cell>
        <fo:table-cell padding="0.1cm"
                       border-right-width="0.5pt"
                       border-right-style="solid"
                       border-bottom-width="0.5pt"
                       border-bottom-style="solid">
          <fo:block font-size="8pt"
                    font-weight="bold">
            <xsl:text>Totaux</xsl:text>
          </fo:block>
        </fo:table-cell>
        <fo:table-cell padding="0.1cm"
                       border-right-width="0.5pt"
                       border-right-style="solid"
                       border-bottom-width="0.5pt"
                       border-bottom-style="solid">
          <fo:block font-size="7pt"
                    font-weight="bold"
                    text-align="right">
            <xsl:call-template name="format-montant">
              <xsl:with-param name="montant" select="@montant-brut"/>
            </xsl:call-template>                          
          </fo:block>
        </fo:table-cell>
        <fo:table-cell padding="0.1cm"
                       border-right-width="0.5pt"
                       border-right-style="solid"
                       border-bottom-width="0.5pt"
                       border-bottom-style="solid">
          <fo:block font-size="7pt"
                    font-weight="bold"
                    text-align="right">
            <xsl:call-template name="format-montant">
              <xsl:with-param name="montant" select="@montant-amort"/>
            </xsl:call-template>                          
          </fo:block>
        </fo:table-cell>
        <fo:table-cell padding="0.1cm"
                       border-bottom-width="0.5pt"
                       border-bottom-style="solid">
          <fo:block font-size="7pt"
                    font-weight="bold"
                    text-align="right">
            <xsl:call-template name="format-montant">
              <xsl:with-param name="montant" select="@montant-net"/>
            </xsl:call-template>                          
          </fo:block>
        </fo:table-cell>
      </fo:table-row>

    </fo:table-body>
  </fo:table>
</xsl:template>


<!-- <immo> ***************************************************** -->
<xsl:template match="immo">
  <fo:table-row>
    <fo:table-cell padding="0.1cm"
                   border-right-width="0.5pt"
                   border-right-style="solid">
      <fo:block font-size="7pt">
        <xsl:value-of select="@entree"/>
      </fo:block>
    </fo:table-cell>
    <fo:table-cell padding="0.1cm"
                   border-right-width="0.5pt"
                   border-right-style="solid">
      <fo:block font-size="7pt">
        <xsl:value-of select="@compte"/>
      </fo:block>
    </fo:table-cell>
    <fo:table-cell padding="0.1cm"
                   border-right-width="0.5pt"
                   border-right-style="solid">
      <fo:block font-size="7pt">
        <xsl:value-of select="."/>
      </fo:block>
    </fo:table-cell>
    <fo:table-cell padding="0.1cm"
                   border-right-width="0.5pt"
                   border-right-style="solid">
      <fo:block font-size="7pt"
                text-align="right">
        <xsl:call-template name="format-montant">
          <xsl:with-param name="montant" select="@montant-brut"/>
        </xsl:call-template>
      </fo:block>
    </fo:table-cell>
    <fo:table-cell padding="0.1cm"
                   border-right-width="0.5pt"
                   border-right-style="solid">
      <fo:block font-size="7pt"
                text-align="right">
        <xsl:call-template name="format-montant">
          <xsl:with-param name="montant" select="@montant-amort"/>
        </xsl:call-template>
      </fo:block>
    </fo:table-cell>
    <fo:table-cell padding="0.1cm"
                   border-right-width="0.5pt"
                   border-right-style="solid">
      <fo:block font-size="7pt"
                text-align="right">
        <xsl:call-template name="format-montant">
          <xsl:with-param name="montant" select="@montant-net"/>
        </xsl:call-template>
      </fo:block>
    </fo:table-cell>
  </fo:table-row>
</xsl:template>


</xsl:stylesheet>
