<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE xsl:stylesheet [
 <!ENTITY xsd "http://www.w3.org/2001/XMLSchema#">
]>

<!--
  Linked Raster Data GDAL

  Copyright (C) 2014 Thomas Scharrenbach

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

  -->

<!-- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -->
<!-- XSLT Stylesheet for converting GDAL projection data from GML to RDF. -->
<!-- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -->
<xsl:stylesheet version="1.0" xmlns:gml="http://www.opengis.net/gml/"
	xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:xlink="http://www.w3.org/1999/xlink"
	xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#" xmlns:str="http://exslt.org/strings"
	xmlns:owl="http://www.w3.org/2002/07/owl#" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

	<xsl:output method="xml" version="1.0" encoding="UTF-8"
		omit-xml-declaration="no" indent="no" />

	<!-- These are the root elements. As, in terms of RDF, it is a resource we
		call the resource template. -->
	<xsl:template match="gml:ProjectedCRS">
		<rdf:RDF>
			<xsl:call-template name="resource" />
		</rdf:RDF>
	</xsl:template>
	<xsl:template match="gml:GeographicCRS">
		<rdf:RDF>
			<xsl:call-template name="resource" />
		</rdf:RDF>
	</xsl:template>

	<!-- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -->
	<!-- When handling properties we have to take special care of text nodes
		and property attributes. -->
	<!-- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -->
	<!-- Fortunately, RDF does not distinguish between data and object properties.
		If a property has a text element, we can simply declare this child to be
		a data property and add resources as objects. -->
	<!-- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -->
	<!-- In case of attributes the case seems somewhat more complicated, as
		in RDF we cannot assert the property of a specific triple an attribute (except
		using reification). In case the attribute is an xlink we can simply add this
		as an object. If not we add the attribute as another property to the anonymous
		resource as for nested properties. -->
	<!-- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -->
	<xsl:template name="property">
		<xsl:call-template name="namedresources" />
		<xsl:call-template name="anonresources" />
		<xsl:call-template name="text" />

		<xsl:for-each select="@xlink:href">
			<xsl:element name="{name(..)}">
				<xsl:attribute name="rdf:resource"><xsl:value-of select="." /></xsl:attribute>
			</xsl:element>
		</xsl:for-each>


	</xsl:template>

	<!-- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -->
	<!-- Resources in GML start with a capital letter. -->
	<!-- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -->
	<xsl:template name="namedresources">
		<xsl:if
			test="./*[contains('ABCDEFGHIJKLMNOPQRSTUVWXYZ', substring(local-name(.), 1, 1))]">
			<xsl:element name="{name()}">
				<xsl:for-each
					select="./*[contains('ABCDEFGHIJKLMNOPQRSTUVWXYZ', substring(local-name(.), 1, 1))]">
					<xsl:call-template name="resource" />
				</xsl:for-each>
			</xsl:element>
		</xsl:if>
	</xsl:template>

	<!-- Properties in GML start with a lower-case letter. So, if we observe
		properties nested in a property we have to surround all the child properties
		by a single anonymous RDF resource. We can then apply the property template
		again to all those nested properties. -->
	<xsl:template name="anonresources">
		<xsl:if
			test="./*[not(contains('ABCDEFGHIJKLMNOPQRSTUVWXYZ', substring(local-name(.), 1, 1)))]">
			<xsl:element name="{name()}">

				<xsl:for-each select="@*[name() != 'xlink:href']">
					<xsl:call-template name="attribute" />
				</xsl:for-each>
				<rdf:Description>
					<xsl:for-each
						select="./*[not(contains('ABCDEFGHIJKLMNOPQRSTUVWXYZ', substring(local-name(.), 1, 1)))]">
						<xsl:call-template name="property" />
					</xsl:for-each>
				</rdf:Description>
			</xsl:element>
		</xsl:if>
	</xsl:template>

	<!-- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -->
	<!-- In GML child elements of resources are always attributes and properties.
		As such, we can add an rdf:Descrpition tag for the resource and apply the
		property template to all child elements. -->
	<!-- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -->
	<xsl:template name="resource">
		<rdf:Description>
			<xsl:attribute name="rdf:type">http://www.opengis.net/gml/<xsl:value-of
				select="local-name()" /></xsl:attribute>
			<xsl:for-each select="@*">
				<xsl:call-template name="attribute" />
			</xsl:for-each>
			<xsl:for-each select="*">
				<xsl:call-template name="property" />
			</xsl:for-each>
		</rdf:Description>
	</xsl:template>

	<!-- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -->
	<!-- In GML attributes encode properties. -->
	<!-- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -->
	<!-- We must, however, take special care of those attributes carrying URIs. -->
	<!-- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -->
	<xsl:template name="attribute">
		<xsl:element name="{name()}">
			<xsl:choose>
				<xsl:when test="contains(., 'urn')">
					<xsl:attribute name="rdf:resource">
						<xsl:value-of select="." />
					</xsl:attribute>
				</xsl:when>
				<xsl:otherwise>
					<xsl:attribute name="rdf:datatype">http://www.w3.org/2001/XMLSchema#string</xsl:attribute>
					<xsl:value-of select="." />
				</xsl:otherwise>
			</xsl:choose>
		</xsl:element>
	</xsl:template>


	<!-- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -->
	<!-- In GML text nodes encode property values. -->
	<!-- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -->
	<!-- We must, however, take special care of those texts carrying URIs. -->
	<!-- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -->
	<xsl:template name="text">
		<xsl:if test="string-length(normalize-space(text())) > 0">
			<xsl:element name="{name()}">
				<xsl:choose>
					<xsl:when test="contains(text(), 'urn')">
						<xsl:attribute name="rdf:resource">
						<xsl:value-of select="normalize-space(text())" />
					</xsl:attribute>
					</xsl:when>
					<xsl:otherwise>
						<xsl:attribute name="rdf:datatype">http://www.w3.org/2001/XMLSchema#string</xsl:attribute>
						<xsl:value-of select="normalize-space(text())" />
					</xsl:otherwise>
				</xsl:choose>
			</xsl:element>
		</xsl:if>
	</xsl:template>

</xsl:stylesheet>