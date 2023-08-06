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

<!-- <grand-livre> ****************************** -->
<xsl:template match="grand-livre">
  <fo:page-sequence master-reference="A4">

    <fo:static-content flow-name="xsl-region-after">
      <xsl:call-template name="footer"/>
    </fo:static-content>

    <fo:flow flow-name="xsl-region-body">
      <xsl:call-template name="grand-livre.titlepage"/>
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
                <xsl:text>Grand Livre du </xsl:text>
                <xsl:value-of select="@debut"/> 
                <xsl:text> au </xsl:text>
                <xsl:value-of select="@fin"/>
                <xsl:text> - Liste des comptes</xsl:text>
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
      <xsl:call-template name="grand-livre.table.of.content"/>
    </fo:flow>

  </fo:page-sequence>

  <xsl:apply-templates select="compte">
    <xsl:sort select="@num"/>
  </xsl:apply-templates>

</xsl:template>


<!-- Page de titre de <grand-livre> *********************************** -->
<xsl:template name="grand-livre.titlepage">
  <xsl:call-template name="titlepage">
    <xsl:with-param name="type-doc" select="'Grand Livre'"/>
  </xsl:call-template>
</xsl:template>


<!-- Liste des comptes de <grand-livre> ********************************* -->
<xsl:template name="grand-livre.table.of.content">
  <fo:block font-size="18pt" 
            font-family="sans-serif"
            space-before="1em"
            space-after="1.5em"
            font-weight="bold"
            text-align="center"
            break-before="page">
    <xsl:text>Grand Livre du </xsl:text>
    <xsl:value-of select="@debut"/> 
    <xsl:text> au </xsl:text>
    <xsl:value-of select="@fin"/>
  </fo:block>

  <fo:block font-size="10pt"
            font-weight="bold"
            space-before="0cm"
            space-after="1em">
    <xsl:text>Liste des comptes</xsl:text>
  </fo:block>

  <fo:table table-layout="fixed" width="18cm">
    <fo:table-column column-number="1"
                     column-width="3.3cm"/>
    <fo:table-column column-number="2"
                     column-width="14.7cm"/>
    <fo:table-body>
      <xsl:apply-templates select="compte" mode="toc">
        <xsl:sort select="@num"/>
      </xsl:apply-templates>
    </fo:table-body>
  </fo:table>
</xsl:template>


<!-- <compte> mode "toc" *********************************** -->
<xsl:template match="compte" mode="toc">
  <fo:table-row>
    <fo:table-cell>
      <fo:block font-size="8pt">
        <fo:basic-link internal-destination="{generate-id(.)}">
          <xsl:text>Compte </xsl:text>
          <xsl:value-of select="@num"/>
        </fo:basic-link>
      </fo:block>
    </fo:table-cell>
    <fo:table-cell>
      <fo:block font-size="8pt"
                text-align-last="justify">
        <fo:basic-link internal-destination="{generate-id(.)}">
          <xsl:apply-templates select="$plan_comptable">
            <xsl:with-param name="numero" select="@num"/>
          </xsl:apply-templates>
        </fo:basic-link>
        <xsl:text> </xsl:text>
        <fo:leader leader-length.minimum="12pt" leader-length.optimum="40pt"
                   leader-length.maximum="100%" leader-pattern="dots"/>
        <fo:basic-link internal-destination="{generate-id(.)}">
	  <fo:page-number-citation ref-id="{generate-id(.)}"/>
	</fo:basic-link>
      </fo:block>
    </fo:table-cell>
  </fo:table-row>
</xsl:template>


<!-- <compte> ****************************************** -->
<xsl:template match="compte">
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
                <xsl:text>Grand Livre du </xsl:text>
                <xsl:value-of select="ancestor::grand-livre/@debut"/> 
                <xsl:text> au </xsl:text>
                <xsl:value-of select="ancestor::grand-livre/@fin"/>
                <xsl:text> - Compte </xsl:text>
                <xsl:value-of select="@num"/>
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
      <xsl:call-template name="compte.content"/>
    </fo:flow>

  </fo:page-sequence>
</xsl:template>


<!-- contenu de <compte> ********************************************* -->
<xsl:template name="compte.content">
  <fo:block id="{generate-id(.)}"
            break-before="page"
            font-size="16pt" 
            font-family="sans-serif"
            space-before="1em"
            space-after="1.5em"
            font-weight="bold">
    <xsl:text>Compte </xsl:text>
    <xsl:value-of select="@num"/>
    <xsl:text> - </xsl:text>
    <xsl:apply-templates select="$plan_comptable">
      <xsl:with-param name="numero" select="@num"/>
    </xsl:apply-templates>
  </fo:block>

