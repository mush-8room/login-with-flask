#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PROJECT_ROOT=$SCRIPT_DIR
cd "${PROJECT_ROOT}"

AWS_REGION="ap-northeast-2"
IMAGE_NAME="study/login-with-flask"
IMAGE_TAG="latest"

DOCKERCLI=docker
AWSCLI=aws
JQCLI=jq

set -e 
command -v ${AWSCLI} > /dev/null 2>&1    || { echo >&2 'aws-cli not found'; exit 1; }
command -v ${DOCKERCLI} > /dev/null 2>&1 || { echo >&2 'docker not found'; exit 1; }
command -v ${JQCLI} > /dev/null 2>&1     || { echo >&2 'jq not found'; exit 1; }
set +e 

VERSION=$( poetry version -s )
AWS_ACCOUNT_ID=$( ${AWSCLI} sts get-caller-identity | ${JQCLI} -r .Account )	

ECR_HOST_NAME=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
REPO_URI=$ECR_HOST_NAME/$IMAGE_NAME

${DOCKERCLI} build -t ${IMAGE_NAME} . -f ./Dockerfile
${DOCKERCLI} tag "${IMAGE_NAME}:${IMAGE_TAG}" "${IMAGE_NAME}:${VERSION}"
${DOCKERCLI} tag "${IMAGE_NAME}:${IMAGE_TAG}" "${REPO_URI}:${VERSION}"
${DOCKERCLI} tag "${IMAGE_NAME}:${IMAGE_TAG}" "${REPO_URI}:${IMAGE_TAG}"

aws ecr get-login-password --region $AWS_REGION | \
    docker login --username AWS --password-stdin $ECR_HOST_NAME

${DOCKERCLI} push "${REPO_URI}:${VERSION}"
${DOCKERCLI} push "${REPO_URI}:${IMAGE_TAG}"

