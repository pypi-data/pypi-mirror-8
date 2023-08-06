Django Postcode Proxy
=========================

Simple proxy class to integrate Dutch 'postcode/huisnr' address verification in your Django application.

Install
=========

          $ pip install django-postcodepy-proxy


Quick start
-----------------

1. Add 'postcodepy_proxy' to your INSTALLED_APPS setting like this::

         INSTALLED_APPS= (
             ...
             'postcodepy_proxy',
         )

2. Add the config part for the proxy::

         POSTCODEPY = {
           "AUTH" : {
             "API_ACCESS_KEY" : "<the key you got from postcode.nl>",
             "API_ACCESS_SECRET" : "<the secret you got from postcode.nl>",
           },
         }

In your app ...
================

Derive a class from the *PostcodepyProxyView* class and implement your own logic like the 2 simple examples below for HTML and JSON rendering.

## Simple HTML rendering
 
      from django.shortcuts import render

      # Create your views here.

      from postcodepy_proxy.views import PostcodepyProxyView
      from postcodepy import postcodepy

      class PCDemoHTMLView( PostcodepyProxyView ):
        template_name = "postcodeproxy.html"
      
        def get(self, request, *args, **kwargs):
          rv = super(PCDemoHTMLView, self).get(request, *args, **kwargs)
          return render(request, self.template_name, rv)


## JSON rendering

Most likely is that you want JSON rendering for XHR-io in your application. Implement exception-handling that suits your needs.


      from django.http import HttpResponse
      from postcodepy.postcodepy import PostcodeError
      import json

      class PCDemoJSONView( PostcodepyProxyView ):
        def get(self, request, *args, **kwargs):
          rv = None
          try:
            rv = super(PCDemoJSONView, self).get(request, *args, **kwargs)
          except PostcodeError, e:
            # Pass the exceptioninformation as response data
            rv = e.response_data

          return HttpResponse( json.dumps(rv), content_type="application/json")


## Route the requests

      url(r'^jsonpostcode/(?P<postcode>[\d]{4}[a-zA-Z]{2})/(?P<houseNumber>[\d]+)/$', views.PCDemoJSONView.as_view() ),
      url(r'^jsonpostcode/(?P<postcode>[\d]{4}[a-zA-Z]{2})/(?P<houseNumber>[\d]+)/(?P<houseNumberAddition>[A-Za-z]+)/$', views.PCDemoJSONView.as_view() ),
