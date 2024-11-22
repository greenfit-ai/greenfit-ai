<h1 align="center">GreenFit AI</h1>
<h2 align="center">Find out about sustainability in your favorite sport clothing brands, in just one click!🌱</h2>


<div align="center">
    <img src="https://img.shields.io/github/languages/top/AstraBert/greenfit-ai" alt="GitHub top language">
   <img src="https://img.shields.io/github/commit-activity/t/AstraBert/greenfit-ai" alt="GitHub commit activity">
   <img src="https://img.shields.io/badge/greenfit_ai-beta-green" alt="Static Badge">
   <img src="https://img.shields.io/github/license/AstraBert/greenfit-ai" alt="License">
   <img src="https://github.com/AstraBert/greenfit-ai/actions/workflows/docker-publish.yml/badge.svg" alt="Docker deployment status">
   <br>
   <br>
   <div>
        <img src="logo.png" alt="Flowchart" align="center" width=200 height=200>
   </div>
</div>

### For users

Go to [our Streamlit **demo** webapp](https://huggingface.co/spaces/greenfit-ai/greenfit-ai) and get a hands-on experience of GreenFit AI!

Otherwise, head over to our [product showcase website](https://astrabert.github.io/greenfitai-showcase/) and feel free to explore the product from there

### For developers

**1. Build from source**

You can build the app from source by:

- Cloning this repo:

```bash
git clone https://github.com/AstraBert/greenfit-ai
cd greenfit-ai
```

- Create a virtual environment and activate it:

```bash
python3 -m venv streamlit-app
source streamlit-app/bin/activate
```

- Install the required dependencies:

```bash
python3 -m pip install -r requirements.txt
```

- Build your `.streamlit/secrets.toml` file like this:

```bash
rapid_api_key="RAPID_API_KEY"
openai_api_key="OPENAI_API_KEY"
qdrant_api_key="QDRANT_API_KEY"
qdrant_url="QDRANT_URL"
courier_auth_token="COURIER_AUTH_TOKEN"
supa_key="SUPABASE_ANON_KEY"
supa_url="SUPABASE_URL"
```
- Run the application:

```bash
python3 -m streamlit run app.py
```

**2. Use the Docker image**

There is a Docker image available on the GitHub Container Registry at `ghcr.io/astrabert/greenfit-ai`. 

You can choose two ways to use the Docker image:

- _From the pre-built image_: 
    + Pull the image: we advise you pull the `main` tag, as it is on track with the latest modifications to the app
    ```bash
    docker pull ghcr.io/astrabert/beans-ai:main
    ```
    + Create a `.streamlit/secrets.toml` as specified in the previous section
    + Create a `.env` file and specify the path to `.streamlit/secrets.toml` under the `STREAMLIT_SECRETS_PATH` variable
    + Launch docker compose and find the app http://localhost:8501:
    ```bash
    docker compose up -d
    ```
- _Build the image yourself_ (**assuming you have cloned the repository and you are inside it**): 
    + Create a `.streamlit/secrets.toml` as specified in the previous section
    + Create a `.env` file and specify the path to `.streamlit/secrets.toml` under the `STREAMLIT_SECRETS_PATH` variable
    + Launch docker compose with the build option and find the app http://localhost:8501:
    ```bash
    docker compose -f compose.build.yaml up -d
    ```

Find an example of the `.env` file on [`.env.example`](./.env.example)