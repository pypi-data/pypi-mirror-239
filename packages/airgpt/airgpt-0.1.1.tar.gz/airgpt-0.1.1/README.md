# airgpt

This repository contains `airgpt`: a command line tool empowered by AI and LLM. It calls OpenAI to get the appropriate command based on user prompts, and executes the command to get the results.

## Installation

1. Sign up with [OpenAI](https://platform.openai.com/account/api-keys) to get an API key. Set up the environment vairable `OPENAI_API_KEY` in a terminal:

```bash
export OPENAI_API_KEY=<your_openai_api_key>
```

2. Make sure you have Python 3.10+ installed. Install `airgpt` with the following command:

```bash
pip3 install airgpt
```

3. When the installation is complete, run the following command to start the `airgpt`:

```bash
airgpt
```

## Developing the Python source code locally
The following steps could be used to develop `airgpt` locally:

1. Clone the repository from GitHub:

```bash
git clone https://github.com/kp-enterprise/airgpt.git
```

2. Create a virtual environment and install the required libraries:

```bash
cd airgpt
python3 -m venv venv
source venv/bin/activate
pip3 install -i requirements.txt
```

3. Run the following command to start `airgpt`:

```bash
python3 airgpt.py
```
