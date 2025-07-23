## MODAL CONTAINER (modal.com)

FIRST SETUP:
- make sure installed modal on python
- run python -m modal setup

CONTAINER INTIALIZATION:
- Go to Workspace Settings
- Go to API Tokens
- Create New Token
- modal token set --token-id <token_id> --token-secret <token_secret> --profile=<workspace_name>
- modal profile activate <workspace_name>

## TO SERVE IN MODAL CONTAINER (For local testing purposes)
`
modal config set-environment development
`

` on the root folder
modal serve infra.modal.main
`

## TO DEPLOY ON PROD (MAIN)

`
modal config set-environment main
`

`
modal deploy src.main --tag $(GIT_HASH)  ($(GIT_HASH) or the manual value of git rev-parse HEAD)