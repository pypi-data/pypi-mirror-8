<?xml version="1.0" encoding="ISO-8859-1"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

  <xsl:import href="common.xslt"/>

  <xsl:output method="html" 
              version="4.0" 
              encoding="UTF-8" 
              indent="yes" 
              doctype-public="-//W3C//DTD HTML 4.0//EN"/>

  <xsl:param name="societe.def" select="'../xml/societe.xml'"/>

  <xsl:param name="old.cr" select="document($cr.precedent)/compte-resultat"/>

  <xsl:variable name="societe" select="document($societe.def)/societe"/>
  <xsl:variable name="plan_comptable" select="document($societe/plan-comptable/text())/plan-comptable"/>

<!-- / ===================================================================== -->

<xsl:template match="compte-resultat">
  <html>
    <head>
      <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
      <link rel="stylesheet" type="text/css" href="{$societe/html/css}" />
      <script language="javascript" type="text/javascript" src="{$societe/html/mochikit}" />

      <title>Comptabilité <xsl:value-of select="$societe/nom"/> -- Compte de résultat</title>
      <script language="javascript">
      function toggleVisible(id) { 
        elt = document.getElementById(id); 
        if (elt.style.display == 'block') { elt.style.display = 'none' }
        else { elt.style.display = 'block' };
      }
      </script>
    </head>
    <body>
      <h1>
        <xsl:text>Comptabilité </xsl:text>
        <xsl:value-of select="$societe/nom"/>
        <xsl:text> -- Compte de résultat du  </xsl:text>
        <xsl:value-of select="@debut"/> 
        <xsl:text> au </xsl:text>
        <xsl:value-of select="@fin"/>
      </h1>

      <p style="font-size: small;"><a href="..">comptabilité</a> &gt;
        <a href="pilote.html">exercice</a> &gt;
        compte-résultat
      </p>

      <h2>Résultat COMPTABLE</h2>

      <table class="pycompta" width="100%" align="center" cellpadding="3">
        <tr>
          <td></td><th>N</th><th>N-1</th>
        </tr>
        <xsl:apply-templates select="produits/poste[1]"/>
        <xsl:apply-templates select="charges/poste[1]"/>
        <tr bgcolor="lightgray">
          <td>
            <b>1- Résultat d'exploitation</b>
          </td>
          <td align="right">
            <b>
              <xsl:call-template name="format-montant">
                <xsl:with-param name="montant"
                  select="produits/poste[1]/@montant - charges/poste[1]/@montant"/>
              </xsl:call-template>
            </b>
          </td>
          <td align="right">
            <b>
              <xsl:call-template name="format-montant">
                <xsl:with-param name="montant"
                  select="$old.cr/produits/poste[1]/@montant - $old.cr/charges/poste[1]/@montant"/>
              </xsl:call-template>
            </b>
          </td>
        </tr>
        <xsl:apply-templates select="produits/poste[2]"/>
        <xsl:apply-templates select="charges/poste[2]"/>
        <xsl:apply-templates select="produits/poste[3]"/>
        <xsl:apply-templates select="charges/poste[3]"/>
        <tr bgcolor="lightgray">
          <td>
            <b>2- Résultat financier</b>
          </td>
          <td align="right">
            <b>
              <xsl:call-template name="format-montant">
                <xsl:with-param name="montant"
                  select="produits/poste[3]/@montant - charges/poste[3]/@montant"/>
              </xsl:call-template>
            </b>
          </td>
          <td align="right">
            <b>
              <xsl:call-template name="format-montant">
                <xsl:with-param name="montant"
                  select="$old.cr/produits/poste[3]/@montant - $old.cr/charges/poste[3]/@montant"/>
              </xsl:call-template>
            </b>
          </td>
        </tr>
        <tr bgcolor="lightgray">
          <td>
            <b>3- Résultat courant avant impôts</b>
          </td>
          <td align="right">
            <b>
              <xsl:call-template name="format-montant">
                <xsl:with-param name="montant"
                  select="sum(produits/poste[position()&lt;=3]/@montant) - sum(charges/poste[position()&lt;=3]/@montant)"/>
              </xsl:call-template>
            </b>
          </td>
          <td align="right">
            <b>
              <xsl:call-template name="format-montant">
                <xsl:with-param name="montant"
                  select="sum($old.cr/produits/poste[position()&lt;=3]/@montant) - sum($old.cr/charges/poste[position()&lt;=3]/@montant)"/>
              </xsl:call-template>
            </b>
          </td>
        </tr>
        <xsl:apply-templates select="produits/poste[4]"/>
        <xsl:apply-templates select="charges/poste[4]"/>
        <tr bgcolor="lightgray">
          <td>
            <b>4- Résultat exceptionnel</b>
          </td>
          <td align="right">
            <b>
              <xsl:call-template name="format-montant">
                <xsl:with-param name="montant"
                  select="produits/poste[4]/@montant - charges/poste[4]/@montant"/>
              </xsl:call-template>
            </b>
          </td>
          <td align="right">
            <b>
              <xsl:call-template name="format-montant">
                <xsl:with-param name="montant"
                  select="$old.cr/produits/poste[4]/@montant - $old.cr/charges/poste[4]/@montant"/>
              </xsl:call-template>
            </b>
          </td>
        </tr>
        <xsl:apply-templates select="charges/poste[5]"/>
        <xsl:apply-templates select="charges/poste[6]"/>
        <tr>
          <td>&#xA0;</td>
          <td>&#xA0;</td>
          <td>&#xA0;</td>
        </tr>
        <tr>
          <td align="right">
            <b>Total des produits</b>
          </td>
          <td align="right">
            <b>
              <xsl:call-template name="format-montant">
                <xsl:with-param name="montant"
                  select="produits/@montant"/>
              </xsl:call-template>
            </b>
          </td>
          <td align="right">
            <b>
              <xsl:call-template name="format-montant">
                <xsl:with-param name="montant"
                  select="$old.cr/produits/@montant"/>
              </xsl:call-template>
            </b>
          </td>
        </tr>
        <tr>
          <td align="right">
            <b>Total des charges</b>
          </td>
          <td align="right">
            <b>
              <xsl:call-template name="format-montant">
                <xsl:with-param name="montant"
                  select="charges/@montant"/>
              </xsl:call-template>
            </b>
          </td>
          <td align="right">
            <b>
              <xsl:call-template name="format-montant">
                <xsl:with-param name="montant"
                  select="$old.cr/charges/@montant"/>
              </xsl:call-template>
            </b>
          </td>
        </tr>
        <tr bgcolor="lightgray">
          <td>
            <b>5- Bénéfice ou perte</b>
          </td>
          <td align="right">
            <b>
              <xsl:call-template name="format-montant">
                <xsl:with-param name="montant"
                  select="produits/@montant - charges/@montant"/>
              </xsl:call-template>
            </b>
          </td>
          <td align="right">
            <b>
              <xsl:call-template name="format-montant">
                <xsl:with-param name="montant"
                  select="$old.cr/produits/@montant - $old.cr/charges/@montant"/>
              </xsl:call-template>
            </b>
          </td>
        </tr>
      </table>

      <h2>Résultat FISCAL</h2>

      <p><em>Faut le calculer à la main...</em></p>

    </body>
  </html>
