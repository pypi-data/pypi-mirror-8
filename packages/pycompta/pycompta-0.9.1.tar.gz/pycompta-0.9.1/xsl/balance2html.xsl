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

<!-- / ===================================================================== -->

<xsl:template match="balance">

<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<link rel="stylesheet" type="text/css" href="{$societe/html/css}" />
<script language="javascript" type="text/javascript" src="{$societe/html/mochikit}" />
<title>Comptabilité <xsl:value-of select="$societe/nom"/> -- Balance du <xsl:value-of select="@debut"/> au <xsl:value-of select="@fin"/></title>
</head>
<body>
<h1>Comptabilité <xsl:value-of select="$societe/nom"/> -- Balance du <xsl:value-of select="@debut"/> au <xsl:value-of select="@fin"/></h1>

<p style="font-size: small;"><a href="..">comptabilité</a> &gt;
 <a href="pilote.html">exercice</a> &gt;
 balance
</p>

<table width="100%" align="center" cellpadding="3" class="pycompta">
<thead>
<tr>
<th colspan="2" rowspan="2">Compte</th>
<th colspan="2">Report</th>
<th colspan="2">Période</th>
<th colspan="2">Solde</th>
</tr>

<tr>
<xsl:if test="( sum(compte/@debit) - sum(compte/@credit) ) != 0">
<xsl:attribute name="bgcolor">red</xsl:attribute>
</xsl:if>
<th>Débit</th>
<th>Crédit</th>
<th>Débit</th>
<th>Crédit</th>
<th>Débit</th>
<th>Crédit</th>
</tr>
</thead>
<tbody>
  <xsl:apply-templates select="compte">
     <xsl:sort select="@numero"/>
  </xsl:apply-templates>

<tr>
<xsl:if test="( sum(compte/@debit) - sum(compte/@credit) ) != 0">
<xsl:attribute name="bgcolor">red</xsl:attribute>
</xsl:if>
<td><b>TOTAUX</b></td>
<td>&#160;</td>

<td align="right"><b><xsl:call-template name="format-montant"><xsl:with-param name="montant"><xsl:value-of select="sum(compte[sum(@report-debit) &gt; sum(@report-credit)]/@report-debit) - sum(compte[sum(@report-debit) &gt; sum(@report-credit)]/@report-credit)"/></xsl:with-param></xsl:call-template></b></td>
<td align="right"><b><xsl:call-template name="format-montant"><xsl:with-param name="montant"><xsl:value-of select="sum(compte[sum(@report-credit) &gt; sum(@report-debit)]/@report-credit) - sum(compte[sum(@report-credit) &gt; sum(@report-debit)]/@report-debit)"/></xsl:with-param></xsl:call-template></b></td>

<td></td><td></td>
<!--
<td align="right"><b><xsl:call-template name="format-montant"><xsl:with-param name="montant"><xsl:value-of select="sum(compte[sum(@debit) &gt; sum(@credit)]/@debit) - sum(compte[sum(@debit) &gt; sum(@credit)]/@credit)"/></xsl:with-param></xsl:call-template></b></td>
<td align="right"><b><xsl:call-template name="format-montant"><xsl:with-param name="montant"><xsl:value-of select="sum(compte[sum(@credit) &gt; sum(@debit)]/@credit) - sum(compte[sum(@credit) &gt; sum(@debit)]/@debit)"/></xsl:with-param></xsl:call-template></b></td>
-->
<td align="right"><b><xsl:call-template name="format-montant"><xsl:with-param name="montant"><xsl:value-of select="sum(compte[sum(@debit) &gt; sum(@credit)]/@debit) - sum(compte[sum(@debit) &gt; sum(@credit)]/@credit)"/></xsl:with-param></xsl:call-template></b></td>
<td align="right"><b><xsl:call-template name="format-montant"><xsl:with-param name="montant"><xsl:value-of select="sum(compte[sum(@credit) &gt; sum(@debit)]/@credit) - sum(compte[sum(@credit) &gt; sum(@debit)]/@debit)"/></xsl:with-param></xsl:call-template></b></td>

</tr>
</tbody>
</table>

</body>
</html>
</xsl:template>

<!-- compte ============================================================== -->

<xsl:template match="compte">

<tr onmouseover="addElementClass(this, 'highlighted');" onmouseout="removeElementClass(this, 'highlighted')">
<xsl:attribute name="class"><xsl:choose>
<xsl:when test="position() mod 6 &lt; 3">rowlight</xsl:when>
<xsl:otherwise>rowdark</xsl:otherwise></xsl:choose></xsl:attribute>

<td><a><xsl:attribute name="href">grand-livre.<xsl:value-of select="$ext"/>html#compte<xsl:value-of select="@numero"/></xsl:attribute><xsl:value-of select="@numero"/></a></td>
<td><xsl:apply-templates select="$plan_comptable"><xsl:with-param name="numero" select="@numero"/></xsl:apply-templates></td>

<td align="right"><xsl:if test="@report-debit &gt; @report-credit"><xsl:call-template name="format-montant"><xsl:with-param name="montant"><xsl:value-of select="@report-debit - @report-credit"/></xsl:with-param></xsl:call-template></xsl:if></td>
<td align="right"><xsl:if test="@report-debit &lt; @report-credit"><xsl:call-template name="format-montant"><xsl:with-param name="montant"><xsl:value-of select="@report-credit - @report-debit"/></xsl:with-param></xsl:call-template></xsl:if></td>

<td align="right"><xsl:if test="@debit &gt; @report-debit"><xsl:call-template name="format-montant"><xsl:with-param name="montant"><xsl:value-of select="@debit - @report-debit"/></xsl:with-param></xsl:call-template></xsl:if></td>
<td align="right"><xsl:if test="@credit &gt; @report-credit"><xsl:call-template name="format-montant"><xsl:with-param name="montant"><xsl:value-of select="@credit - @report-credit"/></xsl:with-param></xsl:call-template></xsl:if></td>

<td align="right"><xsl:if test="@debit &gt; @credit"><xsl:call-template name="format-montant"><xsl:with-param name="montant"><xsl:value-of select="@debit - @credit"/></xsl:with-param></xsl:call-template></xsl:if></td>
<td align="right"><xsl:if test="@debit &lt; @credit"><xsl:call-template name="format-montant"><xsl:with-param name="montant"><xsl:value-of select="@credit - @debit"/></xsl:with-param></xsl:call-template></xsl:if></td>

</tr>
</xsl:template>

</xsl:stylesheet>