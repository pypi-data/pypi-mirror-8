<?xml version="1.0" encoding="ISO-8859-1"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
                xmlns:p="http://pilote.data"
                exclude-result-prefixes="p">

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

<p:calendrier>
<p:mois num="1" nom="Janvier"/>
<p:mois num="2" nom="Février"/>
<p:mois num="3" nom="Mars"/>
<p:mois num="4" nom="Avril"/>
<p:mois num="5" nom="Mai"/>
<p:mois num="6" nom="Juin"/>
<p:mois num="7" nom="Juillet"/>
<p:mois num="8" nom="Août"/>
<p:mois num="9" nom="Septembre"/>
<p:mois num="10" nom="Octobre"/>
<p:mois num="11" nom="Novembre"/>
<p:mois num="12" nom="Décembre"/>
</p:calendrier>

<xsl:variable name="calendrier" select="document('')/*/p:calendrier"/>

<xsl:template match="/">

<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
    <link rel="stylesheet" type="text/css" href="{$societe/html/css}" />
    <script language="javascript" type="text/javascript" src="{$societe/html/mochikit}" />
    <title>Comptabilité <xsl:value-of select="$societe/nom"/></title>
  </head>
<body>
<h1>Comptabilité <xsl:value-of select="$societe/nom"/></h1>

<p style="font-size: small;"><a href="..">comptabilité</a> &gt;
   exercice
</p>
<!--
<p>Etat
<a href="facturation.html">facturation</a> qui remplacera celui qui est <a href="../factures/factures.html">maintenu à la main</a></p>
-->

<xsl:if test="pilote/previsions/mensualite">
<h2>Prévisions</h2>

<table align="center" cellpadding="5" class="pycompta">
    <tr>
    <th></th>
    <th><a href="journal.prev.html">Journal</a></th>
    <th><a href="grand-livre.prev.html">Grand Livre</a></th>
    <th><a href="balance.prev.html">Balance</a></th>
    <th><a href="compte-resultat.prev.html">Résultat</a></th>
    <th><a href="bilan.prev.html">Bilan</a></th>
    <th><a href="bilan-immo.prev.html">Immobilisations</a> [<a href="immo-amort.prev.html">J</a>]</th>
    <th><a href="tresorerie.compte.prev.html">Tresorerie</a></th>
    <th><a href="produits.compte.prev.html">Produits</a></th>
    <th>Paye <a href="paye.journal.prev.html">J</a>-<a href="paye.grand-livre.prev.html">GL</a>-<a href="paye.balance.prev.html">B</a></th>
    <th>Banque <a href="banque.journal.prev.html">J</a>-<a href="banque.glivre.prev.html">GL</a></th>
    </tr>

  <xsl:apply-templates select="pilote/previsions/mensualite" mode="prev"/>

</table>

</xsl:if>

<h2>Documents comptables</h2>

<p />

<table align="center" cellpadding="5" class="pycompta">
    <tr>
    <th>Exercice complet</th>
    <th><a href="journal.html">Journal</a></th>
    <th><a href="grand-livre.html">Grand Livre</a></th>
    <th><a href="balance.html">Balance</a></th>
    <th><a href="compte-resultat.html">Résultat</a></th>
    <th><a href="bilan.html">Bilan</a></th>
    <th><a href="bilan-immo.html">Immobilisations</a> [<a href="immo-amort.html">J</a>]</th>
    <th><a href="tresorerie.compte.html">Tresorerie</a></th>
    <th><a href="produits.compte.html">Produits</a></th>
    <th>Paye <a href="paye.journal.html">J</a>-<a href="paye.grand-livre.html">GL</a>-<a href="paye.balance.html">B</a></th>
    <th>Banque <a href="banque.journal.html">J</a>-<a href="banque.glivre.html">GL</a></th>
    <!--
    <th><a href="facturation.html">Facturation</a></th>
    -->
    </tr>

  <xsl:apply-templates select="pilote/recapitulatif/mensualite"/>

