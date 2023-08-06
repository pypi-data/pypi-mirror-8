<?xml version="1.0" encoding="ISO-8859-1"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

  <xsl:import href="common.xslt"/>

  <xsl:output method="text" encoding="ISO-8859-1" />

  <xsl:param name="societe.def" select="'../xml/societe.xml'"/>

  <xsl:decimal-format decimal-separator="," grouping-separator="."/>

  <xsl:variable name="societe" select="document($societe.def)/societe"/>
  <xsl:variable name="plan_comptable" select="document($societe/plan-comptable/text())/plan-comptable"/>

  <xsl:variable name="ext">
    <xsl:choose>
      <xsl:when test="substring(/balance/@debut,0,8) = substring(/balance/@fin,0,8)">
	<!-- Balance mensuelle -->
	<xsl:value-of select="substring(/balance/@debut,0,8)"/>
	<xsl:text>.</xsl:text>
      </xsl:when>
      <xsl:otherwise>
	<!-- Balance annuelle -->
	<xsl:text></xsl:text>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:variable>

<xsl:template match="balance">
  <xsl:text>Comptabilité </xsl:text>
  <xsl:value-of select="$societe/nom"/>
  <xsl:text> -- Balance du </xsl:text>
  <xsl:value-of select="@debut"/>
  <xsl:text> au </xsl:text>
  <xsl:value-of select="@fin"/>
  <xsl:text>
</xsl:text>
  <xsl:text>Les sommes sont portées en Euros. Le séparateur décimal est la virgule. Le fichier utilise le jeu de caractères 'Europe de l'Ouest' (ISO-8859-1).
</xsl:text>
  <xsl:text>Compte;Libellé;Report débit;Report crédit;Débit;Crédit;Solde Débit;Solde Crédit
</xsl:text>
<xsl:apply-templates />
</xsl:template>

<xsl:template match="compte">
  <xsl:value-of select="@numero"/>
  <xsl:text>;"</xsl:text>
  <xsl:apply-templates select="$plan_comptable">
    <xsl:with-param name="numero" select="@numero"/>
  </xsl:apply-templates>
  <xsl:text>";</xsl:text>
  <xsl:value-of select="format-number(@report-debit div 100,'###0,00')"/>
  <xsl:text>;</xsl:text>
  <xsl:value-of select="format-number(@report-credit div 100,'###0,00')"/>
  <xsl:text>;</xsl:text>
  <xsl:value-of select="format-number(@debit div 100,'###0,00')"/>
  <xsl:text>;</xsl:text>
  <xsl:value-of select="format-number(@credit div 100,'###0,00')"/>
  <xsl:text>;</xsl:text>
  <xsl:if test="@debit > @credit">
    <xsl:value-of select="format-number((@debit - @credit) div 100,'###0,00')"/>
  </xsl:if>
  <xsl:text>;</xsl:text>
  <xsl:if test="@credit > @debit">
    <xsl:value-of select="format-number((@credit - @debit) div 100,'###0,00')"/>
  </xsl:if>
</xsl:template>

</xsl:stylesheet>