<fo:table table-layout="fixed" width="18cm"
           border-top-width="0.5pt" 
           border-top-style="solid"
           border-right-width="0.5pt" 
           border-right-style="solid"
           border-left-width="0.5pt" 
           border-left-style="solid"
	   space-before="0.25cm">

  <fo:table-column column-number="1" 
		   column-width="1.5cm"/>
  <fo:table-column column-number="2" 
		   column-width="5.70cm"/>
  <fo:table-column column-number="3" 
		   column-width="1.75cm"/>
  <fo:table-column column-number="4"
                   column-width="0.1cm"/>
  <fo:table-column column-number="5" 
		   column-width="1.5cm"/>
  <fo:table-column column-number="6" 
		   column-width="5.70cm"/>
  <fo:table-column column-number="7" 
		   column-width="1.75cm"/>
  
  <fo:table-header>
    <fo:table-row keep-with-next="always">
      <fo:table-cell padding="0.1cm"
		     number-columns-spanned="3" 
		     border-bottom-width="0.5pt" 
		     border-bottom-style="solid"
		     border-right-width="0.5pt" 
		     border-right-style="solid">
	<fo:block font-size="8pt"
		  text-align="center"
		  vertical-align="middle">Débit</fo:block>
      </fo:table-cell>
      <fo:table-cell border-right-width="0.5pt" 
		     border-right-style="solid">
	<fo:block/>
      </fo:table-cell>
      <fo:table-cell padding="0.1cm"
		     number-columns-spanned="3" 
		     border-bottom-width="0.5pt" 
		     border-bottom-style="solid">
	<fo:block font-size="8pt"
		  text-align="center"
		  vertical-align="middle">Crédit</fo:block>
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
		  vertical-align="middle">Date</fo:block>
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
		  vertical-align="middle">Montant</fo:block>
      </fo:table-cell>
      <fo:table-cell border-right-width="0.5pt" 
		     border-right-style="solid"
		     border-bottom-width="0.5pt"
		     border-bottom-style="solid">
	<fo:block/>
      </fo:table-cell>
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
		  vertical-align="middle">Libellé</fo:block>
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

    <!-- Première partie : les reports -->

    <fo:table-row>
      <fo:table-cell number-columns-spanned="7"
		     padding="0.1cm"
		     border-right-width="0.5pt" 
		     border-right-style="solid"
		     border-bottom-width="0.5pt" 
		     border-bottom-style="solid">
	<fo:block space-before="0.2cm"
		  font-size="7pt"
		  font-weight="bold">
	  <xsl:choose>
	    <xsl:when test="@report-debit > @report-credit">
	      <xsl:attribute name="text-align">start</xsl:attribute>
	      <xsl:text>Report Débit </xsl:text>
	      <xsl:call-template name="format-montant">
		<xsl:with-param name="montant" 
				select="@report-debit - @report-credit"/>
	      </xsl:call-template>
	    </xsl:when>
	    <xsl:when test="@report-debit = @report-credit">
	      <xsl:attribute name="text-align">center</xsl:attribute>
	      <xsl:text>Report Équilibré</xsl:text>
	    </xsl:when>
	    <xsl:otherwise>
	      <xsl:attribute name="text-align">end</xsl:attribute>
	      <xsl:text>Report Crédit </xsl:text>
	      <xsl:call-template name="format-montant">
		<xsl:with-param name="montant" 
				select="@report-credit - @report-debit"/>
	      </xsl:call-template>
	    </xsl:otherwise>
	  </xsl:choose>
	</fo:block>
      </fo:table-cell>
    </fo:table-row>

    <fo:table-row keep-with-previous="always">
      <fo:table-cell number-columns-spanned="7"
		     padding="0.1cm"
		     margin-top="0.25cm"
		     border-bottom-width="0.5pt"
		     border-bottom-style="solid">
	<fo:block />
      </fo:table-cell>
    </fo:table-row>


    <!-- Partie principale : les écritures de débit et de crédit -->
    <xsl:call-template name="process.debits.credits">
      <xsl:with-param name="debits" select="debit"/>
      <xsl:with-param name="credits" select="credit"/>
    </xsl:call-template>

    <!-- Dernière partie : les totaux -->
    <fo:table-row keep-with-next="always">
      <fo:table-cell number-columns-spanned="7"
		     padding="0.1cm"
		     margin-top="0.25cm"
		     border-bottom-width="0.5pt"
		     border-bottom-style="solid">
	<fo:block />
      </fo:table-cell>
    </fo:table-row>

    <fo:table-row keep-with-next="always">
      <fo:table-cell padding="0.1cm"
		     border-bottom-width="0.5pt"
		     border-bottom-style="solid">
	<fo:block/>
      </fo:table-cell>
      <fo:table-cell padding="0.1cm"
		     border-right-width="0.5pt" 
		     border-right-style="solid"
		     border-bottom-width="0.5pt"
		     border-bottom-style="solid">
	<fo:block font-size="7pt"
		  text-align="start"
		  font-style="italic">
	  <xsl:text>Total Débits</xsl:text>
	</fo:block>
      </fo:table-cell>
      <fo:table-cell padding="0.1cm"
		     border-right-width="0.5pt" 
		     border-right-style="solid"
		     border-bottom-width="0.5pt"
		     border-bottom-style="solid">
	<fo:block font-size="7pt"
		  text-align="end"
		  font-style="italic">
	  <xsl:call-template name="format-montant">
	    <xsl:with-param name="montant" 
			    select="@debit - @report-debit"/>
	  </xsl:call-template>
	</fo:block>
      </fo:table-cell>
      <fo:table-cell border-right-width="0.5pt" 
		     border-right-style="solid"
		     border-bottom-width="0.5pt"
		     border-bottom-style="solid">
	<fo:block/>
      </fo:table-cell>
      <fo:table-cell padding="0.1cm"
		     border-bottom-width="0.5pt"
		     border-bottom-style="solid">
	<fo:block/>
      </fo:table-cell>
      <fo:table-cell padding="0.1cm"
		     border-right-width="0.5pt" 
		     border-right-style="solid"
		     border-bottom-width="0.5pt"
		     border-bottom-style="solid">
	<fo:block font-size="7pt"
		  text-align="start"
		  font-style="italic">
	  <xsl:text>Total Crédits</xsl:text>
	</fo:block>
      </fo:table-cell>
      <fo:table-cell padding="0.1cm"
		     border-right-width="0.5pt" 
		     border-right-style="solid"
		     border-bottom-width="0.5pt"
		     border-bottom-style="solid">
	<fo:block font-size="7pt"
		  text-align="end"
		  font-style="italic">
	  <xsl:call-template name="format-montant">
	    <xsl:with-param name="montant" 
			    select="@credit - @report-credit"/>
	  </xsl:call-template>
	</fo:block>
      </fo:table-cell>
    </fo:table-row>
      
    <fo:table-row>
      <fo:table-cell number-columns-spanned="7"
		     padding="0.1cm"
		     border-right-width="0.5pt" 
		     border-right-style="solid"
		     border-bottom-width="0.5pt" 
		     border-bottom-style="solid">
	<fo:block space-before="0.2cm"
		  font-size="7pt"
		  font-weight="bold">
	  <xsl:choose>
	    <xsl:when test="@debit > @credit">
	      <xsl:attribute name="text-align">start</xsl:attribute>
	      <xsl:text>Compte Débiteur </xsl:text>
	      <xsl:call-template name="format-montant">
		<xsl:with-param name="montant" 
				select="@debit - @credit"/>
	      </xsl:call-template>
	    </xsl:when>
	    <xsl:when test="@debit = @credit">
	      <xsl:attribute name="text-align">center</xsl:attribute>
	      <xsl:text>Compte Équilibré</xsl:text>
	    </xsl:when>
	    <xsl:otherwise>
	      <xsl:attribute name="text-align">end</xsl:attribute>
	      <xsl:text>Compte Créditeur </xsl:text>
	      <xsl:call-template name="format-montant">
		<xsl:with-param name="montant" 
				select="@credit - @debit"/>
	      </xsl:call-template>
	    </xsl:otherwise>
	  </xsl:choose>
	</fo:block>
      </fo:table-cell>
    </fo:table-row>

  </fo:table-body>
