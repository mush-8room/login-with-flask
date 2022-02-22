#!/bin/bash

REFRESH_TOKEN=$1
CLIENT_ID=my-client
CLIENT_SECRET=secret

http --form :5000/oauth/token grant_type=refresh_token refresh_token=$REFRESH_TOKEN -a $CLIENT_ID:$CLIENT_SECRET -v
