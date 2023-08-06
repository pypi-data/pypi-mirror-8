<?xml version="1.0" encoding="ISO-8859-1"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:set="http://exslt.org/sets"
                version="1.0">

<xsl:output method="xml" encoding="ISO-8859-1" indent="yes" />

<!-- / ===================================================================== -->

<xsl:template match="/">

  <facturation>
    <xsl:for-each select="set:distinct(journal/ecriture[*/@compte='411']/ref[@type='doc'])">
     <facture>
       <xsl:attribute name="id"><xsl:value-of select="."/></xsl:attribute>
       <xsl:attribute name="docid"><xsl:value-of select="@id"/></xsl:attribute>

       <xsl:for-each select="/journal/ecriture[debit/@compte='411' and ref=current()]">
         <action type="emission">
           <xsl:copy-of select="@date"/>
         </action>
       </xsl:for-each>
       <xsl:for-each select="/journal/ecriture[credit/@compte='411' and ref=current()]">
         <action type="paiement">
           <xsl:copy-of select="@date"/>
         </action>
       </xsl:for-each>
     </facture>
    </xsl:for-each>
  </facturation>

</xsl:template>

</xsl:stylesheet>