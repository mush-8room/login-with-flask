#!/bin/bash

CODE=$1
REDIRECT_URI=http://localhost:3000/oauth/callback
CLIENT_ID=my-client
CLIENT_SECRET=secret

http --form :5000/oauth/token code=$CODE grant_type=authorization_code redirect_uri=$REDIRECT_URI -a $CLIENT_ID:$CLIENT_SECRET -v 
