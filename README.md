# DBEI Digital Built Week 2023 Lab
## Web APIs with Revit and Python
File and code found in this repository relate to the lab taught for DBEI Digital Built Week Americas 2023.

## Class Description
This tutorial provides an overview of how to connect your BIM content to web-based resources using REST APIs. We will utilize the open source pyRevit application and the Python Requests module in order to export and import data directly between Revit and the web. In this demo we will leverage Airtable and it’s well-documented API in order to enable us to create a lightweight database that lives outside of Revit.

## Learning Objectives
* Understanding the basics of REST APIs and common HTTP request methods.
* How to create pyRevit tools that can be run directly from Revit with a custom ribbon.
* Introduction to the Python Requests module, and how to use it with pyRevit.
* How to use Airtable to set up a simple relational database, and how to work with its API.

## Notes
* This content is only intended to be introductory. Users looking to expand on this will need to look further for doing more advanced requests on larger numbers of records.
* The Python Requests module did not work on the virtual desktop clients provided during the in-person lab session. Therefore the code presents two options for making requests from pyRevit: (1) Python Requests module that ships with pyRevit, and (2) The WebClient class from System.Net. These two approaches are interchangable for purposes of this demonstration.
