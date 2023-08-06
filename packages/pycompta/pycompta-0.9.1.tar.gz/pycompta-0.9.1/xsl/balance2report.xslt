<?xml version="1.0" encoding="ISO-8859-1"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

  <xsl:output method="xml" encoding="ISO-8859-1" indent="yes" />

<xsl:template match="balance">

<xsl:variable name="comptes_bilan" select="compte[substring(@numero,1,1) != '6' and substring(@numero,1,1) != '7']" />
<xsl:variable name="comptes_resultat" select="compte[substring(@numero,1,1) = '6' or substring(@numero,1,1) = '7']" />

<xsl:variable name="resultat" select="sum($comptes_resultat/@credit) - sum($comptes_resultat/@debit)" />

<ecritures>
<ecriture>
  <libelle>Report exercice précédent</libelle>
  <xsl:apply-templates select="$comptes_bilan">
     <xsl:sort select="@numero"/>
  </xsl:apply-templates>

<xsl:if test="$resultat &gt; 0">
  <credit compte="11">
    <xsl:attribute name="montant"><xsl:value-of select="format-number( ($resultat div 100), '##0.00')" /></xsl:attribute>
  </credit>
</xsl:if>

<xsl:if test="$resultat &lt; 0">
  <debit compte="11">
    <xsl:attribute name="montant"><xsl:value-of select="format-number( -($resultat div 100), '##0.00')" /></xsl:attribute>
  </debit>
</xsl:if>

</ecriture>
</ecritures>

</xsl:template>

<xsl:template match="compte">

<xsl:if test="@debit &gt; @credit">
<debit>
<xsl:attribute name="compte"><xsl:value-of select="@numero"/></xsl:attribute>
<xsl:attribute name="montant"><xsl:value-of select="format-number(number((@debit - @credit) div 100),'##0.00')"/></xsl:attribute>
</debit>
</xsl:if>

<xsl:if test="@debit &lt; @credit">
<credit>
<xsl:attribute name="compte"><xsl:value-of select="@numero"/></xsl:attribute>
<xsl:attribute name="montant"><xsl:value-of select="format-number(number((@credit - @debit) div 100),'##0.00')"/></xsl:attribute>
</credit>
</xsl:if>

</xsl:template>

</xsl:stylesheet>
