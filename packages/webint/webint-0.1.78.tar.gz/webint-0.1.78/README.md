`webint` helps you build a web interface.

## Usage

```bash
mkdir example.site && cd example.site
poetry init --name=example-site
poetry add webint
poetry run web scaffold 
poetry version minor
poetry publish

web config --host digitalocean --token {YOUR_TOKEN}
web init example.site example-site example:app
```

### Hack

```bash
poetry run web run example:app --port 9999
```

Changes to your python code will auto-reload the local development server.

#### Deploy an update

```bash
poetry version (major|minor|patch)
poetry publish
```

Wait a couple minutes and update your site at https://example.site/system/software