</table>

<p><a href="plan-comptable.html">Plan Comptable</a></p>

<p>Trésorerie : <xsl:apply-templates select="pilote/tresorerie/compte"/> </p>

<h2>Graphiques</h2>

<!--
<p align="center"><img border="1" src="comptes.png"/></p>
<p align="center"><img border="1" src="tresorerie.png"/></p>
-->
<iframe src="diagram.html" width="550" height="450" />
<iframe src="diagram_treso.html" width="550" height="450" />

</body>
</html>

</xsl:template>

<xsl:template match="mensualite" mode="prev">

    <tr>
      <xsl:attribute name="class"><xsl:choose>
      <xsl:when test="position() mod 2 = 0">rowlight</xsl:when>
      <xsl:otherwise>rowdark</xsl:otherwise></xsl:choose></xsl:attribute>


    <td><xsl:value-of select="@annee"/><xsl:text> </xsl:text> <xsl:value-of select="$calendrier/p:mois[@num=current()/@mois]/@nom"/></td>

    <td><a><xsl:attribute name="href">journal.<xsl:value-of select="@annee"/>-<xsl:if test="@mois &lt; 10">0</xsl:if><xsl:value-of select="@mois"/>.prev.html</xsl:attribute>Journal</a></td>

    <td><a><xsl:attribute name="href">grand-livre.<xsl:value-of select="@annee"/>-<xsl:if test="@mois &lt; 10">0</xsl:if><xsl:value-of select="@mois"/>.prev.html</xsl:attribute>Grand Livre</a></td>

    <td><xsl:if test="@balance != 'True'">
<xsl:attribute name="bgcolor">black</xsl:attribute>
</xsl:if>
<a><xsl:attribute name="href">balance.<xsl:value-of select="@annee"/>-<xsl:if test="@mois &lt; 10">0</xsl:if><xsl:value-of select="@mois"/>.prev.html</xsl:attribute>Balance</a></td>

    <td align='right'><a><xsl:attribute name="href">compte-resultat.<xsl:value-of select="@annee"/>-<xsl:if test="@mois &lt; 10">0</xsl:if><xsl:value-of select="@mois"/>.prev.html</xsl:attribute><xsl:call-template name="format-montant"><xsl:with-param name="montant"><xsl:value-of select="@compte-resultat-produits - @compte-resultat-charges"/></xsl:with-param></xsl:call-template></a></td>


   <td align='right'>
<xsl:if test="@bilan-actif != @bilan-passif">
<xsl:attribute name="bgcolor">black</xsl:attribute>
</xsl:if>
<a><xsl:attribute name="href">bilan.<xsl:value-of select="@annee"/>-<xsl:if test="@mois &lt; 10">0</xsl:if><xsl:value-of select="@mois"/>.prev.html</xsl:attribute><xsl:call-template name="format-montant"><xsl:with-param name="montant"><xsl:value-of select="@bilan-actif"/></xsl:with-param></xsl:call-template></a></td>

   <td align='right'><a><xsl:attribute name="href">bilan-immo.<xsl:value-of select="@annee"/>-<xsl:if test="@mois &lt; 10">0</xsl:if><xsl:value-of select="@mois"/>.prev.html</xsl:attribute><xsl:call-template name="format-montant"><xsl:with-param name="montant"><xsl:value-of select="@immobilisations"/></xsl:with-param></xsl:call-template></a> - <a><xsl:attribute name="href">immo-amort.<xsl:value-of select="@annee"/>-<xsl:if test="@mois &lt; 10">0</xsl:if><xsl:value-of select="@mois"/>.prev.html</xsl:attribute>J</a></td>

   <td align='right'><a><xsl:attribute name="href">tresorerie.compte.<xsl:value-of select="@annee"/>-<xsl:if test="@mois &lt; 10">0</xsl:if><xsl:value-of select="@mois"/>.prev.html</xsl:attribute><xsl:call-template name="format-montant"><xsl:with-param name="montant"><xsl:value-of select="@tresorerie"/></xsl:with-param></xsl:call-template></a></td>

   <td align='right'><a><xsl:attribute name="href">produits.compte.<xsl:value-of select="@annee"/>-<xsl:if test="@mois &lt; 10">0</xsl:if><xsl:value-of select="@mois"/>.prev.html</xsl:attribute><xsl:call-template name="format-montant"><xsl:with-param name="montant"><xsl:value-of select="@produits"/></xsl:with-param></xsl:call-template></a></td>

    <td><a><xsl:attribute name="href">paye.journal.<xsl:value-of select="@annee"/>-<xsl:if test="@mois &lt; 10">0</xsl:if><xsl:value-of select="@mois"/>.prev.html</xsl:attribute>J</a>
