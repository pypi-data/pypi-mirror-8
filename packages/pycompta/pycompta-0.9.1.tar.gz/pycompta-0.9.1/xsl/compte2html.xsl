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

<xsl:variable name="ext"><xsl:value-of select="substring(compte/@debut,0,8)"/></xsl:variable>

<xsl:template match="compte">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<link rel="stylesheet" type="text/css" href="{$societe/html/css}" />
<script language="javascript" type="text/javascript" src="{$societe/html/mochikit}" />

<title>Comptabilité <xsl:value-of select="$societe/nom"/> -- Historique du compte <xsl:value-of select="@numero"/> du <xsl:value-of select="@debut"/> au <xsl:value-of select="@fin"/></title>
</head>
<body>
<h1>Comptabilité <xsl:value-of select="$societe/nom"/> -- Historique du compte <xsl:value-of select="@numero"/> du <xsl:value-of select="@debut"/> au <xsl:value-of select="@fin"/></h1>

      <p style="font-size: small;"><a href="..">comptabilité</a> &gt;
        <a href="pilote.html">exercice</a> &gt;
        historique du compte <xsl:value-of select="@numero"/>
      </p>

<table align="center" width="100%" class="pycompta">
  <tr>
    <th>Date</th>
    <th width="50%">Libellé</th>
    <th>Réglement</th>
    <th>Débit</th>
    <th>Crédit</th>
    <th>Solde</th>
  </tr>
  <xsl:apply-templates select="mouvement"/>

</table>
</body>
</html>
</xsl:template>

<!-- ecriture ============================================================== -->

<xsl:template match="mouvement">

<tr onmouseover="addElementClass(this, 'highlighted');" onmouseout="removeElementClass(this, 'highlighted')">
<xsl:attribute name="class"><xsl:choose>
<xsl:when test="position() mod 6 &lt; 3">rowlight</xsl:when>
<xsl:otherwise>rowdark</xsl:otherwise></xsl:choose></xsl:attribute>

<td><xsl:value-of select="@date"/></td>
<td><em><xsl:value-of select="libelle"/></em></td>
<td><xsl:if test="reglement"><xsl:value-of select="reglement/@type"/> <xsl:value-of select="reglement"/><br /></xsl:if></td>
<td align="right"><xsl:call-template name="format-montant"><xsl:with-param name="montant"><xsl:value-of select="@debit"/></xsl:with-param></xsl:call-template></td>
<td align="right"><xsl:call-template name="format-montant"><xsl:with-param name="montant"><xsl:value-of select="@credit"/></xsl:with-param></xsl:call-template></td>
<td align="right"><xsl:call-template name="format-montant"><xsl:with-param name="montant"><xsl:value-of select="@solde"/></xsl:with-param></xsl:call-template></td>
</tr>
</xsl:template>

<!-- references ======================================================== 

<xsl:template match="ref[@type='doc']">
  <a><xsl:attribute name="href">file:///home/logilab/prive/depodoc/<xsl:value-of select="@id"/>.pdf</xsl:attribute><xsl:value-of select="."/></a> ;
</xsl:template>

<xsl:template match="ref[@type='personne']">
  <a><xsl:attribute name="href">file:///home/logilab/prive/clients/personnes/<xsl:value-of select="@id"/>.html</xsl:attribute><xsl:value-of select="."/></a> ;
</xsl:template>

<xsl:template match="ref[@type='societe']">
  <a><xsl:attribute name="href">file:///home/logilab/prive/clients/societes/<xsl:value-of select="@id"/>.html</xsl:attribute><xsl:value-of select="."/></a> ;
</xsl:template>

<xsl:template match="ref[@type='affaire']">
  <a><xsl:attribute name="href">file:///home/logilab/prive/clients/affaires/<xsl:value-of select="@id"/>.html</xsl:attribute><xsl:value-of select="."/></a> ;
</xsl:template>
-->

</xsl:stylesheet>