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

<!-- <journaux> ****************************** -->
<xsl:template match="journaux">
  <fo:page-sequence master-reference="A4">

    <fo:static-content flow-name="xsl-region-after">
      <xsl:call-template name="footer"/>
    </fo:static-content>

    <fo:flow flow-name="xsl-region-body">
      <xsl:call-template name="journaux.titlepage"/>
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
                <xsl:text>Journaux Mensuels du </xsl:text>
                <xsl:value-of select="@debut"/> 
                <xsl:text> au </xsl:text>
                <xsl:value-of select="@fin"/>
                <xsl:text> - Liste des journaux</xsl:text>
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
      <xsl:call-template name="journaux.table.of.content"/>
    </fo:flow>

  </fo:page-sequence>

</xsl:template>


<!-- Page de titre de <journaux> *********************************** -->
<xsl:template name="journaux.titlepage">
  <xsl:call-template name="titlepage">
    <xsl:with-param name="type-doc" select="'Journaux Mensuels'"/>
  </xsl:call-template>
</xsl:template>


<!-- Liste des journaux mensuels de <journaux> ************************* -->
<xsl:template name="journaux.table.of.content">
  <fo:block font-size="16pt" 
            font-family="sans-serif"
            space-before="1em"
            space-after="1.5em"
            font-weight="bold"
            text-align="center"
            break-before="page">
    <xsl:text>Journaux Mensuels du </xsl:text>
    <xsl:value-of select="@debut"/>
    <xsl:text> au </xsl:text>
    <xsl:value-of select="@fin"/>
  </fo:block>

  <fo:block font-size="10pt"
            font-weight="bold"
            space-before="0cm"
            space-after="1em">
    <xsl:text>Liste des journaux mensuels</xsl:text>
  </fo:block>

  <xsl:apply-templates select="journal" mode="toc">
    <xsl:sort select="@debut"/>
  </xsl:apply-templates>

</xsl:template>


<!-- <journal>  mode 'toc' ********************************** -->
<xsl:template match="journal" mode="toc">

  <fo:block font-size="8pt"
	    text-align-last="justify">
    <fo:basic-link internal-destination="{generate-id(.)}">
      <xsl:text>Journal mensuel du </xsl:text>
      <xsl:value-of select="@debut"/>
      <xsl:text> au </xsl:text>
      <xsl:value-of select="@fin"/>
    </fo:basic-link>
    <xsl:text> </xsl:text>
    <fo:leader leader-length.minimum="12pt" leader-length.optimum="40pt"
	       leader-length.maximum="100%" leader-pattern="dots"/>
    <fo:basic-link internal-destination="{generate-id(.)}">
      <fo:page-number-citation ref-id="{generate-id(.)}"/>
    </fo:basic-link>
  </fo:block>

</xsl:template>


<!-- <journal> ****************************************** -->
<xsl:template match="journal">
  <!-- si c'est le noeud racine, insère une page de titre -->
  <xsl:if test="not(parent::*)">
    <fo:page-sequence master-reference="A4">

      <fo:static-content flow-name="xsl-region-after">
        <xsl:call-template name="footer"/>
      </fo:static-content>

      <fo:flow flow-name="xsl-region-body">
        <xsl:call-template name="journal.titlepage"/>
      </fo:flow>

    </fo:page-sequence>    
  </xsl:if>

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
                <xsl:if test="ancestor::journaux">
                  <xsl:text>Journaux Mensuels - </xsl:text>
                </xsl:if>
                <xsl:text>Journal </xsl:text>
                <xsl:if test="ancestor::journaux">
                  <xsl:text>Mensuel </xsl:text>
                </xsl:if>
                <xsl:text>du </xsl:text>
                <xsl:value-of select="@debut"/> 
                <xsl:text> au </xsl:text>
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
      <xsl:call-template name="journal.content"/>
    </fo:flow>

  </fo:page-sequence>
</xsl:template>


<!-- Page de titre de <journal> **************************************** -->
<xsl:template name="journal.titlepage">
  <xsl:call-template name="titlepage">
    <xsl:with-param name="type-doc" select="'Journal'"/>
  </xsl:call-template>
</xsl:template>