-
    <a><xsl:attribute name="href">paye.grand-livre.<xsl:value-of select="@annee"/>-<xsl:if test="@mois &lt; 10">0</xsl:if><xsl:value-of select="@mois"/>.prev.html</xsl:attribute>GL</a>
-
    <a><xsl:attribute name="href">paye.balance.<xsl:value-of select="@annee"/>-<xsl:if test="@mois &lt; 10">0</xsl:if><xsl:value-of select="@mois"/>.prev.html</xsl:attribute>B</a></td>
   <!--
   <td align='right'><a><xsl:attribute name="href">tresorerie.prev.<xsl:value-of select="@annee"/>-<xsl:if test="@mois &lt; 10">0</xsl:if><xsl:value-of select="@mois"/>.html</xsl:attribute><xsl:value-of select="@tresorerie"/></a></td>
-->
    <td align='center'><a><xsl:attribute name="href">banque.journal.<xsl:value-of select="@annee"/>-<xsl:if test="@mois &lt; 10">0</xsl:if><xsl:value-of select="@mois"/>.prev.html</xsl:attribute>J</a>
-
    <a><xsl:attribute name="href">banque.glivre.<xsl:value-of select="@annee"/>-<xsl:if test="@mois &lt; 10">0</xsl:if><xsl:value-of select="@mois"/>.prev.html</xsl:attribute>GL</a></td>
    </tr>
</xsl:template>

<xsl:template match="mensualite">

    <tr>
      <xsl:attribute name="class"><xsl:choose>
      <xsl:when test="position() mod 2 = 0">rowlight</xsl:when>
      <xsl:otherwise>rowdark</xsl:otherwise></xsl:choose></xsl:attribute>

    <td><xsl:value-of select="@annee"/><xsl:text> </xsl:text> <xsl:value-of select="document('')/*/p:calendrier/p:mois[@num=current()/@mois]/@nom"/></td>

    <td><a><xsl:attribute name="href">journal.<xsl:value-of select="@annee"/>-<xsl:if test="@mois &lt; 10">0</xsl:if><xsl:value-of select="@mois"/>.html</xsl:attribute>Journal</a></td>

    <td><a><xsl:attribute name="href">grand-livre.<xsl:value-of select="@annee"/>-<xsl:if test="@mois &lt; 10">0</xsl:if><xsl:value-of select="@mois"/>.html</xsl:attribute>Grand Livre</a></td>

    <td align='right'>
<xsl:if test="@balance != 'True'">
<xsl:attribute name="bgcolor">black</xsl:attribute>
</xsl:if>
<a><xsl:attribute name="href">balance.<xsl:value-of select="@annee"/>-<xsl:if test="@mois &lt; 10">0</xsl:if><xsl:value-of select="@mois"/>.html</xsl:attribute>Balance</a></td>

    <td align='right'><a><xsl:attribute name="href">compte-resultat.<xsl:value-of select="@annee"/>-<xsl:if test="@mois &lt; 10">0</xsl:if><xsl:value-of select="@mois"/>.html</xsl:attribute><xsl:call-template name="format-montant"><xsl:with-param name="montant"><xsl:value-of select="@compte-resultat-produits - @compte-resultat-charges"/></xsl:with-param></xsl:call-template></a></td>

   <td align='right'>
