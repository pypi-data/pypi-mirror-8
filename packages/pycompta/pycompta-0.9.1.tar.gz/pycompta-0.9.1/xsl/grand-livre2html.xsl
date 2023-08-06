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

<!-- / ===================================================================== -->

<xsl:template match="grand-livre">

<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<link rel="stylesheet" type="text/css" href="{$societe/html/css}" />
<script language="javascript" type="text/javascript" src="{$societe/html/mochikit}" />

<title>Comptabilité <xsl:value-of select="$societe/nom"/> -- Grand Livre du <xsl:value-of select="@debut"/> 
au <xsl:value-of select="@fin"/></title>
</head>
<body>
<h1>Comptabilité <xsl:value-of select="$societe/nom"/> -- Grand Livre du <xsl:value-of select="@debut"/> 
au <xsl:value-of select="@fin"/></h1>

<p style="font-size: small;"><a href="..">comptabilité</a> &gt;
 <a href="pilote.html">exercice</a> &gt;
 grand livre
</p>

  <p>Comptes
  <xsl:for-each select="compte">
     <xsl:sort select="@num"/>
<a><xsl:attribute name="href">#compte<xsl:value-of select="@num"/></xsl:attribute><xsl:attribute name="title"><xsl:apply-templates select="$plan_comptable"><xsl:with-param name="curr-compte" select="."/></xsl:apply-templates></xsl:attribute><xsl:value-of select="@num"/></a> -
  </xsl:for-each>
  </p>

  <xsl:apply-templates select="compte">
     <xsl:sort select="@num"/>
  </xsl:apply-templates>

<hr />

<table border="0" width="100%">
<tr>
<td align="left"><b><xsl:call-template name="format-montant"><xsl:with-param name="montant"><xsl:value-of select="@debit"/></xsl:with-param></xsl:call-template></b></td>
<th><b>TOTAUX</b></th>
<td align="right"><b><xsl:call-template name="format-montant"><xsl:with-param name="montant"><xsl:value-of select="@credit"/></xsl:with-param></xsl:call-template></b></td>
</tr>
</table>

</body>
</html>
</xsl:template>

<!-- compte ============================================================== -->

<xsl:template match="compte">

<hr />

<a><xsl:attribute name="name">compte<xsl:value-of select="@num"/></xsl:attribute></a>

<h2>Compte <xsl:value-of select="@num"/> - <xsl:apply-templates select="$plan_comptable"><xsl:with-param name="curr-compte" select="."/></xsl:apply-templates></h2>

<table border="0" width="100%" align="center">

<!-- report -->
<tr>
  <td colspan="2">
    <xsl:choose>
      <xsl:when test="@report-debit &gt; @report-credit">
	<xsl:attribute name="align">left</xsl:attribute>
	<b>
	  <xsl:text>Report débit </xsl:text>
	  <xsl:call-template name="format-montant">
	    <xsl:with-param name="montant" 
			    select="@report-debit - @report-credit"/>
	  </xsl:call-template>
	</b>
      </xsl:when>
      <xsl:when test="@report-debit = @report-credit">
	<xsl:attribute name="align">center</xsl:attribute>
	<b>Report équilibre</b>
      </xsl:when>
      <xsl:otherwise>
	<xsl:attribute name="align">right</xsl:attribute>
	<b>
	  <xsl:text>Report crédit </xsl:text>
	  <xsl:call-template name="format-montant">
	    <xsl:with-param name="montant"
			    select="@report-credit - @report-debit"/>
	  </xsl:call-template>
	</b>
      </xsl:otherwise>
    </xsl:choose>
  </td>
</tr>

<!-- écritures de débit et crédit -->
<xsl:if test="debit or credit">
<tr>

<!-- débits -->
<td valign="top" width="50%">

<xsl:if test="debit">
  <table border="0" align="center" width="100%" cellpadding="2">
    <tr>
      <th width="15%">Date</th>
      <th width="70%">Libellé</th>
      <th width="15%">Débit</th>
    </tr>

    <xsl:apply-templates select="debit">
      <xsl:sort select="@date"/>
    </xsl:apply-templates>
  </table>
</xsl:if>

</td>

<!-- crédits -->
<td valign="top" width="50%">

<xsl:if test="credit">
  <table border="0" align="center" width="100%" cellpadding="2">
    <tr>
      <th width="15%">Date</th>
      <th width="70%">Libellé</th>
      <th width="15%">Crédit</th>
    </tr>

    <xsl:apply-templates select="credit">
      <xsl:sort select="@date"/>
    </xsl:apply-templates>
  </table>
</xsl:if>

</td>

</tr>
</xsl:if>

<!-- totaux -->
<tr>

<!-- débits -->
<td valign="top" width="50%">
<table border="0" align="center" width="100%" cellpadding="2">
  <tr>
    <td width="15%"></td>
    <td width="70%"><i>Total Débits</i></td>
    <td width="15%" align="right"><i>
      <xsl:call-template name="format-montant">
	<xsl:with-param name="montant" 
			select="@var-debit"/>
      </xsl:call-template>
    </i></td>
  </tr>
</table>
</td>

<!-- crédits -->
<td valign="top" width="50%">
<table border="0" align="center" width="100%" cellpadding="2">
  <tr>
    <td width="15%"></td>
    <td width="70%"><i>Total Crédits</i></td>
    <td width="15%" align="right"><i>
      <xsl:call-template name="format-montant">
	<xsl:with-param name="montant" 
			select="@var-credit"/>
      </xsl:call-template>
    </i></td>
  </tr>
</table>
</td>

</tr>

<!-- Total compte -->
<tr>
  <td colspan="2">
    <xsl:choose>
      <xsl:when test="@debit &gt; @credit">
	<xsl:attribute name="align">left</xsl:attribute>
	<b>
	  <xsl:text>COMPTE DÉBITEUR </xsl:text>
	  <xsl:call-template name="format-montant">
	    <xsl:with-param name="montant"
			    select="@debit - @credit"/>
	  </xsl:call-template>
	</b>
      </xsl:when>
      <xsl:when test="@debit = @credit">
	<xsl:attribute name="align">center</xsl:attribute>
	<b>COMPTE ÉQUILIBRÉ</b>
      </xsl:when>
      <xsl:otherwise>
	<xsl:attribute name="align">right</xsl:attribute>
	<b>
	  <xsl:text>COMPTE CRÉDITEUR </xsl:text>
	  <xsl:call-template name="format-montant">
	    <xsl:with-param name="montant"
			    select="@credit - @debit"/>
	</xsl:call-template>
	</b>
      </xsl:otherwise>
    </xsl:choose>
  </td>
</tr>

</table>

</xsl:template>

<!-- ligne débit ou crédit -->
<xsl:template match="debit | credit">
<tr valign="top" onmouseover="addElementClass(this, 'highlighted');" onmouseout="removeElementClass(this, 'highlighted')">
<td><a><xsl:attribute name="href">journal.<xsl:value-of select="$ext"/>html#<xsl:value-of select="@e_num"/></xsl:attribute><xsl:value-of select="@date"/></a></td>
<td><xsl:value-of select="text()"/></td>
<td align="right"><xsl:call-template name="format-montant"><xsl:with-param name="montant"><xsl:value-of select="@montant"/></xsl:with-param></xsl:call-template></td>
</tr>
</xsl:template>

<xsl:template match="plan-comptable">
  <xsl:param name="curr-compte"/>
  <xsl:value-of select="key('numero_comptes', $curr-compte/@num)/@nom"/>
</xsl:template>

</xsl:stylesheet>