<!-- contenu de <journal> ********************************************** -->
<xsl:template name="journal.content">
  <fo:block id="{generate-id(.)}"
            break-before="page"
            font-size="16pt" 
            font-family="sans-serif"
            space-before="1em"
            space-after="1.5em"
            font-weight="bold">
    <xsl:text>Journal du </xsl:text>
    <xsl:value-of select="@debut"/>
    <xsl:text> au </xsl:text>
    <xsl:value-of select="@fin"/>
  </fo:block>

 <fo:table table-layout="fixed" width="18cm"
           border-width="0.5pt" 
           border-style="solid">

  <fo:table-column column-number="1" 
                   column-width="1.5cm"/>
  <fo:table-column column-number="2" 
                   column-width="1.5cm"/>
  <fo:table-column column-number="3" 
                   column-width="1.5cm"/>
  <fo:table-column column-number="4" 
                   column-width="10cm"/>
  <fo:table-column column-number="5" 
                   column-width="1.75cm"/>
  <fo:table-column column-number="6" 
                   column-width="1.75cm"/>

  <fo:table-header>
    <fo:table-row keep-with-next="always">
      <fo:table-cell padding="0.1cm"
                     number-rows-spanned="2" 
                     border-bottom-width="0.5pt" 
                     border-bottom-style="solid"
                     border-right-width="0.5pt" 
                     border-right-style="solid">
        <fo:block font-size="8pt"
                  text-align="center"
                  vertical-align="middle">Date écrit.</fo:block>
      </fo:table-cell>
      <fo:table-cell padding="0.1cm"
                     number-columns-spanned="2" 
                     border-bottom-width="0.5pt" 
                     border-bottom-style="solid" 
                     border-right-width="0.5pt" 
                     border-right-style="solid">
        <fo:block font-size="8pt"
                  text-align="center"
                  vertical-align="middle">Comptes</fo:block>
      </fo:table-cell>
      <fo:table-cell padding="0.1cm"
                     number-rows-spanned="2" 
                     border-bottom-width="0.5pt" 
                     border-bottom-style="solid" 
                     border-right-width="0.5pt" 
                     border-right-style="solid">
        <fo:block font-size="8pt"
                  text-align="center"
                  vertical-align="middle">Désignation</fo:block>
      </fo:table-cell>
      <fo:table-cell padding="0.1cm"
                     number-columns-spanned="2"
                     border-bottom-width="0.5pt" 
                     border-bottom-style="solid">
        <fo:block font-size="8pt"
                  text-align="center"
                  vertical-align="middle">Montants</fo:block>
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
                  vertical-align="middle">Débit</fo:block>
      </fo:table-cell>
      <fo:table-cell padding="0.1cm"
                     border-bottom-width="0.5pt" 
                     border-bottom-style="solid" 
                     border-right-width="0.5pt" 
                     border-right-style="solid">
        <fo:block font-size="8pt"
                  text-align="center"
                  vertical-align="middle">Crédit</fo:block>
      </fo:table-cell>
      <fo:table-cell padding="0.1cm"
                     border-bottom-width="0.5pt" 
                     border-bottom-style="solid" 
                     border-right-width="0.5pt" 
                     border-right-style="solid">
        <fo:block font-size="8pt"
                  text-align="center"
                  vertical-align="middle">Débit</fo:block>
      </fo:table-cell>
      <fo:table-cell padding="0.1cm"
                     border-bottom-width="0.5pt" 
                     border-bottom-style="solid">
        <fo:block font-size="8pt"
                  text-align="center"
                  vertical-align="middle">Crédit</fo:block>
      </fo:table-cell>
    </fo:table-row>
  </fo:table-header>

  <fo:table-body>
    <xsl:apply-templates select="ecriture">
      <xsl:sort select="@date" order="ascending"/>
    </xsl:apply-templates>
  </fo:table-body>

 </fo:table>
</xsl:template>