<xsl:if test="@bilan-actif != @bilan-passif">
<xsl:attribute name="bgcolor">black</xsl:attribute>
</xsl:if>
<a><xsl:attribute name="href">bilan.<xsl:value-of select="@annee"/>-<xsl:if test="@mois &lt; 10">0</xsl:if><xsl:value-of select="@mois"/>.html</xsl:attribute><xsl:call-template name="format-montant"><xsl:with-param name="montant"><xsl:value-of select="@bilan-actif"/></xsl:with-param></xsl:call-template></a></td>
<!--
   <td align='right'><a><xsl:attribute name="href">tresorerie.<xsl:value-of select="@annee"/>-<xsl:if test="@mois &lt; 10">0</xsl:if><xsl:value-of select="@mois"/>.html</xsl:attribute><xsl:value-of select="@tresorerie"/></a></td>
-->
   <td align='right'><a><xsl:attribute name="href">bilan-immo.<xsl:value-of select="@annee"/>-<xsl:if test="@mois &lt; 10">0</xsl:if><xsl:value-of select="@mois"/>.html</xsl:attribute><xsl:call-template name="format-montant"><xsl:with-param name="montant"><xsl:value-of select="@immobilisations"/></xsl:with-param></xsl:call-template></a> - <a><xsl:attribute name="href">immo-amort.<xsl:value-of select="@annee"/>-<xsl:if test="@mois &lt; 10">0</xsl:if><xsl:value-of select="@mois"/>.html</xsl:attribute>J</a></td>

   <td align='right'><a><xsl:attribute name="href">tresorerie.compte.<xsl:value-of select="@annee"/>-<xsl:if test="@mois &lt; 10">0</xsl:if><xsl:value-of select="@mois"/>.html</xsl:attribute><xsl:call-template name="format-montant"><xsl:with-param name="montant"><xsl:value-of select="@tresorerie"/></xsl:with-param></xsl:call-template></a></td>

   <td align='right'><a><xsl:attribute name="href">produits.compte.<xsl:value-of select="@annee"/>-<xsl:if test="@mois &lt; 10">0</xsl:if><xsl:value-of select="@mois"/>.html</xsl:attribute><xsl:call-template name="format-montant"><xsl:with-param name="montant"><xsl:value-of select="@produits"/></xsl:with-param></xsl:call-template></a></td>

    <td><a><xsl:attribute name="href">paye.journal.<xsl:value-of select="@annee"/>-<xsl:if test="@mois &lt; 10">0</xsl:if><xsl:value-of select="@mois"/>.html</xsl:attribute>J</a>
-
    <a><xsl:attribute name="href">paye.grand-livre.<xsl:value-of select="@annee"/>-<xsl:if test="@mois &lt; 10">0</xsl:if><xsl:value-of select="@mois"/>.html</xsl:attribute>GL</a>
-
    <a><xsl:attribute name="href">paye.balance.<xsl:value-of select="@annee"/>-<xsl:if test="@mois &lt; 10">0</xsl:if><xsl:value-of select="@mois"/>.html</xsl:attribute>B</a></td>

    <td align='center'><a><xsl:attribute name="href">banque.journal.<xsl:value-of select="@annee"/>-<xsl:if test="@mois &lt; 10">0</xsl:if><xsl:value-of select="@mois"/>.html</xsl:attribute>J</a>
-
    <a><xsl:attribute name="href">banque.glivre.<xsl:value-of select="@annee"/>-<xsl:if test="@mois &lt; 10">0</xsl:if><xsl:value-of select="@mois"/>.html</xsl:attribute>GL</a></td>
    </tr>
</xsl:template>

<xsl:template match="compte">

<a><xsl:attribute name="href">tresorerie.<xsl:value-of select="@num"/>.compte.prev.html</xsl:attribute><xsl:value-of select="@num"/></a>
<xsl:text> - </xsl:text>

</xsl:template>

</xsl:stylesheet>
