<?xml version="1.0" encoding="ISO-8859-1"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

  <xsl:import href="common.xslt"/>

  <xsl:output method="html" 
              version="4.0" 
              encoding="UTF-8" 
              indent="yes" 
              doctype-public="-//W3C//DTD HTML 4.0//EN"/>

  <xsl:param name="societe.def" select="'../xml/societe.xml'"/>
  <xsl:param name="setup.depodoc" select="'file:///var/lib/compta/'"/>

  <xsl:variable name="societe" select="document($societe.def)/societe"/>
  <xsl:variable name="plan_comptable" select="document($societe/plan-comptable/text())/plan-comptable"/>

<!-- / ===================================================================== -->

<xsl:template match="/">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<link rel="stylesheet" type="text/css" href="{$societe/style/css}" />
<title>Comptabilité <xsl:value-of select="$societe/nom"/> -- Etat facturation</title>
</head>
<body>
<h1>Comptabilité <xsl:value-of select="$societe/nom"/> -- Etat Facturation</h1>

<table border="1" cellpadding="5">
  <tr>
    <th>Numéro</th>
    <th>Etat</th>
    <th>Historique</th>
  </tr>
  <xsl:apply-templates select="facturation/facture">
     <xsl:sort select="@id" order="descending"/>
  </xsl:apply-templates>
</table>
</body>
</html>
</xsl:template>

<xsl:template match="facture">

<tr>
<td valign="top"><a><xsl:attribute name="href"><xsl:value-of select="$setup.depodoc"/><xsl:value-of select="@docid"/>.pdf</xsl:attribute><xsl:value-of select="@id"/></a></td>

<td valign="top">
<xsl:choose>
<xsl:when test="action[@type='paiement']">
Payée
</xsl:when>
<xsl:when test="action[@type='emission']">
<font color="navy">Emise</font>
</xsl:when>
<xsl:otherwise>
???
</xsl:otherwise>
</xsl:choose>
</td>

<td><ul>
<xsl:for-each select="action">
<li><xsl:value-of select="@type"/> le <xsl:value-of select="@date"/></li>
</xsl:for-each>
</ul>
</td>

</tr>

</xsl:template>

</xsl:stylesheet>