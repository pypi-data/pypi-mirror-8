<?xml version="1.0" encoding="ISO-8859-1"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

  <xsl:output method="html" 
              version="4.0" 
              encoding="UTF-8" 
              indent="yes" 
              doctype-public="-//W3C//DTD HTML 4.0//EN"/>

  <xsl:param name="societe.def" select="'../xml/societe.xml'"/>

  <xsl:variable name="societe" select="document($societe.def)/societe"/>

<!-- / ===================================================================== -->

<xsl:template match="/">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<link rel="stylesheet" type="text/css" href="{$societe/style/css}" />
<title>Comptabilit� <xsl:value-of select="$societe/nom"/> -- Plan Comptable</title>
</head>
<body>
<h1>Comptabilit� <xsl:value-of select="$societe/nom"/> -- Plan comptable</h1>

      <p style="font-size: small;"><a href="..">comptabilit�</a> &gt;
        <a href="pilote.html">exercice</a> &gt;
        plan comptable
      </p>

<center>
<table cellpadding="3" border="0">
<tr>
<th width="61%" colspan="5">Comptes de Bilan</th>
<th width="26%" colspan="2">Comptes de Gestion</th>
<th width="13%">Comptes&#160;Speciaux</th>
</tr>

<tr align="center" valign="top">
<td width="12%"><a href="#classe1">Classe 1</a><br /><br />
Comptes de capitaux</td>
<td width="12%"><a href="#classe2">Classe 2</a><br /><br />
Comptes d'immobilisations</td>
<td width="12%"><a href="#classe3">Classe 3</a><br /><br />
Comptes de stocks et en-cours</td>
<td width="12%"><a href="#classe4">Classe 4</a><br /><br />
Comptes de tiers</td>
<td width="12%"><a href="#classe5">Classe 5</a><br /><br />
Comptes financiers</td>
<td width="13%"><a href="#classe6">Classe 6</a><br /><br />
Comptes de charges</td>
<td width="13%"><a href="#classe7">Classe 7</a><br /><br />
Comptes de produits</td>
<td width="13%" rowspan="11"><a href="#classe8">Classe 8</a><br /><br />
Comptes qui n'ont pas leur place dans les classes 1 � 7</td>
</tr>

<tr valign="top">
<td><a href="#compte10">10</a>.&#160;Capital et r�serves</td>
<td><a href="#compte20">20</a>.&#160;Immobilisations incorporelles</td>
<td></td>
<td><a href="#compte40">40</a>.&#160;Fournisseurs et comptes rattach�s</td>
<td><a href="#compte50">50</a>.&#160;Valeurs mobili�res de placement</td>
<td><a href="#compte60">60</a>.&#160;Achats (sauf 603.&#160;Variation des stocks (approvisionnements et marchandises))</td>
<td><a href="#compte70">70</a>.&#160;Ventes de produits fabriqu�s, prestations de services,
marchandises</td>
</tr>

<tr valign="top">
<td><a href="#compte11">11</a>.&#160;Report � nouveau</td>
<td><a href="#compte21">21</a>.&#160;Immobilisations corporelles</td>
<td><a href="#compte31">31</a>.&#160;Mati�res premi�res (et fournitures)</td>
<td><a href="#compte41">41</a>.&#160;Clients et comptes rattach�s</td>
<td><a href="#compte51">51</a>.&#160;Banques, �tablissements financiers et assimil�s</td>
<td><a href="#compte61">61</a>.&#160;Services ext�rieurs</td>
<td><a href="#compte71">71</a>.&#160;Production stock�e (ou d�stockage).</td>
</tr>

<tr valign="top">
<td><a href="#compte12">12</a>.&#160;R�sultat de  l'exercice</td>
<td><a href="#compte22">22</a>.&#160;Immobilisations mises en concession</td>
<td><a href="#compte32">32</a>.&#160;Autres approvisionnements</td>
<td><a href="#compte42">42</a>.&#160;Personnel et  comptes rattach�s</td>
<td><a href="#compte52">52</a>.&#160;Instruments de Tr�sorerie</td>
<td><a href="#compte62">62</a>.&#160;Autres services  ext�rieurs</td>
<td><a href="#compte72">72</a>.&#160;Production immobilis�e</td>
</tr>

<tr valign="top">
<td><a href="#compte13">13</a>.&#160;Subventions d'investissement</td>
<td><a href="#compte23">23</a>.&#160;Immobilisations en cours</td>
<td><a href="#compte33">33</a>.&#160;En-cours de production de biens</td>
<td><a href="#compte43">43</a>.&#160;S�curit� sociale et autres organismes sociaux</td>
<td><a href="#compte53">53</a>.&#160;Caisse</td>
<td><a href="#compte63">63</a>.&#160;Imp�ts, taxes et  versements assimil�s</td>
<td><a href="#compte73">73</a>.&#160;Produits nets partiels sur op�rations � long terme</td>
</tr>

<tr valign="top">
<td><a href="#compte14">14</a>.&#160;Provisions r�glement�es</td>
<td></td>
<td><a href="#compte34">34</a>.&#160;En-cours de production de services</td>
<td><a href="#compte44">44</a>.&#160;Etat et autres collectivit�s publiques</td>
<td><a href="#compte54">54</a>.&#160;R�gies d'avances et accr�ditifs</td>
<td><a href="#compte64">64</a>.&#160;Charges de personnel</td>
<td><a href="#compte74">74</a>.&#160;Subventions d'exploitation</td>
</tr>