</fo:table>

</xsl:template>


<xsl:template name="process.debits.credits">
 <xsl:param name="debits"/>
 <xsl:param name="credits"/>

 <xsl:choose>

   <xsl:when test="count($debits) = 0 and count($credits) = 0"/>

   <xsl:otherwise>

     <xsl:variable name="debit" select="$debits[position() = 1]"/>
     <xsl:variable name="credit" select="$credits[position() = 1]"/>

     <fo:table-row>

       <xsl:choose>

	 <xsl:when test="count($debit) = 0">

	   <fo:table-cell number-columns-spanned="3"
			  padding="0.1cm">
	     <fo:block/>
	   </fo:table-cell>

	 </xsl:when>

	 <xsl:otherwise>

	   <fo:table-cell padding="0.1cm"
			  border-right-width="0.5pt" 
			  border-right-style="solid">
	     <xsl:if test="count($debits) = 1">
	       <xsl:attribute name="border-bottom-width">0.5pt</xsl:attribute>
	       <xsl:attribute name="border-bottom-style">solid</xsl:attribute>
	     </xsl:if>
	     <fo:block font-size="7pt">
	       <xsl:value-of select="$debit/@date"/>
	     </fo:block>
	   </fo:table-cell>

	   <fo:table-cell padding="0.1cm"
			  border-right-width="0.5pt" 
			  border-right-style="solid">
	     <xsl:if test="count($debits) = 1">
	       <xsl:attribute name="border-bottom-width">0.5pt</xsl:attribute>
	       <xsl:attribute name="border-bottom-style">solid</xsl:attribute>
	     </xsl:if>
	     <fo:block font-size="7pt">
	       <xsl:value-of select="$debit/text()"/>
	     </fo:block>
	   </fo:table-cell>

	   <fo:table-cell padding="0.1cm"
			  border-right-width="0.5pt" 
			  border-right-style="solid">
	     <xsl:if test="count($debits) = 1">
	       <xsl:attribute name="border-bottom-width">0.5pt</xsl:attribute>
	       <xsl:attribute name="border-bottom-style">solid</xsl:attribute>
	     </xsl:if>
	     <fo:block font-size="7pt"
		       text-align="end">
	       <xsl:call-template name="format-montant">
		 <xsl:with-param name="montant" select="$debit/@montant"/>
	       </xsl:call-template>
	     </fo:block>
	   </fo:table-cell>

	 </xsl:otherwise>
       </xsl:choose>

       <fo:table-cell>
	 <fo:block/>
       </fo:table-cell>

       <xsl:choose>

	 <xsl:when test="count($credit) = 0">

	   <fo:table-cell number-columns-spanned="3"
			  padding="0.1cm"
			  border-right-width="0.5pt"
			  border-right-style="solid">
	     <fo:block/>
	   </fo:table-cell>

	 </xsl:when>

	 <xsl:otherwise>

	   <fo:table-cell padding="0.1cm"
			  border-left-width="0.5pt"
			  border-left-style="solid"
			  border-right-width="0.5pt" 
			  border-right-style="solid">
	     <xsl:if test="count($credits) = 1">
	       <xsl:attribute name="border-bottom-width">0.5pt</xsl:attribute>
	       <xsl:attribute name="border-bottom-style">solid</xsl:attribute>
	     </xsl:if>
	     <fo:block font-size="7pt">
	       <xsl:value-of select="$credit/@date"/>
	     </fo:block>
	   </fo:table-cell>

	   <fo:table-cell padding="0.1cm"
			  border-right-width="0.5pt" 
			  border-right-style="solid">
	     <xsl:if test="count($credits) = 1">
	       <xsl:attribute name="border-bottom-width">0.5pt</xsl:attribute>
	       <xsl:attribute name="border-bottom-style">solid</xsl:attribute>
	     </xsl:if>
	     <fo:block font-size="7pt">
	       <xsl:value-of select="$credit/text()"/>
	     </fo:block>
	   </fo:table-cell>

	   <fo:table-cell padding="0.1cm"
			  border-right-width="0.5pt" 
			  border-right-style="solid">
	     <xsl:if test="count($credits) = 1">
	       <xsl:attribute name="border-bottom-width">0.5pt</xsl:attribute>
	       <xsl:attribute name="border-bottom-style">solid</xsl:attribute>
	     </xsl:if>
	     <fo:block font-size="7pt"
		       text-align="end">
	       <xsl:call-template name="format-montant">
		 <xsl:with-param name="montant" select="$credit/@montant"/>
	       </xsl:call-template>
	     </fo:block>
	   </fo:table-cell>

	 </xsl:otherwise>
       </xsl:choose>

     </fo:table-row>

     <xsl:call-template name="process.debits.credits">
       <xsl:with-param name="debits" select="$debits[position() > 1]"/>
       <xsl:with-param name="credits" select="$credits[position() > 1]"/>
     </xsl:call-template>

   </xsl:otherwise>
 </xsl:choose>
</xsl:template>

</xsl:stylesheet>