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
      <link rel="stylesheet" type="text/css" href="{$societe/style/css}" />
      <title>Comptabilité <xsl:value-of select="$societe/nom"/> -- Compte de résultat</title>
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

      <table border="0" width="100%" align="center" cellpadding="3">

        <tr>

          <!-- Les charges -->
          <td valign="top">
            <table border="0" width="100%" align="center">
              <tr>
                <th colspan="2">Charges</th>
              </tr>

              <xsl:apply-templates select="charges/poste"/>
            </table>
          </td>

          <!-- Les produits -->
          <td valign="top">
            <table border="0" width="100%" align="center">
              <tr>
                <th colspan="2">Produits</th>
              </tr>

              <xsl:apply-templates select="produits/poste"/>
            </table>
          </td>
        </tr>

        <!-- Les totaux -->
        <tr>
          <td>&#xA0;</td>
          <td>&#xA0;</td>
        </tr>
        <tr>

          <!-- Total des charges -->
          <td valign="top">
            <table border="0" width="100%" align="center">
              <!-- Insertion du résultat s'il est positif -->
              <tr>
                <td>
                  <xsl:choose>
                    <xsl:when test="produits/@montant >= charges/@montant">
                      <b>
                        <font color="#00FF00">Solde créditeur (bénéfice)</font>
                      </b>
                    </xsl:when>
                    <xsl:otherwise>
                      <xsl:text>&#xA0;</xsl:text>
                    </xsl:otherwise>
                  </xsl:choose>
                </td>
                <td align="right">
                  <xsl:choose>
                    <xsl:when test="produits/@montant >= charges/@montant">
                      <b>
                        <font color="#00FF00">
                          <xsl:call-template name="format-montant">
                            <xsl:with-param name="montant"
                                            select="  produits/@montant
                                                    - charges/@montant "/>
                          </xsl:call-template>
                        </font>
                      </b>
                    </xsl:when>
                    <xsl:otherwise>
                      <xsl:text>&#xA0;</xsl:text>
                    </xsl:otherwise>
                  </xsl:choose>
                </td>
              </tr>
              <tr>
                <td>
                  <b>Total général</b>
                </td>
                <td align="right">
                  <b>
                    <xsl:choose>
                      <xsl:when test="produits/@montant > charges/@montant">
                        <xsl:call-template name="format-montant">
                          <xsl:with-param name="montant"
                                          select="produits/@montant"/>
                        </xsl:call-template>
                      </xsl:when>
                      <xsl:otherwise>
                        <xsl:call-template name="format-montant">
                          <xsl:with-param name="montant"
                                          select="charges/@montant"/>
                        </xsl:call-template>
                      </xsl:otherwise>
                    </xsl:choose>
                  </b>
                </td>
              </tr>
            </table>
          </td>

          <!-- Total des produits -->
          <td valign="top">
            <table border="0" width="100%" align="center">
              <!-- Insertion du résultat s'il est positif -->
              <tr>
                <td>
                  <xsl:choose>
                    <xsl:when test="charges/@montant > produits/@montant">
                      <b>
                        <font color="#FF0000">Solde débiteur (perte)</font>
                      </b>
                    </xsl:when>
                    <xsl:otherwise>
                      <xsl:text>&#xA0;</xsl:text>
                    </xsl:otherwise>
                  </xsl:choose>
                </td>
                <td align="right">
                  <xsl:choose>
                    <xsl:when test="charges/@montant > produits/@montant">
                      <b>
                        <font color="#FF0000">
                          <xsl:call-template name="format-montant">
                            <xsl:with-param name="montant"
                                            select="  charges/@montant
                                                    - produits/@montant"/>
                          </xsl:call-template>
                        </font>
                      </b>
                    </xsl:when>
                    <xsl:otherwise>
                      <xsl:text>&#xA0;</xsl:text>
                    </xsl:otherwise>
                  </xsl:choose>
                </td>
              </tr>
              <tr>
                <td>
                  <b>Total général</b>
                </td>
                <td align="right">
                  <b>
                    <xsl:choose>
                      <xsl:when test="charges/@montant > produits/@montant">
                        <xsl:call-template name="format-montant">
                          <xsl:with-param name="montant"
                                          select="charges/@montant"/>
                        </xsl:call-template>
                      </xsl:when>
                      <xsl:otherwise>
                        <xsl:call-template name="format-montant">
                          <xsl:with-param name="montant"
                                          select="produits/@montant"/>
                        </xsl:call-template>
                      </xsl:otherwise>
                    </xsl:choose>
                  </b>
                </td>
              </tr>
            </table>
          </td>

        </tr>
      </table>

    </body>
  </html>
</xsl:template>

<!-- poste ============================================================== -->
<xsl:template match="poste">
  <xsl:if test="count(ancestor::poste) = 0">
    <tr>
      <td>&#xA0;</td>
      <td>&#xA0;</td>
    </tr>
  </xsl:if>
  <tr>
    <td>
      <xsl:variable name="contenu">
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
  </tr>

  <xsl:apply-templates select="poste"/>
 
  <xsl:if test="poste">
    <tr>
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
    </tr>
  </xsl:if>

</xsl:template>

</xsl:stylesheet>