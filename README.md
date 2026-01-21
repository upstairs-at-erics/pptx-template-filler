# PPT Template Filler API

A high-performance REST API and Admin UI for automating PowerPoint document generation.   
Using standard `.pptx` files as templates containing multiple `{{tagname}}`, tags can be automatically replaced with dynamic data and fully populated powerpoint file downloaded.

## Screenshots
![login](https://github.com/user-attachments/assets/322fe62d-5fad-4649-a59a-cc3862506d37)




## Overview

The service scans PowerPoint template files (.pptx) for text delimited by curly braces e.g., `{{CLIENT_NAME}}` and provides endpoints to list, inspect, and fill these tags from JSON payloads.

### Key Features
* **Dual Interface**: Full REST API for programmatic use and a Flask-based Admin UI for manual testing/management.
* **Slide Filtering**: Use the `keep` array in the json object to choose exactly which slide indices to retain in the final output.
* **Flexible Tagging**: Supports blanking out tags, skipping tags for iterative processing, or nested tagging.
* **Production Ready**: Built with Flask and served via Gunicorn (threaded workers).
* **Observability**: Integrated logging and status endpoints for monitoring health and route availability.


### Workflow
API and UI workflow is identical.  
The api is accessed at  `/api`.  
The UI provides a ready way to test the service as is reached at `/ui`    
1.  **Tagging**: Add placeholders delimited by `{{}}` into your `.pptx` file (e.g., `Project: {PROJ_NAME}`).
2.  **Upload**: Send the template to the app via the UI or `/api/upload-template`.
3.  **Inspect**: Check `/api/placeholders` to see a list of detected tags by slide.
4.  **Fill**: Post a JSON data object to `/api/fill-template`.
5.  **Output**: Receive the processed `.pptx` file immediately as a stream/download.



## API Routes
**<YOUR_KEY>** is set in environment variables in docker deployment.  
**<BASEURL>** will be `http://node:port`  
All GET routes require:`?api_key=YOUR_KEY`  


### GET /status
Verify the API is reachable and authenticated. Returns API server status and navigation url's.
```curl
curl -X GET "http://<BASEURL>/api/status?api_key=<YOUR_KEY>"
```


### GET /list-templates
Returns a list of all uploaded `.pptx` templates.  
**Example:**  
```curl  
curl -X GET "http://<BASEURL>/api/list-templates?api_key=<YOUR_KEY>"
```

### POST /upload-template
Uploads a new PowerPoint template to the server.

**Example:**
```curl
curl -X POST http://<BASEURL>/api/upload-template?api_key=<YOUR_KEY> \
     -F "file=@example.pptx"
```

### GET /download-template
Downloads an retained un-filled template back to the client.

**Example:**
```curl
curl -X GET "http://<BASEURL>/api/download-template?template=example.pptx&api_key=<YOUR_KEY>" \
     --output example.pptx
```

### POST /remove-template
Removes a retained un-filled template from the server.  
Example:
```curl
curl -X POST http://<BASEURL>/api/remove-template?api_key=<YOUR_KEY> \
     -d '{"template":"example.pptx"}'
```  

### GET /placeholders

Returns a list of placeholder tags found inside the selected template.

**Example:**
```curl
curl -X GET "http://<BASEURL>/api/placeholders?template=example.pptx&api_key=<YOUR_KEY>"
```  
### POST /fill-template
**Example:**
```curl
curl -X POST "<BASEURL>/api/fill-template?api_key=<YOUR_KEY>" \
     -H "Content-Type: application/json" \
     -d '<DATAOBJECT>' \
     --output filled_example.pptx"
```  
#### Data Object
```json
{
  "template": "example.pptx",
  "key": APIKEY,
  "replacements": {
     "TAG1": "tagvalue1", 
     "TAG2": "tagvalue2",
     },
  "keep" : []
}

```   
`keep` is a list of slide numbers to keep starting at slide 0. All other slides are discarded. If omitted, all slides are returned.  

#### Special Replacement Logic (in tagvalues)  
The output can be controlled using these special values in the replacements object:

**Blank a tag**: Use `""`  or `null` .

**Skip/Ignore a tag**: Use `"!!!"`  (this keeps the {TAG} in the document for future processing).

**Nested tagging**: Use `"{NEW_TAG}"` to replace one placeholder with another.
  
## Stack

The application is containerized and managed via Docker Compose (Tailscale/Traefik ready).

* **Runtime**: Python 3.11+ / Flask
* **WSGI Server**: Gunicorn
* **Security**: API Key requirement for all endpoints; Session-based auth for Admin UI.
* **Persistence**: Bind mounts for templates, filled outputs, and logs.

## Docker Build & Deployment
Example Build Command (creates image in Docker)  
```bash 
docker build -t <image-name> .
```
Example docker-compose.yml (can be pasted into Portainer Stacks)  
```yaml 
services:
  pptx-micro-01:
    image: <image-name>:latest
    container_name: pptx1-filler

    ports:
      - "<tailnet IP>:5110:5110"

    environment:
      SECRET_KEY: "a secret password you make"
      TENANT: "using organisation"
      REMOVE_FILLED_FILES: "False"
      UPLOAD_FOLDER: "uploaded"
      FILLED_FOLDER: "filled"
      ADMIN_USERNAME: "username for ui"
      ADMIN_PASSWORD: "password for ui"
      API_KEY: "32 character key for api"

    volumes:
      - /location/for/hot-patch-code:/app
      - /location/for/cached/filled/files:/app/filled
      - /location/for/logs:/app/logs
      - /location/for/cached/uploads:/app/uploaded

    restart: unless-stopped

    networks:
      - root_default

networks:
  root_default:
    external: true

```


This project is licensed under the **MIT License**.
[MIT](https://choosealicense.com/licenses/mit/)
