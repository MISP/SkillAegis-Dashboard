# SkillAegis

## Installation
```bash
# Setup venv
python3 -m venv venv
source venv/bin/activate

# Install deps
pip3 install -r REQUIREMENTS

# Create config file and adapt it to your needs
cp config.py.sample config.py
```

## Running the PROD setup
```bash
python3 server.py
# Access the page http://localhost:4000 with your browser
```


## Running the DEV setup
```bash
python3 server.py
```
```bash
npm run dev
# Access the page provided by the output of the above command
```

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Customize configuration

See [Vite Configuration Reference](https://vitejs.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```
