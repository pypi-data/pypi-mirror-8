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

  <xsl:param name="old.cr" select="document($cr.precedent)/compte-resultat"/>

  <xsl:variable name="societe" select="document($societe.def)/societe"/>
  <xsl:variable name="plan_comptable" select="document($societe/plan-comptable/text())/plan-comptable"/>

<!-- <compte-resultat> ****************************** -->
<xsl:template match="compte-resultat">
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
    <xsl:with-param name="type-doc" select="'Compte de Résultat'"/>
  </xsl:call-template>
</xsl:template>

<!-- contenu de <compte-resultat> ****************************** -->
<xsl:template name="compte-resultat.content">
  <fo:block font-size="18pt" 
            font-family="sans-serif"
            space-before="0.2em"
            space-after="0.5em"
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
                     column-width="14cm"/>
    <fo:table-column column-number="2" 
                     column-width="2cm"/>
    <fo:table-column column-number="3" 
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
                    vertical-align="middle">Désignation</fo:block>
        </fo:table-cell>
        <fo:table-cell padding="0.1cm"
                       border-bottom-width="0.5pt"
                       border-bottom-style="solid"
                       border-right-width="0.5pt"
                       border-right-style="solid">
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

      <xsl:apply-templates select="produits/poste[1]" mode="cr1col"/>
      <xsl:apply-templates select="charges/poste[1]" mode="cr1col"/>
      <fo:table-row>
        <fo:table-cell padding="0.1cm"
                       border-right-width="0.5pt"
                       border-right-style="solid"
                       border-bottom-width="0.5pt"
                       border-bottom-style="solid">
          <fo:block font-size="7pt"
                    font-weight="bold">
            <xsl:text>1- Résultat d'exploitation</xsl:text>
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
              <xsl:with-param name="montant"
                              select="  produits/poste[1]/@montant 
                                      - charges/poste[1]/@montant"/>
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
              <xsl:with-param name="montant"
                select="  $old.cr/produits/poste[1]/@montant 
                        - $old.cr/charges/poste[1]/@montant"/>
            </xsl:call-template>
          </fo:block>
        </fo:table-cell>
      </fo:table-row>

      <xsl:apply-templates select="produits/poste[2]" mode="cr1col"/>
      <xsl:apply-templates select="charges/poste[2]" mode="cr1col"/>
      <xsl:apply-templates select="produits/poste[3]" mode="cr1col"/>
      <xsl:apply-templates select="charges/poste[3]" mode="cr1col"/>
      <fo:table-row>
        <fo:table-cell padding="0.1cm"
                       border-right-width="0.5pt"
                       border-right-style="solid"
                       border-bottom-width="0.5pt"
                       border-bottom-style="solid">
          <fo:block font-size="7pt"
                    font-weight="bold">
            <xsl:text>2- Résultat financier</xsl:text>
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
              <xsl:with-param name="montant"
                              select="  produits/poste[3]/@montant 
                                      - charges/poste[3]/@montant"/>
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
              <xsl:with-param name="montant"
                select="  $old.cr/produits/poste[3]/@montant 
                        - $old.cr/charges/poste[3]/@montant"/>
            </xsl:call-template>
          </fo:block>
        </fo:table-cell>
      </fo:table-row>
      <fo:table-row>
        <fo:table-cell padding="0.1cm"
                       border-right-width="0.5pt"
                       border-right-style="solid"
                       border-bottom-width="0.5pt"
                       border-bottom-style="solid">
          <fo:block font-size="7pt"
                    font-weight="bold">
            <xsl:text>3- Résultat courant avant impôts</xsl:text>
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
              <xsl:with-param name="montant"
                   select="  sum(produits/poste[position() &lt;= 3]/@montant) 
                           - sum(charges/poste[position() &lt;= 3]/@montant)"/>
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
              <xsl:with-param name="montant"
                select="  sum($old.cr/produits/poste[position() &lt;= 3]/@montant) 
                        - sum($old.cr/charges/poste[position() &lt;= 3]/@montant)"/>
            </xsl:call-template>
          </fo:block>
        </fo:table-cell>
      </fo:table-row>

      <xsl:apply-templates select="produits/poste[4]" mode="cr1col"/>
      <xsl:apply-templates select="charges/poste[4]" mode="cr1col"/>
      <fo:table-row>
        <fo:table-cell padding="0.1cm"
                       border-right-width="0.5pt"
                       border-right-style="solid"
                       border-bottom-width="0.5pt"
                       border-bottom-style="solid">
          <fo:block font-size="7pt"
                    font-weight="bold">
            <xsl:text>4- Résultat exceptionnel</xsl:text>
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
              <xsl:with-param name="montant"
                              select="  produits/poste[4]/@montant 
                                      - charges/poste[4]/@montant"/>
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
              <xsl:with-param name="montant"
                select="  $old.cr/produits/poste[4]/@montant 
                        - $old.cr/charges/poste[4]/@montant"/>
            </xsl:call-template>
          </fo:block>
        </fo:table-cell>
      </fo:table-row>

      <xsl:apply-templates select="charges/poste[5]" mode="cr1col"/>
      <xsl:apply-templates select="charges/poste[6]" mode="cr1col"/>

      <fo:table-row>
        <fo:table-cell padding="0.1cm"
                       border-right-width="0.5pt"
                       border-right-style="solid"
                       border-bottom-width="0.5pt"
                       border-bottom-style="solid">
          <fo:block font-size="7pt"
                    font-weight="bold">
            <xsl:text>Total des produits</xsl:text>
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
              <xsl:with-param name="montant"
                              select="produits/@montant"/>
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
              <xsl:with-param name="montant"
                select="$old.cr/produits/@montant"/>
            </xsl:call-template>
          </fo:block>
        </fo:table-cell>
      </fo:table-row>
      <fo:table-row>
        <fo:table-cell padding="0.1cm"
                       border-right-width="0.5pt"
                       border-right-style="solid"
                       border-bottom-width="0.5pt"
                       border-bottom-style="solid">
          <fo:block font-size="7pt"
                    font-weight="bold">
            <xsl:text>Total des charges</xsl:text>
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
              <xsl:with-param name="montant"
                              select="charges/@montant"/>
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
              <xsl:with-param name="montant"
                select="$old.cr/charges/@montant"/>
            </xsl:call-template>
          </fo:block>
        </fo:table-cell>
      </fo:table-row>
      <fo:table-row>
        <fo:table-cell padding="0.1cm"
                       border-right-width="0.5pt"
                       border-right-style="solid"
                       border-bottom-width="0.5pt"
                       border-bottom-style="solid">
          <fo:block font-size="7pt"
                    font-weight="bold">
            <xsl:text>5- Bénéfice ou perte</xsl:text>
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
              <xsl:with-param name="montant"
                              select="produits/@montant - charges/@montant"/>
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
              <xsl:with-param name="montant"
                select="$old.cr/produits/@montant - $old.cr/charges/@montant"/>
            </xsl:call-template>
          </fo:block>
        </fo:table-cell>
      </fo:table-row>


    </fo:table-body>
  </fo:table>
</xsl:template>


<!-- <poste> ***************************************************** -->
<xsl:template match="poste" mode="cr1col">

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
              <xsl:with-param name="montant" select="$old.cr//poste[@id = current()/@id]/@montant"/>
            </xsl:call-template>
          </xsl:otherwise>
        </xsl:choose>
      </fo:block>
    </fo:table-cell>      
  </fo:table-row>

  <!-- Si a des fils <poste> les insère -->
  <xsl:apply-templates select="poste" mode="cr1col"/>

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
            select="$old.cr//poste[@id = current()/@id]/@montant"/>
          </xsl:call-template>
        </fo:block>
      </fo:table-cell>
    </fo:table-row>
  </xsl:if>

</xsl:template>

</xsl:stylesheet>
