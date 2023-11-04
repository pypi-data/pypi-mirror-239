# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['local-code-qa',
 'local-code-qa.app',
 'local-code-qa.packages.rag-chroma-private.rag_chroma_private',
 'local-code-qa.packages.rag-chroma-private.tests']

package_data = \
{'': ['*'],
 'local-code-qa': ['packages/*',
                   'packages/rag-chroma-private/*',
                   'packages/rag-chroma-private/docs/*']}

install_requires = \
['fastapi>=0.103.2,<0.104.0',
 'langserve>=0.0.16',
 'sse-starlette>=1.6.5,<2.0.0',
 'tomli-w>=1.0.0,<2.0.0',
 'uvicorn>=0.23.2,<0.24.0']

setup_kwargs = {
    'name': 'local-code-qa',
    'version': '0.0.1',
    'description': 'learning to use langchain',
    'long_description': '# rag-template-1\n\n## Installation\n\nInstall the LangChain CLI if you haven\'t yet\n\n```bash\npip install -U "langchain-cli[serve]"\n```\n\n## Adding packages\n\n```bash\n# adding packages from \n# https://github.com/langchain-ai/langchain/tree/master/templates\nlangchain app add $PROJECT_NAME\n\n# adding custom GitHub repo packages\nlangchain app add --repo $OWNER/$REPO\n# or with whole git string (supports other git providers):\n# langchain app add git+https://github.com/hwchase17/chain-of-verification\n\n# with a custom api mount point (defaults to `/{package_name}`)\nlangchain app add $PROJECT_NAME --api_path=/my/custom/path/rag\n```\n\nNote: you remove packages by their api path\n\n```bash\nlangchain app remove my/custom/path/rag\n```\n\n## Setup LangSmith (Optional)\nLangSmith will help us trace, monitor and debug LangChain applications. \nLangSmith is currently in private beta, you can sign up [here](https://smith.langchain.com/). \nIf you don\'t have access, you can skip this section\n\n\n```shell\nexport LANGCHAIN_TRACING_V2=true\nexport LANGCHAIN_API_KEY=<your-api-key>\nexport LANGCHAIN_PROJECT=<your-project>  # if not specified, defaults to "default"\n```\n\n## Launch LangServe\n\n```bash\nlangchain serve\n```\n',
    'author': 'Lee Harrold',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
