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

<xsl:template match="/">

<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<link rel="stylesheet" type="text/css" href="{$societe/html/css}" />
<script language="javascript" type="text/javascript" src="{$societe/html/mochikit}" />

<title>Comptabilité <xsl:value-of select="$societe/nom"/> -- Trésorerie</title>
</head>
<body>
<h1>Comptabilité <xsl:value-of select="$societe/nom"/> -- Trésorerie</h1>

      <p style="font-size: small;"><a href="..">comptabilité</a> &gt;
        <a href="pilote.html">exercice</a> &gt;
        trésorerie
      </p>

<table border="0" width="100%" align="center" cellpadding="3">


<tr>
  <td></td>
  <td align="center"><b>Liquide - dettes = <xsl:call-template name="format-montant"><xsl:with-param name="montant"><xsl:value-of select="sum(tresorerie/liquide/@montant) - sum(tresorerie/dette/@montant)"/></xsl:with-param></xsl:call-template></b></td>
  <td></td>
</tr>

<tr>
  <td valign="top"><table border="0" width="100%" cellpadding="3">

  <tr>
    <th>Creance</th>
    <th align="right"><xsl:call-template name="format-montant"><xsl:with-param name="montant"><xsl:value-of select="sum(tresorerie/creance/@montant)"/></xsl:with-param></xsl:call-template></th>
  </tr>

<xsl:for-each select="tresorerie/creance">
  <tr>
    <td><xsl:value-of select="@nom"/></td>
    <td align="right"><xsl:call-template name="format-montant"><xsl:with-param name="montant"><xsl:value-of select="@montant"/></xsl:with-param></xsl:call-template></td>
  </tr>
</xsl:for-each>

  </table></td>

  <td valign="top"><table border="0" width="100%" cellpadding="3">
  <tr>
    <th>Liquide</th>
    <th align="right"><xsl:call-template name="format-montant"><xsl:with-param name="montant"><xsl:value-of select="sum(tresorerie/liquide/@montant)"/></xsl:with-param></xsl:call-template></th>
  </tr>

<xsl:for-each select="tresorerie/liquide">
  <tr>
    <td><xsl:value-of select="@nom"/></td>
    <td align="right"><xsl:call-template name="format-montant"><xsl:with-param name="montant"><xsl:value-of select="@montant"/></xsl:with-param></xsl:call-template></td>
  </tr>
</xsl:for-each>

  </table></td>
  <td valign="top"><table border="0" width="100%" cellpadding="3">

  <tr>
    <th>Dettes</th>
    <th align="right"><xsl:call-template name="format-montant"><xsl:with-param name="montant"><xsl:value-of select="sum(tresorerie/dette/@montant)"/></xsl:with-param></xsl:call-template></th>
  </tr>

<xsl:for-each select="tresorerie/dette">
  <tr>
    <td><xsl:value-of select="@nom"/></td>
    <td align="right"><xsl:call-template name="format-montant"><xsl:with-param name="montant"><xsl:value-of select="@montant"/></xsl:with-param></xsl:call-template></td>
  </tr>
</xsl:for-each>

  </table></td>
</tr>

</table>

</body>
</html>
</xsl:template>

</xsl:stylesheet>