<?xml version="1.0" encoding="ISO-8859-1"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

  <xsl:import href="common.xslt"/>

  <xsl:output method="html" 
              version="4.0" 
              encoding="UTF-8" 
              indent="yes" 
              doctype-public="-//W3C//DTD HTML 4.0//EN"/>

  <xsl:param name="societe.def" select="'../xml/societe.xml'"/>

  <xsl:param name="old.bilan" select="document($bilan.precedent)/bilan"/>

  <xsl:variable name="societe" select="document($societe.def)/societe"/>
  <xsl:variable name="plan_comptable" select="document($societe/plan-comptable/text())/plan-comptable"/>

<!-- / ===================================================================== -->

<xsl:template match="bilan-immo">
  <html>
    <head>
      <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
      <link rel="stylesheet" type="text/css" href="{$societe/html/css}" />
      <script language="javascript" type="text/javascript" src="{$societe/html/mochikit}" />

      <title>Comptabilité <xsl:value-of select="$societe/nom"/> -- Bilan</title>
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
        <xsl:text> -- Bilan immobilisations au  </xsl:text>
        <xsl:value-of select="@fin"/>
      </h1>

      <p style="font-size: small;"><a href="..">comptabilité</a> &gt;
        <a href="pilote.html">exercice</a> &gt;
        bilan des immobilisations
      </p>

      <table class="pycompta" align="center">

	      <tr>
                <th>Immobilisations</th>
                <th>Brut</th>
                <th>Augmentations</th>
                <th>Diminutions</th>
                <th>Net</th>
              </tr>

              <xsl:apply-templates select="poste"/>

              <tr>
                <td>&#xA0;</td>
                <td>&#xA0;</td>
                <td>&#xA0;</td>
                <td>&#xA0;</td>
                <td>&#xA0;</td>
              </tr>

              <tr>
                <td>
                  <b>Total général</b>
                </td>
                <td align="right">
                  <b>
                    <xsl:call-template name="format-montant">
                      <xsl:with-param name="montant"
                                      select="@report-solde"/>
                    </xsl:call-template>
                  </b>
                </td>
                <td align="right">
                  <b>
                    <xsl:call-template name="format-montant">
                      <xsl:with-param name="montant"
                                      select="@var-debit"/>
                    </xsl:call-template>
                  </b>
                </td>
                <td align="right">
                  <b>
                    <xsl:call-template name="format-montant">
                      <xsl:with-param name="montant"
                                      select="@var-credit"/>
                    </xsl:call-template>
                  </b>
                </td>
                <td align="right">
                  <b>
                    <xsl:call-template name="format-montant">
                      <xsl:with-param name="montant"
                                      select="@solde"/>
                    </xsl:call-template>
                  </b>
                </td>
              </tr>

      </table>

    </body>
  </html>
</xsl:template>

<!-- poste ============================================================== -->
<xsl:template match="poste">
  <xsl:if test="count(ancestor::poste) = 0 and position() != 1">
    <tr>
      <td>&#xA0;</td>
      <td>&#xA0;</td>
      <td>&#xA0;</td>
      <td>&#xA0;</td>
      <td>&#xA0;</td>
    </tr>
  </xsl:if>
  <tr onmouseover="addElementClass(this, 'highlighted');" onmouseout="removeElementClass(this, 'highlighted')">

    <!-- libellé -->
    <td>
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
		      <xsl:with-param name="montant" select="@solde"/>
		    </xsl:call-template>
		  </td>
		</tr>
	      </xsl:for-each>
	    </table>
	  </div>
        </xsl:otherwise>
      </xsl:choose>
    </td>

    <!-- montant brut -->
    <td align="right">
      <xsl:variable name="contenu">
        <xsl:choose>
          <xsl:when test="not(poste)">
            <xsl:call-template name="format-montant">
              <xsl:with-param name="montant" select="@report-solde"/>
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

    <!-- montant augmentations -->
    <td align="right">
      <xsl:variable name="contenu">
        <xsl:choose>
          <xsl:when test="not(poste)">
            <xsl:call-template name="format-montant">
              <xsl:with-param name="montant" select="@var-debit"/>
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


    <!-- montant diminutions -->
    <td align="right">
      <xsl:variable name="contenu">
        <xsl:choose>
          <xsl:when test="not(poste)">
            <xsl:call-template name="format-montant">
              <xsl:with-param name="montant" select="@var-credit"/>
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


    <!-- montant net -->
    <td align="right">
      <xsl:variable name="contenu">
        <xsl:choose>
          <xsl:when test="not(poste)">
            <xsl:call-template name="format-montant">
              <xsl:with-param name="montant" select="@solde"/>
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
    <tr onmouseover="addElementClass(this, 'highlighted');" onmouseout="removeElementClass(this, 'highlighted')">
      <td>
        <xsl:variable name="contenu">
          <xsl:text>Total</xsl:text>
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

      <!-- total brut -->
      <td align="right">
        <xsl:variable name="contenu">
          <xsl:call-template name="format-montant">
            <xsl:with-param name="montant" select="@report-solde"/>
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

      <!-- total augmentations -->
      <td align="right">
        <xsl:variable name="contenu">
          <xsl:call-template name="format-montant">
            <xsl:with-param name="montant" select="@var-debit"/>
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

      <!-- total diminutions -->
      <td align="right" >
        <xsl:variable name="contenu">
          <xsl:call-template name="format-montant">
            <xsl:with-param name="montant" select="@var-credit"/>
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

      <!-- montant net -->
      <td align="right" >
        <xsl:variable name="contenu">
          <xsl:call-template name="format-montant">
            <xsl:with-param name="montant" select="@solde"/>
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