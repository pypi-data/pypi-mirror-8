<?xml version="1.0" encoding="ISO-8859-1"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">


  <xsl:import href="common.xslt"/>

  <xsl:output method="html" 
              version="4.0" 
              encoding="UTF-8" 
              indent="yes" 
              doctype-public="-//W3C//DTD HTML 4.0//EN"/>

  <!-- Passer en paramètre à cette feuille de style le numéro comptable
       du compte de banque pour lequel on fabrique le journal -->
  <xsl:param name="num.compte.banque" select="'51211'"/>

  <xsl:param name="societe.def" select="'../xml/societe.xml'"/>

  <xsl:variable name="societe" select="document($societe.def)/societe"/>
  <xsl:variable name="plan_comptable" select="document($societe/plan-comptable/text())/plan-comptable"/>

<!-- / ===================================================================== -->

<xsl:template match="journal">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<link rel="stylesheet" type="text/css" href="{$societe/html/css}" />
<script language="javascript" type="text/javascript" src="{$societe/html/mochikit}" />

<title>Comptabilité <xsl:value-of select="$societe/nom"/> -- Journal de banque du compte <xsl:value-of select="$num.compte.banque"/> du <xsl:value-of select="@debut"/> au <xsl:value-of select="@fin"/></title>
</head>
<body>
<h1>Comptabilité <xsl:value-of select="$societe/nom"/> -- Journal de banque du compte <xsl:value-of select="$num.compte.banque"/> du <xsl:value-of select="@debut"/> au <xsl:value-of select="@fin"/></h1>

<p style="font-size: small;"><a href="..">comptabilité</a> &gt;
  <a href="pilote.html">exercice</a> &gt;
  journal de banque
</p>

<table border="0" align="center" width="100%">
  <tr>
<xsl:if test="@credit != @debit">
<xsl:attribute name="bgcolor">red</xsl:attribute>
</xsl:if>
    <th>Date</th>
    <th width="50%">Libellé</th>
    <th>Réglement</th>
    <th>Débit</th>
    <th>Crédit</th>
  </tr>
  <xsl:apply-templates select="ecriture">
     <xsl:sort select="@date" order="ascending"/> 
  </xsl:apply-templates>

<tr><td colspan="5"><hr /></td></tr>

<tr>
  <td></td>
  <td></td>
  <td><b>TOTAUX</b></td>
  <td align="right"><b>
    <xsl:call-template name="format-montant">
      <xsl:with-param name="montant"
		      select="sum(ecriture/debit [
                                       starts-with(@compte,$num.compte.banque)
				                 ]/@montant)"/>
    </xsl:call-template>
  </b></td>
  <td align="right"><b>
    <xsl:call-template name="format-montant">
      <xsl:with-param name="montant"
		      select="sum(ecriture/credit [
                                       starts-with(@compte,$num.compte.banque)
				                 ]/@montant)"/>
    </xsl:call-template>
  </b></td>
</tr>
</table>
</body>
</html>
</xsl:template>

<!-- ecriture ============================================================== -->

<xsl:template match="ecriture">

<!-- Détail debit/credit -->
<xsl:apply-templates select="debit[starts-with(@compte,$num.compte.banque)]"/>
<xsl:apply-templates select="credit[starts-with(@compte,$num.compte.banque)]"/>

</xsl:template>

<!-- ligne débit -->
<xsl:template match="debit">
<tr  onmouseover="addElementClass(this, 'highlighted');" onmouseout="removeElementClass(this, 'highlighted')">
  <td><xsl:value-of select="../@date"/></td>
  <td><i><xsl:value-of select="../libelle"/></i></td>
  <td>
    <xsl:if test="../reglement">
      <xsl:value-of select="../reglement/@type"/>
      <xsl:text> </xsl:text>
      <xsl:value-of select="../reglement"/>
    </xsl:if>
  </td>
  <td align="right">
    <xsl:call-template name="format-montant">
      <xsl:with-param name="montant" select="@montant"/>
    </xsl:call-template>
  </td>
  <td>&#160;</td>
</tr>
</xsl:template>

<!-- ligne crédit -->
<xsl:template match="credit">
<tr  onmouseover="addElementClass(this, 'highlighted');" onmouseout="removeElementClass(this, 'highlighted')">
  <td><xsl:value-of select="../@date"/></td>
  <td><i><xsl:value-of select="../libelle"/></i></td>
  <td>
    <xsl:if test="../reglement">
      <xsl:value-of select="../reglement/@type"/>
      <xsl:text> </xsl:text>
      <xsl:value-of select="../reglement"/>
    </xsl:if>
  </td>
  <td>&#160;</td>
  <td align="right">
    <xsl:call-template name="format-montant">
      <xsl:with-param name="montant" select="@montant"/>
    </xsl:call-template>
  </td>
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