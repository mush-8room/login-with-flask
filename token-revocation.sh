#!/bin/bash

TOKEN=$1
CLIENT_ID=my-client
CLIENT_SECRET=secret

http --form :5000/oauth/token/revoke token=$TOKEN token_type_hint=access_token -a $CLIENT_ID:$CLIENT_SECRET -v
