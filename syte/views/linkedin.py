# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
import oauth2 as oauth
import cgi
from django.shortcuts import render
from django.core.cache import cache

request_token_url=settings.LINKEDIN_API_URL + '/uas/oauth/requestToken?scope=r_fullprofile+r_network+rw_groups&oauth_callback={0}linkedin/auth'.format(settings.SITE_ROOT_URI)

authenticate_url=settings.LINKEDIN_API_URL + '/uas/oauth/authenticate'
access_token_url=settings.LINKEDIN_API_URL + '/uas/oauth/accessToken'
consumer = oauth.Consumer(key=settings.LINKEDIN_CONSUMER_KEY,secret=settings.LINKEDIN_CONSUMER_SECRET)

def linkedin(request, username):
    if cache.get('LINKEDIN_DATA') is None :
        url = '{0}/v1/people/~:(id,first-name,last-name,headline,public-profile-url,picture-url,location:(name),group-memberships,num-recommenders,num-connections)'.format(
            settings.LINKEDIN_API_URL)

        token = oauth.Token(settings.LINKEDIN_OAUTH_TOKEN,settings.LINKEDIN_OAUTH_TOKEN_SECRET)
        client = oauth.Client(consumer, token)
        resp, profile = client.request(url,headers={"x-li-format": "json"})
        if resp is "200":
            cache.set('LINKEDIN_DATA',profile,3600)
    else:
        profile = cache.get('LINKEDIN_DATA')

    return HttpResponse(content=profile,
                        status=resp.status,
                        content_type=resp['content-type'])

def linkedin_auth(request):
    client = oauth.Client(consumer)

    if request.GET.__contains__('oauth_token') and request.GET.__contains__("oauth_verifier"):
        context = dict()
        auth_token = request.GET.get("oauth_token")
        auth_verifier = request.GET.get("oauth_verifier")

        token = oauth.Token(request.session['request_token']['oauth_token'],
                            request.session['request_token']['oauth_token_secret'])
        client = oauth.Client(consumer, token)

        resp, content = client.request(access_token_url+"?oauth_verifier="+auth_verifier, "GET")
        if resp['status'] != '200':
            print content
            raise Exception("Invalid response from Linkedin.")

        access_token = dict(cgi.parse_qsl(content))

        context['oauth_access_token'] = access_token['oauth_token']
        context['oauth_access_token_secret'] = access_token['oauth_token_secret']



        return render(request, 'linkedin_auth.html', context)
    else:
        resp, content = client.request(request_token_url, "GET")
        if resp['status'] != '200':
            raise Exception("Invalid response from Linkedin.")

        request.session['request_token'] = dict(cgi.parse_qsl(content))
        url = "%s?oauth_token=%s" % (authenticate_url,
        request.session['request_token']['oauth_token'])

        return HttpResponseRedirect(url)

