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

  <xsl:param name="old.bilan" select="document($bilan.precedent)/bilan"/>

  <xsl:variable name="societe" select="document($societe.def)/societe"/>
  <xsl:variable name="plan_comptable" select="document($societe/plan-comptable/text())/plan-comptable"/>

<!-- <bilan> ****************************** -->
<xsl:template match="bilan">
  <fo:page-sequence master-reference="A4">

    <fo:static-content flow-name="xsl-region-after">
      <xsl:call-template name="footer"/>
    </fo:static-content>

    <fo:flow flow-name="xsl-region-body">
      <xsl:call-template name="bilan.titlepage"/>
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
                <xsl:text>Bilan au </xsl:text>
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
      <xsl:call-template name="bilan.content"/>
    </fo:flow>

  </fo:page-sequence>

</xsl:template>


<!-- Page de titre de <bilan> *********************************** -->
<xsl:template name="bilan.titlepage">
  <xsl:call-template name="titlepage">
    <xsl:with-param name="type-doc" select="'Bilan'"/>
  </xsl:call-template>
</xsl:template>


<!-- contenu de <bilan> ****************************** -->
<xsl:template name="bilan.content">
  <xsl:apply-templates select="actif|passif" />
</xsl:template>


<!-- <actif> <passif> ****************************** -->
<xsl:template match="actif|passif" >
  <fo:block font-size="18pt" 
            font-family="sans-serif"
            space-before="1em"
            space-after="1.5em"
            font-weight="bold"
            text-align="center"
            break-before="page">
    <xsl:text>Bilan au </xsl:text>
    <xsl:value-of select="parent::bilan/@fin"/>
    <xsl:choose>
      <xsl:when test="self::actif">
        <xsl:text> (Actif)</xsl:text>
      </xsl:when>
      <xsl:when test="self::passif">
        <xsl:text> (Passif)</xsl:text>
      </xsl:when>
    </xsl:choose>
  </fo:block>

  <fo:table table-layout="fixed" width="18cm"
            border-top-width="0.5pt" 
            border-top-style="solid"
            border-right-width="0.5pt" 
            border-right-style="solid"
            border-left-width="0.5pt" 
            border-left-style="solid">

    <fo:table-column column-number="1" 
                     column-width="10cm"/>
    <fo:table-column column-number="2" 
                     column-width="2cm"/>
    <fo:table-column column-number="3" 
                     column-width="2cm"/>
    <fo:table-column column-number="4" 
                     column-width="2cm"/>
    <fo:table-column column-number="5" 
                     column-width="2cm"/>

    <fo:table-header>
      <fo:table-row>
        <fo:table-cell padding="0.1cm"
                       border-bottom-width="0.5pt"
                       border-bottom-style="solid"
                       number-columns-spanned="5">
          <fo:block font-size="8pt"
                    text-align="center"
                    vertical-align="middle"
                    font-weight="bold">
            <xsl:choose>
              <xsl:when test="self::actif">
                <xsl:text>Actif</xsl:text>
              </xsl:when>
              <xsl:when test="self::passif">
                <xsl:text>Passif</xsl:text>
              </xsl:when>
            </xsl:choose>
          </fo:block>
        </fo:table-cell>
      </fo:table-row>
      <fo:table-row>
        <fo:table-cell padding="0.1cm"
                       border-bottom-width="0.5pt"
                       border-bottom-style="solid"
                       border-right-width="0.5pt"
                       border-right-style="solid"
                       number-columns-spanned="3">
          <fo:block font-size="8pt"
                    text-align="center"
                    vertical-align="middle">Désignation</fo:block>
        </fo:table-cell>
        <fo:table-cell padding="0.1cm"
                       border-right-width="0.5pt"
                       border-right-style="solid"
                       border-bottom-width="0.5pt"
                       border-bottom-style="solid">
          <fo:block font-size="8pt"
                    text-align="center"
                    vertical-align="middle">N</fo:block>
        </fo:table-cell>
        <fo:table-cell padding="0.1cm"
                       border-bottom-width="0.5pt"
                       border-bottom-style="solid">
          <fo:block font-size="8pt"
                    text-align="center"
                    vertical-align="middle">N-1</fo:block>
        </fo:table-cell>
      </fo:table-row>
    </fo:table-header>

    <fo:table-body>

      <xsl:apply-templates select="poste" />
        
      <!-- Insère le total -->
      <fo:table-row>
        <fo:table-cell border-right-style="solid"
                       border-right-width="0.5pt"
                       border-bottom-width="0.5pt"
                       border-bottom-style="solid"
                       number-columns-spanned="3">
          <fo:block space-before="0.25cm"/>
        </fo:table-cell>
        <fo:table-cell border-bottom-width="0.5pt"
                       border-bottom-style="solid">
          <fo:block space-before="0.25cm"/>
        </fo:table-cell>
        <fo:table-cell border-bottom-width="0.5pt"
                       border-bottom-style="solid">
          <fo:block space-before="0.25cm"/>
        </fo:table-cell>
      </fo:table-row>

      <fo:table-row>
        <fo:table-cell padding="0.1cm"
                       border-right-width="0.5pt"
                       border-right-style="solid"
                       border-bottom-width="0.5pt"
                       border-bottom-style="solid"
                       number-columns-spanned="3">
          <fo:block font-size="8pt"
                    font-weight="bold">
            <xsl:text>Total général</xsl:text>
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
              <xsl:with-param name="montant" select="@montant"/>
            </xsl:call-template>                          
          </fo:block>
        </fo:table-cell>
        <fo:table-cell padding="0.1cm"
                       border-bottom-width="0.5pt"
                       border-bottom-style="solid">
          <fo:block font-size="7pt"
                    font-weight="bold"
                    text-align="right">
              <xsl:choose>
                <xsl:when test="self::actif">
                  <xsl:call-template name="format-montant">
                    <xsl:with-param name="montant" select="$old.bilan/actif/@montant"/>
                  </xsl:call-template>                          
                </xsl:when>
                <xsl:when test="self::passif">
                  <xsl:call-template name="format-montant">
                    <xsl:with-param name="montant" select="$old.bilan/passif/@montant"/>
                  </xsl:call-template>                          
                </xsl:when>
              </xsl:choose>
          </fo:block>
        </fo:table-cell>
      </fo:table-row>

    </fo:table-body>
  </fo:table>