<tr valign="top">
<td><a href="#compte15">15</a>.&#160;Provisions pour risques et charges</td>
<td></td>
<td><a href="#compte35">35</a>.&#160;Stocks de produits</td>
<td><a href="#compte45">45</a>.&#160;Groupe et associ�s</td>
<td></td>
<td><a href="#compte65">65</a>.&#160;Autres charges de  gestion courante</td>
<td><a href="#compte75">75</a>.&#160;Autres produits de gestion courante</td>
</tr>

<tr valign="top">
<td><a href="#compte16">16</a>.&#160;Emprunts et dettes assimil�es</td>
<td><a href="#compte26">26</a>.&#160;Participations et cr�ances rattach�es �  des participations</td>
<td></td>
<td><a href="#compte46">46</a>.&#160;D�biteurs divers et cr�diteurs divers</td>
<td></td>
<td><a href="#compte66">66</a>.&#160;Charges financi�res</td>
<td><a href="#compte76">76</a>.&#160;Produits financiers</td>
</tr>

<tr valign="top">
<td><a href="#compte17">17</a>.&#160;Dettes rattach�es �  des participations</td>
<td><a href="#compte27">27</a>.&#160;Autres immobilisations financi�res</td>
<td><a href="#compte37">37</a>.&#160;Stocks de marchandises</td>
<td><a href="#compte47">47</a>.&#160;Comptes transitoires ou d'attente</td>
<td></td>
<td><a href="#compte67">67</a>.&#160;Charges exceptionnelles</td>
<td><a href="#compte77">77</a>.&#160;Produits exceptionnels</td>
</tr>

<tr valign="top">
<td><a href="#compte18">18</a>.&#160;Comptes de liaison des �tablissements et soci�t�s en participation</td>
<td><a href="#compte28">28</a>.&#160;Amortissements des immobilisations</td>
<td></td>
<td><a href="#compte48">48</a>.&#160;Comptes de r�gularisation</td>
<td><a href="#compte58">58</a>.&#160;Virements internes</td>
<td><a href="#compte68">68</a>.&#160;Dotations aux amortissements et aux provisions</td>
<td><a href="#compte78">78</a>.&#160;Reprises sur  amortissements et  provisions</td>
</tr>

<tr valign="top">
<td></td>
<td><a href="#compte29">29</a>.&#160;Provisions pour d�pr�ciation des immobilisations</td>
<td><a href="#compte39">39</a>.&#160;Provisions pour d�pr�ciation des stocks et en-cours</td>
<td><a href="#compte49">49</a>.&#160;Provisions pour d�pr�ciation des comptes financiers</td>
<td><a href="#compte59">59</a>.&#160;Provisions pour d�pr�ciation des comptes financiers</td>
<td><a href="#compte69">69</a>.&#160;Participation des salari�s, imp�ts sur les b�n�fices et assimil�s</td>
<td><a href="#compte79">79</a>.&#160;Transferts de  charges</td>
</tr>
</table>
</center>


<h1>Plan de comptes g�n�ral</h1>

<p><a name="BM432_1"></a>432-1. - Le plan de comptes, vis� � l'article <a href="#BM410_5"><b>410-5</b></a> <b></b>et pr�sent� ci-apr�s, est commun au syst�me de base, au syst�me abr�g� et au syst�me d�velopp�. Les comptes utilis�s dans chaque syst�me sont distingu�s de la fa�on suivante&#160;:</p>

<ul>
<li>syst�me de base : comptes imprim�s en caract�res normaux,</li>
<li><b>syst�me abr�g�</b> : comptes imprim�s en caract�res <b>gras</b> exclusivement,</li>
<li><i>syst�me d�velopp�</i> : comptes du syst�me de base et comptes imprim�s en
caract�res <i>italiques</i>.</li>
</ul>

<xsl:apply-templates select="plan-comptable/classe"/>

</body>
</html>
</xsl:template>

<xsl:template match="classe">
<h2>
  <a name="classe{@numero}" id ="classe{@numero}"/>
  <xsl:value-of select="@numero"/> - <xsl:value-of select="@nom"/>
</h2>
<ul>
  <xsl:apply-templates select="compte"/>
</ul>
</xsl:template>

<!-- compte ============================================================== -->

<xsl:template match="compte">
<li>
  <a name="compte{@numero}" id="compte{@numero}"/>
  <xsl:value-of select="@numero"/> - <xsl:value-of select="@nom"/>
</li>
<xsl:if test="compte"><ul><xsl:apply-templates select="compte"/></ul></xsl:if>
</xsl:template>

<xsl:template match="compte[@type='base']">
<li><b>
  <a name="compte{@numero}" id="compte{@numero}"/>
  <xsl:value-of select="@numero"/> - <xsl:value-of select="@nom"/>
</b></li>
<xsl:if test="compte"><ul><xsl:apply-templates select="compte"/></ul></xsl:if>
</xsl:template>

<xsl:template match="compte[@type='dev']">
<li><i>
  <a name="compte{@numero}" id="compte{@numero}"/>
  <xsl:value-of select="@numero"/> - <xsl:value-of select="@nom"/>
</i></li>
<xsl:if test="compte"><ul><xsl:apply-templates select="compte"/></ul></xsl:if>
</xsl:template>

</xsl:stylesheet>