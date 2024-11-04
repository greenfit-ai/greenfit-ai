# Beans AI🫘

Find out about sustainability in your favorite sport clothing brands, in just one click!

### For users

Go to https://beans-ai.streamlit.app and feel free to explore the product from there!

### For developers

**1. Build from source**

You can build the app from source by:

- Cloning this repo:

```bash
git clone https://github.com/AstraBert/beans-ai
cd beans-ai
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

There is a Docker image available on the GitHub Container Registry at `ghcr.io/astrabert/beans-ai`. 

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