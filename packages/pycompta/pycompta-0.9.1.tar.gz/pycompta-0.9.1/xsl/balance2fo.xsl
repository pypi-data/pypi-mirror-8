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

<!-- <balance> ****************************** -->
<xsl:template match="balance">
  <fo:page-sequence master-reference="A4">

    <fo:static-content flow-name="xsl-region-after">
      <xsl:call-template name="footer"/>
    </fo:static-content>

    <fo:flow flow-name="xsl-region-body">
      <xsl:call-template name="balance.titlepage"/>
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
                <xsl:text>Balance entre le </xsl:text>
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
      <xsl:call-template name="balance.content"/>
    </fo:flow>

  </fo:page-sequence>

</xsl:template>


<!-- Page de titre de <balance> *********************************** -->
<xsl:template name="balance.titlepage">
  <xsl:call-template name="titlepage">
    <xsl:with-param name="type-doc" select="'Balance'"/>
  </xsl:call-template>
</xsl:template>

<!-- contenu de <balance> ************************************************ -->
<xsl:template name="balance.content">
  <fo:block font-size="18pt" 
            font-family="sans-serif"
            space-before="1em"
            space-after="1.5em"
            font-weight="bold"
            text-align="center"
            break-before="page">
     <xsl:text>Balance entre le </xsl:text>
     <xsl:value-of select="@debut"/> 
     <xsl:text> et le </xsl:text>
     <xsl:value-of select="@fin"/>
   </fo:block>

    <fo:table table-layout="fixed"  width="18cm"
              border-top-width="0.5pt" 
              border-top-style="solid"
              border-bottom-width="0.5pt" 
              border-bottom-style="solid"
              border-right-width="0.5pt" 
              border-right-style="solid"
              border-left-width="0.5pt" 
              border-left-style="solid">

      <fo:table-column column-number="1" 
                       column-width="2.4cm"/>
      <fo:table-column column-number="2"
                       column-width="4.5cm"/>
      <fo:table-column column-number="3" 
                       column-width="1.85cm"/>
      <fo:table-column column-number="4" 
                       column-width="1.85cm"/>
      <fo:table-column column-number="5"
                       column-width="1.85cm"/>
      <fo:table-column column-number="6" 
                       column-width="1.85cm"/>
      <fo:table-column column-number="7"
                       column-width="1.85cm"/>
      <fo:table-column column-number="8" 
                       column-width="1.85cm"/>

      <fo:table-header>
        <fo:table-row>
          <fo:table-cell padding="0.1cm"
                         border-bottom-style="solid"
                         border-bottom-width="0.5pt"
                         border-right-style="solid"
                         border-right-width="0.5pt"
                         number-rows-spanned="2"
                         number-columns-spanned="2">
            <fo:block text-align="center"
                      vertical-align="middle"
                      font-size="8pt">Compte</fo:block>
          </fo:table-cell>
          <fo:table-cell padding="0.1cm"
                         border-bottom-style="solid"
                         border-bottom-width="0.5pt"
                         border-right-style="solid"
                         border-right-width="0.5pt"
                         number-columns-spanned="2">
            <fo:block text-align="center"
                      vertical-align="middle"
                      font-size="8pt">Report</fo:block>
          </fo:table-cell>
          <fo:table-cell padding="0.1cm"
                         border-bottom-style="solid"
                         border-bottom-width="0.5pt"
                         border-right-style="solid"
                         border-right-width="0.5pt"
                         number-columns-spanned="2">
            <fo:block text-align="center"
                      vertical-align="middle"
                      font-size="8pt">Période</fo:block>
          </fo:table-cell>
          <fo:table-cell padding="0.1cm"
                         border-bottom-style="solid"
                         border-bottom-width="0.5pt"
                         number-columns-spanned="2">
            <fo:block text-align="center"
                      vertical-align="middle"
                      font-size="8pt">Solde</fo:block>
          </fo:table-cell>
        </fo:table-row>
        <fo:table-row>
          <fo:table-cell padding="0.1cm"
                         border-bottom-style="solid"
                         border-bottom-width="0.5pt"
                         border-right-style="solid"
                         border-right-width="0.5pt">
            <fo:block text-align="center"
                      vertical-align="middle"
                      font-size="8pt">Débit</fo:block>
          </fo:table-cell>
          <fo:table-cell padding="0.1cm"
                         border-bottom-style="solid"
                         border-bottom-width="0.5pt"
                         border-right-style="solid"
                         border-right-width="0.5pt">
            <fo:block text-align="center"
                      vertical-align="middle"
                      font-size="8pt">Crédit</fo:block>
          </fo:table-cell>
          <fo:table-cell padding="0.1cm"
                         border-bottom-style="solid"
                         border-bottom-width="0.5pt"
                         border-right-style="solid"
                         border-right-width="0.5pt">
            <fo:block text-align="center"
                      vertical-align="middle"
                      font-size="8pt">Débit</fo:block>
          </fo:table-cell>
          <fo:table-cell padding="0.1cm"
                         border-bottom-style="solid"
                         border-bottom-width="0.5pt"
                         border-right-style="solid"
                         border-right-width="0.5pt">
            <fo:block text-align="center"
                      vertical-align="middle"
                      font-size="8pt">Crédit</fo:block>
          </fo:table-cell>
          <fo:table-cell padding="0.1cm"
                         border-bottom-style="solid"
                         border-bottom-width="0.5pt"
                         border-right-style="solid"
                         border-right-width="0.5pt">
            <fo:block text-align="center"
                      vertical-align="middle"
                      font-size="8pt">Débit</fo:block>
          </fo:table-cell>
          <fo:table-cell padding="0.1cm"
                         border-bottom-style="solid"
                         border-bottom-width="0.5pt">
            <fo:block text-align="center"
                      vertical-align="middle"
                      font-size="8pt">Crédit</fo:block>
          </fo:table-cell>
        </fo:table-row>
      </fo:table-header>

      <fo:table-body>
        <!-- Les comptes -->
        <xsl:apply-templates select="compte">
          <xsl:sort select="@numero"/>
        </xsl:apply-templates>

        <!-- Les totaux -->
        <fo:table-row>
          <fo:table-cell padding="0.1cm"
                         border-bottom-width="0.5pt"
                         border-bottom-style="solid"
                         number-columns-spanned="8">
            <fo:block space-before="0.25cm"/>
          </fo:table-cell>
        </fo:table-row>
        <fo:table-row>
          <fo:table-cell padding="0.1cm">
	    <fo:block/>
	  </fo:table-cell>
          <fo:table-cell padding="0.1cm"
                         border-right-style="solid"
                         border-right-width="0.5pt">
            <fo:block font-weight="bold"
                      font-size="7.5pt">Totaux sur la période</fo:block>
          </fo:table-cell>
          <fo:table-cell padding="0.1cm"
                         border-right-style="solid"
                         border-right-width="0.5pt">
            <fo:block font-weight="bold"
                      font-size="7.5pt"
                      text-align="right">
              <xsl:call-template name="format-montant">
                <xsl:with-param name="montant"
                                select="
       sum( compte[sum(@report-debit) > sum(@report-credit)] /@report-debit ) 
     - sum( compte[sum(@report-debit) > sum(@report-credit)] /@report-credit )
                                       "/>
              </xsl:call-template>
            </fo:block>
          </fo:table-cell>
          <fo:table-cell padding="0.1cm"
                         border-right-style="solid"
                         border-right-width="0.5pt">
            <fo:block font-weight="bold"
                      font-size="7.5pt"
                      text-align="right">
              <xsl:call-template name="format-montant">
                <xsl:with-param name="montant"
                                select="
       sum( compte[sum(@report-credit) > sum(@report-debit)] /@report-credit ) 
     - sum( compte[sum(@report-credit) > sum(@report-debit)] /@report-debit )
                                       "/>
              </xsl:call-template>
            </fo:block>
          </fo:table-cell>
          <fo:table-cell padding="0.1cm"
                         border-right-style="solid"
                         border-right-width="0.5pt">
            <fo:block font-weight="bold"
                      font-size="7.5pt"
                      text-align="right">
              <xsl:call-template name="format-montant">
                <xsl:with-param name="montant"
                                select="
             sum( compte[sum(@debit) > sum(@report-debit)] /@debit ) 
           - sum( compte[sum(@debit) > sum(@report-debit)] /@report-debit )
                                       "/>
              </xsl:call-template>
            </fo:block>
          </fo:table-cell>
          <fo:table-cell padding="0.1cm"
                         border-right-style="solid"
                         border-right-width="0.5pt">
            <fo:block font-weight="bold"
                      font-size="7.5pt"
                      text-align="right">
              <xsl:call-template name="format-montant">
                <xsl:with-param name="montant"
                                select="
             sum( compte[sum(@credit) > sum(@report-credit)] /@credit ) 
           - sum( compte[sum(@credit) > sum(@report-credit)] /@report-credit )
                                       "/>
              </xsl:call-template>
            </fo:block>
          </fo:table-cell>
          <fo:table-cell padding="0.1cm"
                         border-right-style="solid"
                         border-right-width="0.5pt">
            <fo:block font-weight="bold"
                      font-size="7.5pt"
                      text-align="right">
              <xsl:call-template name="format-montant">
                <xsl:with-param name="montant"
                                select="
                           sum( compte[sum(@debit) > sum(@credit)] /@debit ) 
                         - sum( compte[sum(@debit) > sum(@credit)] /@credit )
                                       "/>
              </xsl:call-template>
            </fo:block>
          </fo:table-cell>
          <fo:table-cell padding="0.1cm">
            <fo:block font-weight="bold"
                      font-size="7.5pt"
                      text-align="right">
              <xsl:call-template name="format-montant">
                <xsl:with-param name="montant"
                                select="
                           sum( compte[sum(@credit) > sum(@debit)] /@credit ) 
                         - sum( compte[sum(@credit) > sum(@debit)] /@debit )
                                       "/>
              </xsl:call-template>
            </fo:block>
          </fo:table-cell>
        </fo:table-row>

      </fo:table-body>
    </fo:table>