<!-- <ecriture> ************************************* -->
<xsl:template match="ecriture">

  <!-- date, écriture -->
  <fo:table-row keep-with-next="always">
    <fo:table-cell padding-top="0.1cm"
                   padding-left="0.1cm"
                   padding-right="0.1cm"
                   border-right-width="0.5pt" 
                   border-right-style="solid">
      <fo:block font-size="7pt" 
                font-family="sans-serif">
        <xsl:value-of select="@date"/>      
      </fo:block>
    </fo:table-cell>
    <fo:table-cell padding-top="0.1cm"
                   padding-left="0.1cm"
                   padding-right="0.1cm"
                   border-right-width="0.5pt" 
                   border-right-style="solid">
      <fo:block/>
    </fo:table-cell>
    <fo:table-cell padding-top="0.1cm"
                   padding-left="0.1cm"
                   padding-right="0.1cm"
                   border-right-width="0.5pt" 
                   border-right-style="solid">
      <fo:block/>
    </fo:table-cell>
    <fo:table-cell padding-top="0.1cm"
                   padding-left="0.1cm"
                   padding-right="0.1cm"
                   border-right-width="0.5pt" 
                   border-right-style="solid">
      <fo:block font-size="8pt" 
                font-family="sans-serif" 
                font-style="italic"
                font-weight="bold">
        <xsl:if test="not(reglement)">
          <xsl:attribute name="space-after">
            <xsl:text>0.1cm</xsl:text>
          </xsl:attribute>
        </xsl:if>
        <xsl:value-of select="libelle"/>
      </fo:block>
      <xsl:if test="reglement">
        <fo:block space-after="0.1cm" 
                  start-indent="1cm" 
                  font-size="7.5pt" 
                  font-family="sans-serif">
          <xsl:text>Règlement </xsl:text>
          <xsl:value-of select="reglement/@type"/>
          <xsl:text> </xsl:text>
          <xsl:value-of select="reglement"/>
        </fo:block>
      </xsl:if>
    </fo:table-cell>
    <fo:table-cell padding-top="0.1cm"
                   padding-left="0.1cm"
                   padding-right="0.1cm"
                   border-right-width="0.5pt" 
                   border-right-style="solid">
      <fo:block/>
    </fo:table-cell>
    <fo:table-cell padding-top="0.1cm"
                   padding-left="0.1cm"
                   padding-right="0.1cm">
      <fo:block/>
    </fo:table-cell>
  </fo:table-row>

  <!-- Détail debit/credit -->
  <xsl:apply-templates select="debit"/>
  <xsl:apply-templates select="credit"/>

</xsl:template>


<!-- <debit> ************************************************* -->
<xsl:template match="debit">
  <fo:table-row keep-with-next="always">
    <fo:table-cell padding-left="0.1cm"
                   padding-right="0.1cm"
                   border-right-width="0.5pt" 
                   border-right-style="solid">
      <fo:block/>
    </fo:table-cell>
    <fo:table-cell padding-left="0.1cm"
                   padding-right="0.1cm"
                   border-right-width="0.5pt" 
                   border-right-style="solid">
      <fo:block font-size="7pt" 
                font-family="sans-serif">
        <xsl:if test="position()=last()">
          <xsl:attribute name="space-after">
            <xsl:text>0.1cm</xsl:text>
          </xsl:attribute>
        </xsl:if>
        <xsl:value-of select="@compte"/>
      </fo:block>
    </fo:table-cell>
    <fo:table-cell padding-left="0.1cm"
                   padding-right="0.1cm" 
                   border-right-width="0.5pt" 
                   border-right-style="solid">
      <fo:block/>
    </fo:table-cell>
    <fo:table-cell padding-left="0.1cm"
                   padding-right="0.1cm"
                   border-right-width="0.5pt" 
                   border-right-style="solid">  
      <fo:block font-size="7pt" 
                font-family="sans-serif">
        <xsl:if test="position()=last()">
          <xsl:attribute name="space-after">
            <xsl:text>0.1cm</xsl:text>
          </xsl:attribute>
        </xsl:if>
        <xsl:apply-templates select="$plan_comptable">
          <xsl:with-param name="numero" select="@compte"/>
        </xsl:apply-templates>
      </fo:block>
    </fo:table-cell>
    <fo:table-cell padding-left="0.1cm"
                   padding-right="0.1cm"
                   border-right-width="0.5pt" 
                   border-right-style="solid">
      <fo:block font-size="7pt" 
                font-family="sans-serif"
                text-align="end">
        <xsl:if test="position()=last()">
          <xsl:attribute name="space-after">
            <xsl:text>0.1cm</xsl:text>
          </xsl:attribute>
        </xsl:if>
        <xsl:call-template name="format-montant">
          <xsl:with-param name="montant" select="@montant"/>
        </xsl:call-template>
      </fo:block>
    </fo:table-cell>
    <fo:table-cell padding-left="0.1cm"
                   padding-right="0.1cm">
      <fo:block/>
    </fo:table-cell>
  </fo:table-row>
</xsl:template>


