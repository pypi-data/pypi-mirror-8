<?xml version="1.0" encoding="ISO-8859-1"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

<xsl:key name="numero_comptes" match="compte" use="@numero"/>
<xsl:decimal-format name="fr" decimal-separator="," grouping-separator=" " NaN="n/d"/>

<xsl:template match="plan-comptable">
  <xsl:param name="numero"/>
  <xsl:value-of select="key('numero_comptes', $numero)/@nom"/>
</xsl:template>

<xsl:template name="format-montant">
  <xsl:param name="montant">0</xsl:param> 
  <xsl:value-of select="format-number(number($montant div 100),'# ##0,00','fr')"/>
</xsl:template> 

</xsl:stylesheet>