</xsl:template>


<!-- <compte> ***************************************************** -->
<xsl:template match="compte">
  <fo:table-row>

    <fo:table-cell padding="0.1cm"
                   border-bottom-style="solid"
                   border-bottom-width="0.5pt">
      <fo:block font-size="7.5pt">
        <xsl:text>Compte </xsl:text>
        <xsl:value-of select="@numero"/>
      </fo:block>
    </fo:table-cell>
    <fo:table-cell padding="0.1cm"
                   border-bottom-style="solid"
                   border-bottom-width="0.5pt"
                   border-right-style="solid"
                   border-right-width="0.5pt">
      <fo:block font-size="7.5pt">
        <xsl:apply-templates select="$plan_comptable">
          <xsl:with-param name="numero" select="@numero"/>
        </xsl:apply-templates>
      </fo:block>
    </fo:table-cell>

    <fo:table-cell padding="0.1cm"
                   border-bottom-style="solid"
                   border-bottom-width="0.5pt"
                   border-right-style="solid"
                   border-right-width="0.5pt">
      <fo:block font-size="7.5pt"
                text-align="right">
        <xsl:if test="@report-debit > @report-credit">
          <xsl:call-template name="format-montant">
            <xsl:with-param name="montant"
                            select="@report-debit - @report-credit"/>
          </xsl:call-template>
        </xsl:if>
      </fo:block>
    </fo:table-cell>
    <fo:table-cell padding="0.1cm"
                   border-bottom-style="solid"
                   border-bottom-width="0.5pt"
                   border-right-style="solid"
                   border-right-width="0.5pt">
      <fo:block font-size="7.5pt"
                text-align="right">
        <xsl:if test="@report-credit > @report-debit">
          <xsl:call-template name="format-montant">
            <xsl:with-param name="montant"
                            select="@report-credit - @report-debit"/>
          </xsl:call-template>
        </xsl:if>
      </fo:block>
    </fo:table-cell>

    <fo:table-cell padding="0.1cm"
                   border-bottom-style="solid"
                   border-bottom-width="0.5pt"
                   border-right-style="solid"
                   border-right-width="0.5pt">
      <fo:block font-size="7.5pt"
                text-align="right">
        <xsl:if test="@debit > @report-debit">
          <xsl:call-template name="format-montant">
            <xsl:with-param name="montant"
                            select="@debit - @report-debit"/>
          </xsl:call-template>
        </xsl:if>
      </fo:block>
    </fo:table-cell>
    <fo:table-cell padding="0.1cm"
                   border-bottom-style="solid"
                   border-bottom-width="0.5pt"
                   border-right-style="solid"
                   border-right-width="0.5pt">
      <fo:block font-size="7.5pt"
                text-align="right">
        <xsl:if test="@credit > @report-credit">
          <xsl:call-template name="format-montant">
            <xsl:with-param name="montant"
                            select="@credit - @report-credit"/>
          </xsl:call-template>
        </xsl:if>
      </fo:block>
    </fo:table-cell>

    <fo:table-cell padding="0.1cm"
                   border-bottom-style="solid"
                   border-bottom-width="0.5pt"
                   border-right-style="solid"
                   border-right-width="0.5pt">
      <fo:block font-size="7.5pt"
                text-align="right">
        <xsl:if test="@debit > @credit">
          <xsl:call-template name="format-montant">
            <xsl:with-param name="montant"
                            select="@debit - @credit"/>
          </xsl:call-template>
        </xsl:if>
      </fo:block>
    </fo:table-cell>
    <fo:table-cell padding="0.1cm"
                   border-bottom-style="solid"
                   border-bottom-width="0.5pt">
      <fo:block font-size="7.5pt"
                text-align="right">
        <xsl:if test="@credit > @debit">
          <xsl:call-template name="format-montant">
            <xsl:with-param name="montant"
                            select="@credit - @debit"/>
          </xsl:call-template>
        </xsl:if>
      </fo:block>
    </fo:table-cell>    

  </fo:table-row>
</xsl:template>

</xsl:stylesheet>