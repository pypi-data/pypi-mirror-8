<?xml version="1.0" encoding="ISO-8859-1"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

  <xsl:import href="common.xslt"/>

  <xsl:output method="html" 
              version="4.0" 
              encoding="UTF-8" 
              indent="yes" 
              doctype-public="-//W3C//DTD HTML 4.0//EN"/>

  <xsl:param name="societe.def" select="'../xml/societe.xml'"/>

  <xsl:variable name="societe" select="document($societe.def)/societe"/>
  <xsl:variable name="plan_comptable" select="document($societe/plan-comptable/text())/plan-comptable"/>

<!-- / ===================================================================== -->

  <xsl:variable name="ext">
    <xsl:choose>
      <xsl:when test="substring(/immo-amort/@debut,0,8) = substring(/immo-amort/@fin,0,8)">
	<!-- Immobilisations Amortissements mensuels -->
	<xsl:value-of select="substring(/immo-amort/@debut,0,8)"/>
	<xsl:text>.</xsl:text>
      </xsl:when>
      <xsl:otherwise>
	<!-- Immobilisations Amortissements annuels -->
	<xsl:text></xsl:text>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:variable>

<xsl:template match="immo-amort">

<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<link rel="stylesheet" type="text/css" href="{$societe/html/css}" />
<script language="javascript" type="text/javascript" src="{$societe/html/mochikit}" />

<title>Comptabilité <xsl:value-of select="$societe/nom"/> -- Immobilisations <!--du <xsl:value-of select="@debut"/> -->
au <xsl:value-of select="@fin"/></title>
</head>
<body>
  <h1>Comptabilité <xsl:value-of select="$societe/nom"/> -- Immobilisations <!-- du <xsl:value-of select="@debut"/> -->
au <xsl:value-of select="@fin"/></h1>

      <p style="font-size: small;"><a href="..">comptabilité</a> &gt;
        <a href="pilote.html">exercice</a> &gt;
        immobilisations
      </p>

<table width="100%" align="center" cellpadding="3" class="pycompta">
<tr>
  <th>Entrée</th>
  <th>Sortie</th>
  <th>Compte</th>
  <th>Libellé</th>
  <th>Brut</th>
  <th>Amort.</th>
  <th>Net</th>
</tr>

  <xsl:apply-templates select="immo">
     <xsl:sort select="@entree" order="descending"/>
  </xsl:apply-templates>

<tr>
<td colspan="7">&#160;</td>
</tr>
<tr>
<td colspan="3">&#160;</td>
<td><b>TOTAUX</b></td>

<td align="right"><b><xsl:call-template name="format-montant"><xsl:with-param name="montant"><xsl:value-of select="@montant-brut"/></xsl:with-param></xsl:call-template></b></td>
<td align="right"><b><xsl:call-template name="format-montant"><xsl:with-param name="montant"><xsl:value-of select="@montant-amort"/></xsl:with-param></xsl:call-template></b></td>
<td align="right"><b><xsl:call-template name="format-montant"><xsl:with-param name="montant"><xsl:value-of select="@montant-net"/></xsl:with-param></xsl:call-template></b></td>

</tr>

</table>

</body>
</html>
</xsl:template>

<!-- immo ============================================================== -->

<xsl:template match="immo">

<tr onmouseover="addElementClass(this, 'highlighted');" onmouseout="removeElementClass(this, 'highlighted')">
  <xsl:attribute name="class"><xsl:choose>
  <xsl:when test="position() mod 6 &lt; 3">rowlight</xsl:when>
  <xsl:otherwise>rowdark</xsl:otherwise></xsl:choose></xsl:attribute>

  <td align="center"><xsl:value-of select="@entree"/></td>
  <td align="center"><xsl:value-of select="@sortie"/></td>

  <td><a><xsl:attribute name="href">grand-livre.<xsl:value-of select="$ext"/>html#compte<xsl:value-of select="@compte"/></xsl:attribute><xsl:value-of select="@compte"/></a></td>

  <td><xsl:value-of select="."/></td>

  <td align="right"><xsl:call-template name="format-montant"><xsl:with-param name="montant"><xsl:value-of select="@montant-brut"/></xsl:with-param></xsl:call-template></td>

  <td align="right"><xsl:call-template name="format-montant"><xsl:with-param name="montant"><xsl:value-of select="@montant-amort"/></xsl:with-param></xsl:call-template></td>

  <td align="right"><xsl:call-template name="format-montant"><xsl:with-param name="montant"><xsl:value-of select="@montant-net"/></xsl:with-param></xsl:call-template></td>

</tr>
</xsl:template>

</xsl:stylesheet>