</xsl:template>


<!-- <poste> ***************************************************** -->
<xsl:template match="poste" >

  <!-- Si a des fils <poste> insère le nom uniquement sinon insère
       nom et montant -->
  <fo:table-row>
    <fo:table-cell padding-right="0.1cm"
                   padding-left="0.1cm"
                   padding-top="{0.1 div count(ancestor-or-self::poste)}cm"
                   padding-bottom="{0.1 div count(ancestor-or-self::poste)}cm"
                   border-right-width="0.5pt"
                   border-right-style="solid">
      <xsl:if test="not(poste) and (count(ancestor::poste) = 0)">
        <xsl:attribute name="border-bottom-width">
          <xsl:text>0.5pt</xsl:text>
        </xsl:attribute>
        <xsl:attribute name="border-bottom-style">
          <xsl:text>solid</xsl:text>
        </xsl:attribute>
      </xsl:if>
      <xsl:if test="not(@montant-brut)">
        <xsl:attribute name="number-columns-spanned">
          <xsl:text>3</xsl:text>
        </xsl:attribute>
      </xsl:if>
      <fo:block font-size="7pt"
                start-indent="{count(ancestor::poste) * 0.5 + 0.25}cm"
                text-indent="-0.25cm">
        <xsl:choose>
          <xsl:when test="count(ancestor::poste) = 0">
            <xsl:attribute name="font-weight">
              <xsl:text>bold</xsl:text>
            </xsl:attribute>
          </xsl:when>
          <xsl:when test="poste and (count(ancestor::poste) = 1)">
            <xsl:attribute name="font-style">
              <xsl:text>italic</xsl:text>
            </xsl:attribute>
          </xsl:when>
        </xsl:choose>
        <xsl:value-of select="@nom"/>
      </fo:block>
    </fo:table-cell>
    <xsl:if test="@montant-brut">
      <fo:table-cell padding-right="0.1cm"
                     padding-left="0.1cm"
                     padding-top="{0.1 div count(ancestor-or-self::poste)}cm"
                  padding-bottom="{0.1 div count(ancestor-or-self::poste)}cm"
                     border-right-width="0.5pt"
                     border-right-style="solid">
        <xsl:if test="not(poste) and (count(ancestor::poste) = 0)">
          <xsl:attribute name="border-bottom-width">
            <xsl:text>0.5pt</xsl:text>
          </xsl:attribute>
          <xsl:attribute name="border-bottom-style">
            <xsl:text>solid</xsl:text>
          </xsl:attribute>          
        </xsl:if>
        <fo:block font-size="7pt">
          <xsl:choose>
            <xsl:when test="poste and not(ancestor::poste/@montant-brut)">
              <xsl:attribute name="text-align">
                <xsl:text>center</xsl:text>
              </xsl:attribute>
              <xsl:attribute name="font-style">
                <xsl:text>italic</xsl:text>
              </xsl:attribute>
              <xsl:text>Brut</xsl:text>
            </xsl:when>
            <xsl:when test="poste">
              <xsl:text>&#xA0;</xsl:text>
            </xsl:when>
            <xsl:otherwise>
              <xsl:attribute name="text-align">
                <xsl:text>right</xsl:text>
              </xsl:attribute>
              <xsl:if test="count(ancestor::poste) = 0">
                <xsl:attribute name="font-weight">
                  <xsl:text>bold</xsl:text>
                </xsl:attribute>
              </xsl:if>
              <xsl:call-template name="format-montant">
                <xsl:with-param name="montant" select="@montant-brut"/>
              </xsl:call-template>
            </xsl:otherwise>
          </xsl:choose>
        </fo:block>
      </fo:table-cell>      
      <fo:table-cell padding-right="0.1cm"
                     padding-left="0.1cm"
                     padding-top="{0.1 div count(ancestor-or-self::poste)}cm"
                  padding-bottom="{0.1 div count(ancestor-or-self::poste)}cm"
                     border-right-width="0.5pt"
                     border-right-style="solid">
        <xsl:if test="not(poste) and (count(ancestor::poste) = 0)">
          <xsl:attribute name="border-bottom-width">
            <xsl:text>0.5pt</xsl:text>
          </xsl:attribute>
          <xsl:attribute name="border-bottom-style">
            <xsl:text>solid</xsl:text>
          </xsl:attribute>          
        </xsl:if>
        <fo:block font-size="7pt">
          <xsl:choose>
            <xsl:when test="poste and not(ancestor::poste/@montant-brut)">
              <xsl:attribute name="text-align">
                <xsl:text>center</xsl:text>
              </xsl:attribute>
              <xsl:attribute name="font-style">
                <xsl:text>italic</xsl:text>
              </xsl:attribute>
              <xsl:text>Amort.</xsl:text>
            </xsl:when>
            <xsl:when test="poste">
              <xsl:text>&#xA0;</xsl:text>
            </xsl:when>
            <xsl:otherwise>
              <xsl:attribute name="text-align">
                <xsl:text>right</xsl:text>
              </xsl:attribute>
              <xsl:if test="count(ancestor::poste) = 0">
                <xsl:attribute name="font-weight">
                  <xsl:text>bold</xsl:text>
                </xsl:attribute>
              </xsl:if>
              <xsl:call-template name="format-montant">
                <xsl:with-param name="montant" select="@montant-amort"/>
              </xsl:call-template>
            </xsl:otherwise>
          </xsl:choose>
        </fo:block>
      </fo:table-cell>
    </xsl:if>      
    <fo:table-cell padding-right="0.1cm"
                   padding-left="0.1cm"
                   padding-top="{0.1 div count(ancestor-or-self::poste)}cm"
                   padding-bottom="{0.1 div count(ancestor-or-self::poste)}cm"
                   border-right-width="0.5pt"
                   border-right-style="solid">
      <xsl:if test="not(poste) and (count(ancestor::poste) = 0)">
        <xsl:attribute name="border-bottom-width">
          <xsl:text>0.5pt</xsl:text>
        </xsl:attribute>
        <xsl:attribute name="border-bottom-style">
          <xsl:text>solid</xsl:text>
        </xsl:attribute>          
      </xsl:if>
      <fo:block font-size="7pt">
        <xsl:choose>
          <xsl:when test="poste and not(ancestor::poste/@montant-brut) 
                           and @montant-brut">
            <xsl:attribute name="text-align">
              <xsl:text>center</xsl:text>
            </xsl:attribute>
            <xsl:attribute name="font-style">
              <xsl:text>italic</xsl:text>
            </xsl:attribute>
            <xsl:text>Net</xsl:text>
          </xsl:when>
          <xsl:when test="poste">
            <xsl:text>&#xA0;</xsl:text>
          </xsl:when>
          <xsl:otherwise>
            <xsl:attribute name="text-align">
              <xsl:text>right</xsl:text>
            </xsl:attribute>
            <xsl:if test="count(ancestor::poste) = 0">
              <xsl:attribute name="font-weight">
                <xsl:text>bold</xsl:text>
              </xsl:attribute>
            </xsl:if>
            <xsl:call-template name="format-montant">
              <xsl:with-param name="montant" select="@montant"/>
            </xsl:call-template>
          </xsl:otherwise>
        </xsl:choose>
      </fo:block>
    </fo:table-cell>      

    <fo:table-cell padding-right="0.1cm"
                   padding-left="0.1cm"
                   padding-top="{0.1 div count(ancestor-or-self::poste)}cm"
                   padding-bottom="{0.1 div count(ancestor-or-self::poste)}cm">
      <xsl:if test="not(poste) and (count(ancestor::poste) = 0)">
        <xsl:attribute name="border-bottom-width">
          <xsl:text>0.5pt</xsl:text>
        </xsl:attribute>
        <xsl:attribute name="border-bottom-style">
          <xsl:text>solid</xsl:text>
        </xsl:attribute>          
      </xsl:if>
      <fo:block font-size="7pt">
        <xsl:choose>
          <xsl:when test="poste and not(ancestor::poste/@montant-brut) 
                           and @montant-brut">
            <xsl:attribute name="text-align">
              <xsl:text>center</xsl:text>
            </xsl:attribute>
            <xsl:attribute name="font-style">
              <xsl:text>italic</xsl:text>
            </xsl:attribute>
            <xsl:text>Net</xsl:text>
          </xsl:when>
          <xsl:when test="poste">
            <xsl:text>&#xA0;</xsl:text>
          </xsl:when>
          <xsl:otherwise>
            <xsl:attribute name="text-align">
              <xsl:text>right</xsl:text>
            </xsl:attribute>
            <xsl:if test="count(ancestor::poste) = 0">
              <xsl:attribute name="font-weight">
                <xsl:text>bold</xsl:text>
              </xsl:attribute>
            </xsl:if>
            <xsl:call-template name="format-montant">
              <xsl:with-param name="montant" select="$old.bilan//poste[@id = current()/@id]/@montant"/>
            </xsl:call-template>
          </xsl:otherwise>
        </xsl:choose>
      </fo:block>
    </fo:table-cell>      
  </fo:table-row>

  <!-- Si a des fils <poste> les insère -->
  <xsl:apply-templates select="poste" />

  <!-- Si a des fils <poste> insère une ligne total avec le montant -->
  <xsl:if test="poste">
    <fo:table-row>
      <fo:table-cell padding-right="0.1cm"
                     padding-left="0.1cm"
                     padding-top="{0.1 div count(ancestor-or-self::poste)}cm"
                  padding-bottom="{0.1 div count(ancestor-or-self::poste)}cm"
                     border-right-width="0.5pt"
                     border-right-style="solid">
        <xsl:if test="not(@montant-brut)">
          <xsl:attribute name="number-columns-spanned">
            <xsl:text>3</xsl:text>
          </xsl:attribute>
        </xsl:if>
        <xsl:if test="count(ancestor::poste) = 0">
          <xsl:attribute name="border-bottom-width">
            <xsl:text>0.5pt</xsl:text>
          </xsl:attribute>
          <xsl:attribute name="border-bottom-style">
            <xsl:text>solid</xsl:text>
          </xsl:attribute>          
        </xsl:if>
        <fo:block font-size="7pt"
                start-indent="{count(ancestor::poste) * 0.5 + 0.25}cm"
                text-indent="-0.25cm">
          <xsl:choose>
            <xsl:when test="count(ancestor::poste)=0">
              <xsl:attribute name="font-weight">
                <xsl:text>bold</xsl:text>
              </xsl:attribute>
            </xsl:when>
            <xsl:when test="count(ancestor::poste)=1">
              <xsl:attribute name="font-style">
                <xsl:text>italic</xsl:text>
              </xsl:attribute>
            </xsl:when>
          </xsl:choose>
          <xsl:text>Total</xsl:text>
        </fo:block>      
      </fo:table-cell>
      <xsl:if test="@montant-brut">
        <fo:table-cell padding-right="0.1cm"
                       padding-left="0.1cm"
                       padding-top="{0.1 div count(ancestor-or-self::poste)}cm"
                    padding-bottom="{0.1 div count(ancestor-or-self::poste)}cm"
                       border-right-width="0.5pt"
                       border-right-style="solid">
          <xsl:if test="count(ancestor::poste) = 0">
            <xsl:attribute name="border-bottom-width">
              <xsl:text>0.5pt</xsl:text>
            </xsl:attribute>
            <xsl:attribute name="border-bottom-style">
              <xsl:text>solid</xsl:text>
            </xsl:attribute>          
          </xsl:if>
          <fo:block font-size="7pt"
                    text-align="right">
            <xsl:choose>
              <xsl:when test="count(ancestor::poste)=0">
                <xsl:attribute name="font-weight">
                  <xsl:text>bold</xsl:text>
                </xsl:attribute>
              </xsl:when>
              <xsl:when test="count(ancestor::poste)=1">
                <xsl:attribute name="font-style">
                  <xsl:text>italic</xsl:text>
                </xsl:attribute>
              </xsl:when>
            </xsl:choose>
            <xsl:call-template name="format-montant">
              <xsl:with-param name="montant" 
                              select="@montant-brut"/>
            </xsl:call-template>
          </fo:block>
        </fo:table-cell>
        <fo:table-cell padding-right="0.1cm"
                       padding-left="0.1cm"
                       padding-top="{0.1 div count(ancestor-or-self::poste)}cm"
                    padding-bottom="{0.1 div count(ancestor-or-self::poste)}cm"
                       border-right-width="0.5pt"
                       border-right-style="solid">
          <xsl:if test="count(ancestor::poste) = 0">
            <xsl:attribute name="border-bottom-width">
              <xsl:text>0.5pt</xsl:text>
            </xsl:attribute>
            <xsl:attribute name="border-bottom-style">
              <xsl:text>solid</xsl:text>
            </xsl:attribute>          
          </xsl:if>
          <fo:block font-size="7pt"
                    text-align="right">
            <xsl:choose>
              <xsl:when test="count(ancestor::poste)=0">
                <xsl:attribute name="font-weight">
                  <xsl:text>bold</xsl:text>
                </xsl:attribute>
              </xsl:when>
              <xsl:when test="count(ancestor::poste)=1">
                <xsl:attribute name="font-style">
                  <xsl:text>italic</xsl:text>
                </xsl:attribute>
              </xsl:when>
            </xsl:choose>
            <xsl:call-template name="format-montant">
              <xsl:with-param name="montant" 
                              select="@montant-amort"/>
            </xsl:call-template>
          </fo:block>
        </fo:table-cell>
      </xsl:if>
      <fo:table-cell padding-right="0.1cm"
                     padding-left="0.1cm"
                     padding-top="{0.1 div count(ancestor-or-self::poste)}cm"
                  padding-bottom="{0.1 div count(ancestor-or-self::poste)}cm"
                     border-right-width="0.5pt"
                     border-right-style="solid">
        <xsl:if test="count(ancestor::poste) = 0">
          <xsl:attribute name="border-bottom-width">
            <xsl:text>0.5pt</xsl:text>
          </xsl:attribute>
          <xsl:attribute name="border-bottom-style">
            <xsl:text>solid</xsl:text>
          </xsl:attribute>          
        </xsl:if>
        <fo:block font-size="7pt"
                  text-align="right">
          <xsl:choose>
            <xsl:when test="count(ancestor::poste)=0">
              <xsl:attribute name="font-weight">
                <xsl:text>bold</xsl:text>
              </xsl:attribute>
            </xsl:when>
            <xsl:when test="count(ancestor::poste)=1">
              <xsl:attribute name="font-style">
                <xsl:text>italic</xsl:text>
              </xsl:attribute>
            </xsl:when>
          </xsl:choose>
          <xsl:call-template name="format-montant">
          <xsl:with-param name="montant" 
                          select="@montant"/>
          </xsl:call-template>
        </fo:block>
      </fo:table-cell>

      <fo:table-cell padding-right="0.1cm"
                     padding-left="0.1cm"
                     padding-top="{0.1 div count(ancestor-or-self::poste)}cm"
                  padding-bottom="{0.1 div count(ancestor-or-self::poste)}cm">
        <xsl:if test="count(ancestor::poste) = 0">
          <xsl:attribute name="border-bottom-width">
            <xsl:text>0.5pt</xsl:text>
          </xsl:attribute>
          <xsl:attribute name="border-bottom-style">
            <xsl:text>solid</xsl:text>
          </xsl:attribute>          
        </xsl:if>
        <fo:block font-size="7pt"
                  text-align="right">
          <xsl:choose>
            <xsl:when test="count(ancestor::poste)=0">
              <xsl:attribute name="font-weight">
                <xsl:text>bold</xsl:text>
              </xsl:attribute>
            </xsl:when>
            <xsl:when test="count(ancestor::poste)=1">
              <xsl:attribute name="font-style">
                <xsl:text>italic</xsl:text>
              </xsl:attribute>
            </xsl:when>
          </xsl:choose>
          <xsl:call-template name="format-montant">
          <xsl:with-param name="montant" 
            select="$old.bilan//poste[@id = current()/@id]/@montant"/>
          </xsl:call-template>
        </fo:block>
      </fo:table-cell>
    </fo:table-row>
  </xsl:if>

</xsl:template>



</xsl:stylesheet>