<!-- <credit> ********************************************* -->
<xsl:template match="credit"> 
  <fo:table-row>
    <xsl:if test="position()!=last()">
      <xsl:attribute name="keep-with-next">
        <xsl:text>always</xsl:text>
      </xsl:attribute>
    </xsl:if>
    <fo:table-cell padding-left="0.1cm"
                   padding-right="0.1cm" 
                   border-right-width="0.5pt" 
                   border-right-style="solid">
      <xsl:if test="position()=last()">
        <xsl:attribute name="padding-bottom">
          <xsl:text>0.1cm</xsl:text>
        </xsl:attribute>
        <xsl:attribute name="border-bottom-width">
          <xsl:text>0.5pt</xsl:text>
        </xsl:attribute>
        <xsl:attribute name="border-bottom-style">
          <xsl:text>solid</xsl:text>
        </xsl:attribute>
      </xsl:if>
      <fo:block/>
    </fo:table-cell>
    <fo:table-cell padding-left="0.1cm"
                   padding-right="0.1cm"
                   border-right-width="0.5pt" 
                   border-right-style="solid">
      <xsl:if test="position()=last()">
        <xsl:attribute name="padding-bottom">
          <xsl:text>0.1cm</xsl:text>
        </xsl:attribute>
        <xsl:attribute name="border-bottom-width">
          <xsl:text>0.5pt</xsl:text>
        </xsl:attribute>
        <xsl:attribute name="border-bottom-style">
          <xsl:text>solid</xsl:text>
        </xsl:attribute>
      </xsl:if>
      <fo:block/>
    </fo:table-cell>
    <fo:table-cell padding-left="0.1cm"
                   padding-right="0.1cm"
                   border-right-width="0.5pt" 
                   border-right-style="solid">
      <xsl:if test="position()=last()">
        <xsl:attribute name="padding-bottom">
          <xsl:text>0.1cm</xsl:text>
        </xsl:attribute>
        <xsl:attribute name="border-bottom-width">
          <xsl:text>0.5pt</xsl:text>
        </xsl:attribute>
        <xsl:attribute name="border-bottom-style">
          <xsl:text>solid</xsl:text>
        </xsl:attribute>
      </xsl:if>
      <fo:block font-size="7pt" 
                font-family="sans-serif">
        <xsl:if test="position()=last()">
          <xsl:attribute name="space-after">
            <xsl:text>0.1cm</xsl:text>
          </xsl:attribute>
        </xsl:if>
        <xsl:value-of select="@compte"/>
      </fo:block>
    </fo:table-cell>
    <fo:table-cell padding-left="0.1cm"
                   padding-right="0.1cm"
                   border-right-width="0.5pt" 
                   border-right-style="solid">
      <xsl:if test="position()=last()">
        <xsl:attribute name="padding-bottom">
          <xsl:text>0.1cm</xsl:text>
        </xsl:attribute>
        <xsl:attribute name="border-bottom-width">
          <xsl:text>0.5pt</xsl:text>
        </xsl:attribute>
        <xsl:attribute name="border-bottom-style">
          <xsl:text>solid</xsl:text>
        </xsl:attribute>
      </xsl:if>
      <fo:block font-size="7pt" 
                font-family="sans-serif">
        <xsl:if test="position()=last()">
          <xsl:attribute name="space-after">
            <xsl:text>0.1cm</xsl:text>
          </xsl:attribute>
        </xsl:if>
        <xsl:apply-templates select="$plan_comptable">
          <xsl:with-param name="numero" select="@compte"/>
        </xsl:apply-templates>
      </fo:block>
    </fo:table-cell>
    <fo:table-cell padding-left="0.1cm"
                   padding-right="0.1cm"
                   border-right-width="0.5pt" 
                   border-right-style="solid">
      <xsl:if test="position()=last()">
        <xsl:attribute name="padding-bottom">
          <xsl:text>0.1cm</xsl:text>
        </xsl:attribute>
        <xsl:attribute name="border-bottom-width">
          <xsl:text>0.5pt</xsl:text>
        </xsl:attribute>
        <xsl:attribute name="border-bottom-style">
          <xsl:text>solid</xsl:text>
        </xsl:attribute>
      </xsl:if>
      <fo:block/>
    </fo:table-cell>
    <fo:table-cell padding-left="0.1cm"
                   padding-right="0.1cm">
      <xsl:if test="position()=last()">
        <xsl:attribute name="padding-bottom">
          <xsl:text>0.1cm</xsl:text>
        </xsl:attribute>
        <xsl:attribute name="border-bottom-width">
          <xsl:text>0.5pt</xsl:text>
        </xsl:attribute>
        <xsl:attribute name="border-bottom-style">
          <xsl:text>solid</xsl:text>
        </xsl:attribute>
      </xsl:if>
      <fo:block font-size="7pt" 
                font-family="sans-serif"
                text-align="end">
        <xsl:if test="position()=last()">
          <xsl:attribute name="space-after">
            <xsl:text>0.1cm</xsl:text>
          </xsl:attribute>
        </xsl:if>
        <xsl:call-template name="format-montant">
          <xsl:with-param name="montant" select="@montant"/>
        </xsl:call-template>
      </fo:block>
    </fo:table-cell>
  </fo:table-row>
</xsl:template>


<!-- references **************************************************** -->

<xsl:template match="ref[@type='doc']"/>

<xsl:template match="ref[@type='personne']"/>

<xsl:template match="ref[@type='societe']"/>

<xsl:template match="ref[@type='affaire']"/>


</xsl:stylesheet>