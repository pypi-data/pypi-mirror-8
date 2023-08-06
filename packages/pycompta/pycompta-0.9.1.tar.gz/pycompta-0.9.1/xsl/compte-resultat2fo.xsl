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

<!-- <compte-resultat> ****************************** -->
<xsl:template match="compte-resultat" >
  <fo:page-sequence master-reference="A4">

    <fo:static-content flow-name="xsl-region-after">
      <xsl:call-template name="footer"/>
    </fo:static-content>

    <fo:flow flow-name="xsl-region-body">
      <xsl:call-template name="compte-resultat.titlepage"/>
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
                <xsl:text>Compte de résultat entre le </xsl:text>
                <xsl:value-of select="@debut"/> 
                <xsl:text> et le </xsl:text>
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
      <xsl:call-template name="compte-resultat.content"/>
    </fo:flow>

  </fo:page-sequence>

</xsl:template>


<!-- Page de titre de <compte-resultat> ******************************* -->
<xsl:template name="compte-resultat.titlepage">
  <xsl:call-template name="titlepage">
    <xsl:with-param name="type-doc" select="'Compte de résultat'"/>
  </xsl:call-template>
</xsl:template>


<!-- contenu de <compte-resultat> ****************************** -->
<xsl:template name="compte-resultat.content">
  <fo:block font-size="18pt" 
            font-family="sans-serif"
            space-before="1em"
            space-after="1.5em"
            font-weight="bold"
            text-align="center"
            break-before="page">
    <xsl:text>Compte de Résultat entre le </xsl:text>
    <xsl:value-of select="@debut"/> 
    <xsl:text> et le </xsl:text>
    <xsl:value-of select="@fin"/>
  </fo:block>

    <fo:table table-layout="fixed" width="18cm"
              border-top-width="0.5pt" 
              border-top-style="solid"
              border-right-width="0.5pt" 
              border-right-style="solid"
              border-left-width="0.5pt" 
              border-left-style="solid">

      <fo:table-column column-number="1" 
                       column-width="8.95cm"/>
      <fo:table-column column-number="2"
                       column-width="0.1cm"/>
      <fo:table-column column-number="3" 
                       column-width="8.95cm"/>

      <fo:table-body>
        <fo:table-row>

          <!-- Les charges -->
          <fo:table-cell border-bottom-width="0.5pt" 
                         border-bottom-style="solid"
                         border-right-style="solid"
                         border-right-width="0.5pt">
            <fo:table table-layout="fixed" width="8.95cm">

              <fo:table-column column-number="1" 
                               column-width="7.20cm"/>
              <fo:table-column column-number="2" 
                               column-width="1.75cm"/>

              <fo:table-header>
                <fo:table-row>
                  <fo:table-cell padding="0.1cm"
                                 border-bottom-width="0.5pt"
                                 border-bottom-style="solid"
                                 number-columns-spanned="2">
                    <fo:block font-size="8pt"
                              text-align="center"
                              vertical-align="middle"
                              font-weight="bold">Charges</fo:block>
                  </fo:table-cell>
                </fo:table-row>
                <fo:table-row>
                  <fo:table-cell padding="0.1cm"
                                 border-bottom-width="0.5pt"
                                 border-bottom-style="solid"
                                 border-right-width="0.5pt"
                                 border-right-style="solid">
                    <fo:block font-size="8pt"
                              text-align="center"
                              vertical-align="middle">Désignation</fo:block>
                  </fo:table-cell>
                  <fo:table-cell padding="0.1cm"
                                 border-bottom-width="0.5pt"
                                 border-bottom-style="solid">
                    <fo:block font-size="8pt"
                              text-align="center"
                              vertical-align="middle">Montant</fo:block>
                  </fo:table-cell>
                </fo:table-row>
              </fo:table-header>

              <fo:table-body>

                <xsl:apply-templates select="charges/poste" />

              </fo:table-body>
            </fo:table>
          </fo:table-cell>

          <!-- Les produits -->
          <fo:table-cell border-right-style="solid"
                         border-right-width="0.5pt"/>
          <fo:table-cell>
            <fo:table table-layout="fixed" width="8.95cm">

              <fo:table-column column-number="1" 
                               column-width="7.20cm"/>
              <fo:table-column column-number="2" 
                               column-width="1.75cm"/>

              <fo:table-header>
                <fo:table-row>
                  <fo:table-cell padding="0.1cm"
                                 border-bottom-width="0.5pt"
                                 border-bottom-style="solid"
                                 number-columns-spanned="2">
                    <fo:block font-size="8pt"
                              text-align="center"
                              vertical-align="middle"
                              font-weight="bold">Produits</fo:block>
                  </fo:table-cell>
                </fo:table-row>
                <fo:table-row>
                  <fo:table-cell padding="0.1cm"
                                 border-bottom-width="0.5pt"
                                 border-bottom-style="solid"
                                 border-right-width="0.5pt"
                                 border-right-style="solid">
                    <fo:block font-size="8pt"
                              text-align="center"
                              vertical-align="middle">Désignation</fo:block>
                  </fo:table-cell>
                  <fo:table-cell padding="0.1cm"
                                 border-bottom-width="0.5pt"
                                 border-bottom-style="solid">
                    <fo:block font-size="8pt"
                              text-align="center"
                              vertical-align="middle">Montant</fo:block>
                  </fo:table-cell>
                </fo:table-row>
              </fo:table-header>

              <fo:table-body>

                <xsl:apply-templates select="produits/poste" />

              </fo:table-body>
            </fo:table>
          </fo:table-cell>
        </fo:table-row>

        <!-- insère les totaux -->
        <fo:table-row>
          <fo:table-cell border-right-style="solid"
                         border-right-width="0.5pt">
            <xsl:if test="produits/@montant >= charges/@montant">
              <xsl:attribute name="border-bottom-width">
                <xsl:text>0.5pt</xsl:text>
              </xsl:attribute>
              <xsl:attribute name="border-bottom-style">
                <xsl:text>solid</xsl:text>
              </xsl:attribute>
            </xsl:if>
            <fo:block space-before="0.25cm"/>
          </fo:table-cell>
          <fo:table-cell border-right-style="solid"
                         border-right-width="0.5pt">
            <fo:block space-before="0.25cm"/>
          </fo:table-cell>
          <fo:table-cell>
            <xsl:if test="charges/@montant > produits/@montant">
              <xsl:attribute name="border-bottom-width">
                <xsl:text>0.5pt</xsl:text>
              </xsl:attribute>
              <xsl:attribute name="border-bottom-style">
                <xsl:text>solid</xsl:text>
              </xsl:attribute>
            </xsl:if>
             <fo:block space-before="0.25cm"/>
          </fo:table-cell>
        </fo:table-row>
        <fo:table-row>

          <!-- total des charges -->
          <fo:table-cell>
            <fo:table table-layout="fixed" width="8.95cm">

              <fo:table-column column-number="1" 
                               column-width="7.20cm"/>
              <fo:table-column column-number="2" 
                               column-width="1.75cm"/>

              <fo:table-body>

                <!-- Insère le résultat s'il est positif -->
                <fo:table-row>
                  <fo:table-cell padding="0.1cm"
                                 border-bottom-width="0.5pt"
                                 border-bottom-style="solid">
                    <xsl:if test="produits/@montant >= charges/@montant">
                      <xsl:attribute name="border-right-width">
                        <xsl:text>0.5pt</xsl:text>
                      </xsl:attribute>
                      <xsl:attribute name="border-right-style">
                        <xsl:text>solid</xsl:text>
                      </xsl:attribute>
                    </xsl:if>
                    <fo:block font-size="7pt"
                              font-weight="bold">
                      <xsl:choose>
                        <xsl:when test="produits/@montant >= charges/@montant">
                          <xsl:text>Solde créditeur (bénéfice)</xsl:text>
                        </xsl:when>
                        <xsl:otherwise>
                          <xsl:text>&#xA0;</xsl:text>
                        </xsl:otherwise>
                      </xsl:choose>
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
                      <xsl:choose>
                        <xsl:when test="produits/@montant >= charges/@montant">
                          <xsl:call-template name="format-montant">
                            <xsl:with-param name="montant" 
                                            select="  produits/@montant 
                                                    - charges/@montant "/>
                          </xsl:call-template>
                        </xsl:when>
                        <xsl:otherwise>
                          <xsl:text>&#xA0;</xsl:text>
                        </xsl:otherwise>
                      </xsl:choose>
                    </fo:block>
                  </fo:table-cell>
                </fo:table-row>

                <!-- Insère le total général -->
                <fo:table-row>
                  <fo:table-cell padding="0.1cm"
                                 border-right-width="0.5pt"
                                 border-right-style="solid"
                                 border-bottom-width="0.5pt"
                                 border-bottom-style="solid">
                    <fo:block font-size="7pt"
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
                      <xsl:choose>
                        <xsl:when test="produits/@montant > charges/@montant">
                          <xsl:call-template name="format-montant">
                            <xsl:with-param name="montant" 
                                            select="produits/@montant"/>
                          </xsl:call-template>
                        </xsl:when>
                        <xsl:otherwise>
                          <xsl:call-template name="format-montant">
                            <xsl:with-param name="montant" 
                                            select="charges/@montant"/>
                          </xsl:call-template>                          
                        </xsl:otherwise>
                      </xsl:choose>
                    </fo:block>
                  </fo:table-cell>
                </fo:table-row>

              </fo:table-body>
            </fo:table>
          </fo:table-cell>

          <!-- total des produits -->
          <fo:table-cell border-bottom-width="0.5pt" 
                         border-bottom-style="solid"
                         border-right-style="solid"
                         border-right-width="0.5pt"/>
          <fo:table-cell>
            <fo:table table-layout="fixed" width="8.95cm">

              <fo:table-column column-number="1" 
                               column-width="7.20cm"/>
              <fo:table-column column-number="2" 
                               column-width="1.75cm"/>

              <fo:table-body>

                <!-- Insère le résultat s'il est négatif -->
                <fo:table-row>
                  <fo:table-cell padding="0.1cm"
                                 border-bottom-width="0.5pt"
                                 border-bottom-style="solid">
                    <xsl:if test="charges/@montant > produits/@montant">
                      <xsl:attribute name="border-right-width">
                        <xsl:text>0.5pt</xsl:text>
                      </xsl:attribute>
                      <xsl:attribute name="border-right-style">
                        <xsl:text>solid</xsl:text>
                      </xsl:attribute>
                    </xsl:if>
                    <fo:block font-size="7pt"
                              font-weight="bold">
                      <xsl:choose>
                        <xsl:when test="charges/@montant > produits/@montant">
                          <xsl:text>Solde débiteur (perte)</xsl:text>
                        </xsl:when>
                        <xsl:otherwise>
                          <xsl:text>&#xA0;</xsl:text>
                        </xsl:otherwise>
                      </xsl:choose>
                    </fo:block>
                  </fo:table-cell>
                  <fo:table-cell padding="0.1cm"
                                 border-bottom-width="0.5pt"
                                 border-bottom-style="solid">
                    <fo:block font-size="7pt"
                              font-weight="bold"
                              text-align="right">
                      <xsl:choose>
                        <xsl:when test="charges/@montant > produits/@montant">
                          <xsl:call-template name="format-montant">
                            <xsl:with-param name="montant" 
                                            select="  charges/@montant 
                                                    - produits/@montant "/>
                          </xsl:call-template>
                        </xsl:when>
                        <xsl:otherwise>
                          <xsl:text>&#xA0;</xsl:text>
                        </xsl:otherwise>
                      </xsl:choose>
                    </fo:block>
                  </fo:table-cell>
                </fo:table-row>

                <!-- Insère le total général -->
                <fo:table-row>
                  <fo:table-cell padding="0.1cm"
                                 border-right-width="0.5pt"
                                 border-right-style="solid"
                                 border-bottom-width="0.5pt"
                                 border-bottom-style="solid">
                    <fo:block font-size="7pt"
                              font-weight="bold">
                      <xsl:text>Total général</xsl:text>
                    </fo:block>
                  </fo:table-cell>
                  <fo:table-cell padding="0.1cm"
                                 border-bottom-width="0.5pt"
                                 border-bottom-style="solid">
                    <fo:block font-size="7pt"
                              font-weight="bold"
                              text-align="right">
                      <xsl:choose>
                        <xsl:when test="charges/@montant > produits/@montant">
                          <xsl:call-template name="format-montant">
                            <xsl:with-param name="montant" 
                                            select="charges/@montant"/>
                          </xsl:call-template>
                        </xsl:when>
                        <xsl:otherwise>
                          <xsl:call-template name="format-montant">
                            <xsl:with-param name="montant" 
                                            select="produits/@montant"/>
                          </xsl:call-template>                          
                        </xsl:otherwise>
                      </xsl:choose>
                    </fo:block>
                  </fo:table-cell>
                </fo:table-row>

              </fo:table-body>
            </fo:table>
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
      <fo:block font-size="7pt"
                text-align="right">
        <xsl:choose>
          <xsl:when test="poste">
            <xsl:text>&#xA0;</xsl:text>
          </xsl:when>
          <xsl:otherwise>
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
                          select="@montant"/>
          </xsl:call-template>
        </fo:block>
      </fo:table-cell>
    </fo:table-row>
  </xsl:if>

</xsl:template>

</xsl:stylesheet>