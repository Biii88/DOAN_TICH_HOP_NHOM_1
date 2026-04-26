# Module 5 - Kong Gateway

## Features
- API Gateway using Kong (DB-less mode)
- Routes:
  - /orders -> Order API
  - /report -> Report Service
- Security:
  - API Key Authentication
  - Rate Limiting (10 requests/minute)

## API Key
apikey: noah-secret-key

## Note
Make sure service names in docker-compose match:
- order_api
- report_service