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
      <xsl:when test="substring(/grand-livre/@debut,0,8) = substring(/grand-livre/@fin,0,8)">
	<!-- Grand Livre mensuel -->
	<xsl:value-of select="substring(/grand-livre/@debut,0,8)"/>
	<xsl:text>.</xsl:text>
      </xsl:when>
      <xsl:otherwise>
	<!-- Grand Livre annuel -->
	<xsl:text></xsl:text>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:variable>


<xsl:template match="grand-livre">
  <xsl:text>Comptabilit� </xsl:text>
  <xsl:value-of select="$societe/nom"/>
  <xsl:text> -- Grand Livre du </xsl:text>
  <xsl:value-of select="@debut"/>
  <xsl:text> au </xsl:text>
  <xsl:value-of select="@fin"/>
  <xsl:text>
</xsl:text>
  <xsl:text>Les sommes sont port�es en Euros. Le s�parateur d�cimal est la virgule. Le fichier utilise le jeu de caract�res 'Europe de l'Ouest' (ISO-8859-1).
</xsl:text>

  <xsl:apply-templates select="compte"/>

</xsl:template>


<!-- compte -->
<xsl:template match="compte">

  <xsl:text>

Compte </xsl:text>
  <xsl:value-of select="@num"/>
  <xsl:text>�- </xsl:text>
  <xsl:apply-templates select="$plan_comptable">
    <xsl:with-param name="numero" select="@num"/>
  </xsl:apply-templates>
  <xsl:text>

</xsl:text>

  <xsl:text>Date;Libell�;D�bit;Cr�dit
</xsl:text>

  <!-- Report -->
  <xsl:text>
</xsl:text>
  <xsl:choose>
    <xsl:when test="@report-debit &gt; @report-credit">
      <xsl:text>;"Report d�bit";</xsl:text>
      <xsl:value-of select="format-number(
			    (@report-debit - @report-credit) div 100,
			    '###0,00' )"/>
      <xsl:text>;
</xsl:text>
    </xsl:when>
    <xsl:when test="@report-debit = @report-credit">
      <xsl:text>;"Report �quilibr�";;
</xsl:text>
    </xsl:when>
    <xsl:otherwise>
      <xsl:text>;"Report cr�dit";;</xsl:text>
      <xsl:value-of select="format-number(
			    (@report-credit - @report-debit) div 100,
			    '###0,00' )"/>
      <xsl:text>
</xsl:text>
    </xsl:otherwise>
  </xsl:choose>

  <xsl:text>
</xsl:text>

  <!-- �critures de d�bit et cr�dit -->
  <xsl:apply-templates select="debit|credit"/>

  <!-- Total compte -->
  <xsl:text>
</xsl:text>
  <xsl:choose>
    <xsl:when test="@debit &gt; @credit">
      <xsl:text>;"COMPTE D�BITEUR";</xsl:text>
      <xsl:value-of select="format-number(
			    (@debit - @credit) div 100,
			    '###0,00' )"/>
      <xsl:text>;
</xsl:text>
    </xsl:when>
    <xsl:when test="@debit = @credit">
      <xsl:text>;"COMPTE �QUILIBR�";;
</xsl:text>
    </xsl:when>
    <xsl:otherwise>
      <xsl:text>;"COMPTE CR�DITEUR";;</xsl:text>
      <xsl:value-of select="format-number(
			    (@credit - @debit) div 100,
			    '###0,00' )"/>
      <xsl:text>
</xsl:text>
    </xsl:otherwise>
  </xsl:choose>

</xsl:template>


<!-- ligne d�bit ou cr�dit -->
<xsl:template match="debit | credit">

  <xsl:value-of select="@date"/>
  <xsl:text>;</xsl:text>
  <xsl:text>"</xsl:text>
  <xsl:value-of select="translate(text(),'&quot;',&quot;'&quot;)"/>
  <xsl:text>";</xsl:text>
  <xsl:if test="self::credit">
    <xsl:text>;</xsl:text>
  </xsl:if>
  <xsl:value-of select="format-number(@montant div 100,'###0,00')"/>
  <xsl:if test="self::debit">
    <xsl:text>;</xsl:text>
  </xsl:if>
  <xsl:text>
</xsl:text>

</xsl:template>

</xsl:stylesheet>
