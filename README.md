# Flask Reverse Proxy

A Flask "extension" for applications in a reverse proxy not at the root.
A complete rip off of http://flask.pocoo.org/snippets/35/.

Here is a basic Nginx configuration file to make this work.

```
server {

    location /production {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Scheme $scheme;
        proxy_set_header X-Script-Name /production;
    }


}

```

I use this at work to run two versions of an app, one for staging and one
for production on the same server.

```
server {

    location /staging {
        proxy_pass http://127.0.0.1:8002;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Scheme $scheme;
        proxy_set_header X-Script-Name /staging;
    }


}

```

A basic apache example:

```
<IfModule !proxy_module>
LoadModule proxy_module modules/mod_proxy.so
</IfModule>
<IfModule !proxy_http_module>
LoadModule proxy_http_module modules/mod_proxy_http.so
</IfModule>

#SetEnvIf Request_URI ^/production production
#SetEnvIf Request_URI ^/staging staging

#RequestHeader set X-Scheme https
#RequestHeader set X-Script-Name "/production" env=production
#RequestHeader set X-Script-Name "/staging" env=staging
#RequestHeader set X-Forwarded-Server-Custom "EXTERNAL HOST NAME"

#For a local proxy only:
ProxyPass /production/ http://localhost:8001/production/
ProxyPassReverse /production/ http://localhost:8001/production/
ProxyPass /staging/ http://localhost:8002/staging/
ProxyPassReverse /staging/ http://localhost:8002/staging/

#If you are passing through to another host:
#<Proxy http://puppetmasterci01.int.ci.lan:80>
#    ProxySet connectiontimeout=5 timeout=90
#</Proxy>

# Proxy for _aliases and .*/_search
#<LocationMatch "^/(production)(.*)$">
#    ProxyPassMatch http://HOSTNAME:8001/$1$2
#    ProxyPassReverse http://HOSTNAME:8001/$1$2
#</LocationMatch>
#<LocationMatch "^/(staging)(.*)$">
#    ProxyPassMatch http://HOSTNAME:8002/$1$2
#    ProxyPassReverse http://HOSTNAME:8002/$1$2
#</LocationMatch>

```

Usage:

```python

from flask_reverse_proxy import FlaskReverseProxied

proxied = FlaskReverseProxied(app)

```


```python

from flask_reverse_proxy import FlaskReverseProxied

proxied = FlaskReverseProxied()

# later ...
proxied.init_app(app)

```