</xsl:template>

<!-- poste ============================================================== -->
<xsl:template match="poste">
  <tr onmouseover="addElementClass(this, 'highlighted');" onmouseout="removeElementClass(this, 'highlighted')">
    <td valign="top">
      <xsl:variable name="contenu">
        <xsl:value-of select="@nom"/>
      </xsl:variable>
      <xsl:variable name="ident">
        <xsl:value-of select="@id"/>
      </xsl:variable>
      <xsl:for-each select="ancestor::poste">
        <xsl:text>&#xA0;&#xA0;&#xA0;&#xA0;&#xA0;&#xA0;</xsl:text>
      </xsl:for-each>
      <xsl:choose>
        <xsl:when test="count(ancestor::poste) = 0">
          <b>
            <xsl:value-of select="$contenu"/>
          </b>
        </xsl:when>
        <xsl:when test="poste and (count(ancestor::poste) = 1)">
          <i>
            <xsl:value-of select="$contenu"/>
          </i>
        </xsl:when>
        <xsl:otherwise>
	  <a><xsl:attribute name="onclick">javascript:toggleVisible('<xsl:value-of select="$ident"/>')</xsl:attribute><xsl:value-of select="$contenu"/></a>
	  <div align="right" style="display: none"><xsl:attribute name="id"><xsl:value-of select="$ident"/></xsl:attribute>
	    <table border="1" style="border-collapse: collapse">
	      <xsl:for-each select="compte">
		<tr>
		  <td><xsl:value-of select="@num" /> - 
		  <xsl:apply-templates select="$plan_comptable">
		    <xsl:with-param name="numero" select="@num"/>
		  </xsl:apply-templates>
		  </td>
		  <td>
		    <xsl:call-template name="format-montant">
		      <xsl:with-param name="montant" select="@credit"/>
		    </xsl:call-template>
		  </td>
		  <td>
		    <xsl:call-template name="format-montant">
		      <xsl:with-param name="montant" select="@debit"/>
		    </xsl:call-template>
		  </td>
		</tr>
	      </xsl:for-each>
	    </table>
	  </div>
        </xsl:otherwise>
      </xsl:choose>
    </td>
    <td valign="top" align="right">
      <xsl:variable name="contenu">
        <xsl:choose>
          <xsl:when test="not(poste)">
            <xsl:call-template name="format-montant">
              <xsl:with-param name="montant" select="@montant"/>
            </xsl:call-template>
          </xsl:when>
          <xsl:otherwise>
            <xsl:text>&#xA0;</xsl:text>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:variable>
      <xsl:choose>
        <xsl:when test="count(ancestor::poste) = 0">
          <b>
            <xsl:value-of select="$contenu"/>
          </b>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="$contenu"/>
        </xsl:otherwise>
      </xsl:choose>
    </td>
    <td valign="top" align="right">
      <xsl:variable name="contenu">
        <xsl:choose>
          <xsl:when test="not(poste)">
            <xsl:call-template name="format-montant">
              <xsl:with-param name="montant" select="$old.cr//poste[@id = current()/@id]/@montant"/>
            </xsl:call-template>
          </xsl:when>
          <xsl:otherwise>
            <xsl:text>&#xA0;</xsl:text>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:variable>
      <xsl:choose>
        <xsl:when test="count(ancestor::poste) = 0">
          <b>
            <xsl:value-of select="$contenu"/>
          </b>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="$contenu"/>
        </xsl:otherwise>
      </xsl:choose>
    </td>
  </tr>

  <xsl:apply-templates select="poste"/>
 
  <xsl:if test="poste">
    <tr>
      <td align="right">
        <xsl:variable name="contenu">
          <xsl:text>Total </xsl:text>
          <xsl:value-of select="@nom"/>
        </xsl:variable>
        <xsl:for-each select="ancestor::poste">
          <xsl:text>&#xA0;&#xA0;&#xA0;&#xA0;&#xA0;&#xA0;</xsl:text>
        </xsl:for-each>
        <xsl:choose>
          <xsl:when test="count(ancestor::poste) = 0">
            <b>
              <xsl:value-of select="$contenu"/>
            </b>
          </xsl:when>
          <xsl:when test="poste and (count(ancestor::poste) = 1)">
            <i>
              <xsl:value-of select="$contenu"/>
            </i>
          </xsl:when>
          <xsl:otherwise>
            <xsl:value-of select="$contenu"/>
          </xsl:otherwise>
        </xsl:choose>
      </td>
      <td align="right">
        <xsl:variable name="contenu">
          <xsl:call-template name="format-montant">
            <xsl:with-param name="montant" select="@montant"/>
          </xsl:call-template>
        </xsl:variable>
        <xsl:choose>
          <xsl:when test="count(ancestor::poste) = 0">
            <b>
              <xsl:value-of select="$contenu"/>
            </b>
          </xsl:when>
          <xsl:when test="count(ancestor::poste) = 1">
            <i>
              <xsl:value-of select="$contenu"/>
            </i>
          </xsl:when>
          <xsl:otherwise>
            <xsl:value-of select="$contenu"/>
          </xsl:otherwise>
        </xsl:choose>
      </td>
      <td align="right">
        <xsl:variable name="contenu">
          <xsl:call-template name="format-montant">
            <xsl:with-param name="montant" select="$old.cr//poste[@id = current()/@id]/@montant"/>
          </xsl:call-template>
        </xsl:variable>
        <xsl:choose>
          <xsl:when test="count(ancestor::poste) = 0">
            <b>
              <xsl:value-of select="$contenu"/>
            </b>
          </xsl:when>
          <xsl:when test="count(ancestor::poste) = 1">
            <i>
              <xsl:value-of select="$contenu"/>
            </i>
          </xsl:when>
          <xsl:otherwise>
            <xsl:value-of select="$contenu"/>
          </xsl:otherwise>
        </xsl:choose>
      </td>
    </tr>
  </xsl:if>

</xsl:template>

</xsl:stylesheet>
