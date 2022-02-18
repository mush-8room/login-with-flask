#!/bin/bash 

PATH=$( http :5000/oauth/authorize client_id==my-client redirect_uri==http://localhost:3000/oauth/callback scope=="openid profile" response_type==code --offline | grep GET | awk '{ print $2 }' )

echo http://localhost:5000$PATH
