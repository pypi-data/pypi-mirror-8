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
      <xsl:when test="substring(/journal/@debut,0,8) = substring(/journal/@fin,0,8)">
	<!-- Journal mensuel -->
	<xsl:value-of select="substring(/journal/@debut,0,8)"/>
	<xsl:text>.</xsl:text>
      </xsl:when>
      <xsl:otherwise>
	<!-- Journal annuel -->
	<xsl:text></xsl:text>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:variable>

<xsl:template match="journal">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<link rel="stylesheet" type="text/css" href="{$societe/html/css}" />
<script language="javascript" type="text/javascript" src="{$societe/html/mochikit}" />

<title>Comptabilité <xsl:value-of select="$societe/nom"/> -- Journal du <xsl:value-of select="@debut"/> au <xsl:value-of select="@fin"/></title>
</head>
<body>
<h1>Comptabilité <xsl:value-of select="$societe/nom"/> -- Journal du <xsl:value-of select="@debut"/> au <xsl:value-of select="@fin"/></h1>

<p style="font-size: small;"><a href="..">comptabilité</a> &gt;
 <a href="pilote.html">exercice</a> &gt;
 journal
</p>

<table align="center" width="100%" class="pycompta">
<thead>
  <tr>
<xsl:if test="@credit != @debit">
<xsl:attribute name="bgcolor">red</xsl:attribute>
</xsl:if>
    <th>Date</th>
    <th>N° Compte</th>
    <th width="50%">Compte</th>
    <th>Débit</th>
    <th>Crédit</th>
  </tr>
</thead>

<tbody>
  <xsl:apply-templates select="ecriture">
     <xsl:sort select="@date" order="descending"/>
  </xsl:apply-templates>
</tbody>

<tfoot>
<tr><td colspan="2"> </td><td><b>TOTAUX</b></td>
<td align="right"><b><xsl:call-template name="format-montant"><xsl:with-param name="montant"><xsl:value-of select="@debit"/></xsl:with-param></xsl:call-template></b></td>
<td align="right"><b><xsl:call-template name="format-montant"><xsl:with-param name="montant"><xsl:value-of select="@credit"/></xsl:with-param></xsl:call-template></b></td>
</tr>
</tfoot>
</table>
</body>
</html>
</xsl:template>

<!-- ecriture ============================================================== -->

<xsl:template match="ecriture">

<xsl:variable name="rowcolor"><xsl:choose>
<xsl:when test="position() mod 2 = 0">rowlight</xsl:when>
<xsl:otherwise>rowdark</xsl:otherwise></xsl:choose></xsl:variable>

<!-- date écriture et ligne de séparation -->
<tr class="{$rowcolor}">

<xsl:if test="( sum(debit/@montant) - sum(credit/@montant) ) != 0">
<xsl:attribute name="bgcolor">red</xsl:attribute>
</xsl:if>
<td valign="top" align="center">
<a><xsl:attribute name="name"><xsl:value-of select="@e_num"/></xsl:attribute>
<xsl:value-of select="@date"/></a></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>

<!-- libellé 
<tr>
<td>&#160;</td>
<td colspan="2"><em><xsl:value-of select="@e_num"/> - <xsl:value-of select="libelle"/></em>
</td>
<td>&#160;</td>
<td>&#160;</td>
</tr>
-->

<!-- Détail debit/credit -->
<xsl:apply-templates select="debit"><xsl:with-param name="rowcolor" select="$rowcolor"/></xsl:apply-templates>
<xsl:apply-templates select="credit"><xsl:with-param name="rowcolor" select="$rowcolor"/></xsl:apply-templates>

<!-- Détail règlement -->
<!-- <xsl:if test="ref | reglement"> -->
<tr class="{$rowcolor}">
<td>&#160;</td>
<td>&#160;</td>
<td>
  <xsl:if test="ref">Cf <xsl:apply-templates select="ref"/> <br/></xsl:if>
  <xsl:if test="reglement">Réglement <xsl:value-of select="reglement/@type"/> <xsl:value-of select="reglement"/><br /></xsl:if>
  <em><xsl:value-of select="libelle"/></em>
</td>
<td>&#160;</td>
<td>&#160;</td>
</tr>
<!-- </xsl:if> -->

</xsl:template>

<!-- ligne débit -->
<xsl:template match="debit">
<xsl:param name="rowcolor" /> 
<tr class="{$rowcolor}">
<td>&#160;</td>
<td align="left">
<a><xsl:attribute name="href">grand-livre.<xsl:value-of select="$ext"/>html#compte<xsl:value-of select="@compte"/></xsl:attribute><xsl:value-of select="@compte"/></a>
</td>
<td><xsl:apply-templates select="$plan_comptable"><xsl:with-param name="numero" select="@compte"/></xsl:apply-templates></td>
<!-- <td align="right"><xsl:value-of select="lglb:format-montant(@montant)"/></td> -->
<td align="right"><xsl:call-template name="format-montant"><xsl:with-param name="montant"><xsl:value-of select="@montant"/></xsl:with-param></xsl:call-template></td>
<td>&#160;</td>
</tr>
</xsl:template>

<!-- ligne crédit -->
<xsl:template match="credit">
<xsl:param name="rowcolor" /> 
<tr class="{$rowcolor}">
<td>&#160;</td>
<td align="center">
<a><xsl:attribute name="href">grand-livre.<xsl:value-of select="$ext"/>html#compte<xsl:value-of select="@compte"/></xsl:attribute><xsl:value-of select="@compte"/></a>
</td>
<td>&#160;&#160;&#160;&#160;&#160;&#160;<xsl:apply-templates select="$plan_comptable"><xsl:with-param name="numero" select="@compte"/></xsl:apply-templates></td>
<td>&#160;</td>
<!-- <td align="right"><xsl:value-of select="lglb:format-montant(@montant)"/></td> -->
<td align="right"><xsl:call-template name="format-montant"><xsl:with-param name="montant"><xsl:value-of select="@montant"/></xsl:with-param></xsl:call-template></td>
</tr>
</xsl:template>

<!-- references ======================================================== -->

<xsl:template match="ref[@type='doc']">
  <a><xsl:attribute name="href">/prive/depodoc/<xsl:value-of select="@id"/>.pdf</xsl:attribute><xsl:value-of select="."/></a> ;
</xsl:template>

<xsl:template match="ref[@type='personne']">
  <a><xsl:attribute name="href">/crm/person/surname/<xsl:value-of select="@id"/></xsl:attribute><xsl:value-of select="."/></a> ;
</xsl:template>

<xsl:template match="ref[@type='societe']">
  <a><xsl:attribute name="href">/crm/company/name/<xsl:value-of select="@id"/></xsl:attribute><xsl:value-of select="."/></a> ;
</xsl:template>

<xsl:template match="ref[@type='affaire']">
  <a><xsl:attribute name="href">/crm/workcase/ref/<xsl:value-of select="@id"/></xsl:attribute><xsl:value-of select="."/></a> ;
</xsl:template>

</xsl:stylesheet>