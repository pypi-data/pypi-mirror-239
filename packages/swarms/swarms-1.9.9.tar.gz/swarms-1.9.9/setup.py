# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['swarms',
 'swarms.agents',
 'swarms.artifacts',
 'swarms.chunkers',
 'swarms.loaders',
 'swarms.memory',
 'swarms.models',
 'swarms.prompts',
 'swarms.schemas',
 'swarms.structs',
 'swarms.swarms',
 'swarms.tools',
 'swarms.utils',
 'swarms.workers']

package_data = \
{'': ['*']}

install_requires = \
['Pillow',
 'asyncio',
 'attrs',
 'beautifulsoup4',
 'black',
 'chromadb',
 'dalle3',
 'datasets',
 'diffusers',
 'duckduckgo-search',
 'einops',
 'faiss-cpu',
 'ggl',
 'google-generativeai',
 'griptape',
 'httpx',
 'huggingface-hub',
 'langchain',
 'langchain-experimental',
 'nest_asyncio',
 'open-interpreter',
 'open_clip_torch',
 'openai',
 'playwright',
 'pydantic',
 'rich',
 'sentencepiece',
 'soundfile',
 'tabulate',
 'tenacity',
 'termcolor',
 'torch',
 'torchvision',
 'transformers',
 'wget']

setup_kwargs = {
    'name': 'swarms',
    'version': '1.9.9',
    'description': 'Swarms - Pytorch',
    'long_description': '![Swarming banner icon](images/swarmslogobanner.png)\n\n<div align="center">\n\nSwarms is a modular framework that enables reliable and useful multi-agent collaboration at scale to automate real-world tasks.\n\n\n[![GitHub issues](https://img.shields.io/github/issues/kyegomez/swarms)](https://github.com/kyegomez/swarms/issues) [![GitHub forks](https://img.shields.io/github/forks/kyegomez/swarms)](https://github.com/kyegomez/swarms/network) [![GitHub stars](https://img.shields.io/github/stars/kyegomez/swarms)](https://github.com/kyegomez/swarms/stargazers) [![GitHub license](https://img.shields.io/github/license/kyegomez/swarms)](https://github.com/kyegomez/swarms/blob/main/LICENSE)[![GitHub star chart](https://img.shields.io/github/stars/kyegomez/swarms?style=social)](https://star-history.com/#kyegomez/swarms)[![Dependency Status](https://img.shields.io/librariesio/github/kyegomez/swarms)](https://libraries.io/github/kyegomez/swarms) [![Downloads](https://static.pepy.tech/badge/swarms/month)](https://pepy.tech/project/swarms)\n\n\n### Share on Social Media\n\n[![Join the Agora discord](https://img.shields.io/discord/1110910277110743103?label=Discord&logo=discord&logoColor=white&style=plastic&color=d7b023)![Share on Twitter](https://img.shields.io/twitter/url/https/twitter.com/cloudposse.svg?style=social&label=Share%20%40kyegomez/swarms)](https://twitter.com/intent/tweet?text=Check%20out%20this%20amazing%20AI%20project:%20&url=https%3A%2F%2Fgithub.com%2Fkyegomez%2Fswarms) [![Share on Facebook](https://img.shields.io/badge/Share-%20facebook-blue)](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fgithub.com%2Fkyegomez%2Fswarms) [![Share on LinkedIn](https://img.shields.io/badge/Share-%20linkedin-blue)](https://www.linkedin.com/shareArticle?mini=true&url=https%3A%2F%2Fgithub.com%2Fkyegomez%2Fswarms&title=&summary=&source=)\n\n[![Share on Reddit](https://img.shields.io/badge/-Share%20on%20Reddit-orange)](https://www.reddit.com/submit?url=https%3A%2F%2Fgithub.com%2Fkyegomez%2Fswarms&title=Swarms%20-%20the%20future%20of%20AI) [![Share on Hacker News](https://img.shields.io/badge/-Share%20on%20Hacker%20News-orange)](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fgithub.com%2Fkyegomez%2Fswarms&t=Swarms%20-%20the%20future%20of%20AI) [![Share on Pinterest](https://img.shields.io/badge/-Share%20on%20Pinterest-red)](https://pinterest.com/pin/create/button/?url=https%3A%2F%2Fgithub.com%2Fkyegomez%2Fswarms&media=https%3A%2F%2Fexample.com%2Fimage.jpg&description=Swarms%20-%20the%20future%20of%20AI) [![Share on WhatsApp](https://img.shields.io/badge/-Share%20on%20WhatsApp-green)](https://api.whatsapp.com/send?text=Check%20out%20Swarms%20-%20the%20future%20of%20AI%20%23swarms%20%23AI%0A%0Ahttps%3A%2F%2Fgithub.com%2Fkyegomez%2Fswarms)\n\n</div>\n\n[![Swarm Fest](images/swarmfest.png)](https://github.com/users/kyegomez/projects/1)\n\n## Vision\nAt Swarms, we\'re transforming the landscape of AI from siloed AI agents to a unified \'swarm\' of intelligence. Through relentless iteration and the power of collective insight from our 1500+ Agora researchers, we\'re developing a groundbreaking framework for AI collaboration. Our mission is to catalyze a paradigm shift, advancing Humanity with the power of unified autonomous AI agent swarms.\n\n-----\n\n## 🤝 Schedule a 1-on-1 Session\n\nBook a [1-on-1 Session with Kye](https://calendly.com/swarm-corp/30min), the Creator, to discuss any issues, provide feedback, or explore how we can improve Swarms for you.\n\n\n----------\n\n## Installation\n`pip3 install --upgrade swarms`\n\n---\n\n## Usage\nWe have a small gallery of examples to run here, [for more check out the docs to build your own agent and or swarms!](https://docs.apac.ai)\n\n### `Flow` Example\n- The `Flow` is a superior iteratioin of the `LLMChain` from Langchain, our intent with `Flow` is to create the most reliable loop structure that gives the agents their "autonomy" through 3 main methods of interaction, one through user specified loops, then dynamic where the agent parses a <DONE> token, and or an interactive human input verison, or a mix of all 3. \n\n```python\n\nfrom swarms.models import OpenAIChat\nfrom swarms.structs import Flow\n\napi_key = ""\n\n# Initialize the language model, this model can be swapped out with Anthropic, ETC, Huggingface Models like Mistral, ETC\nllm = OpenAIChat(\n    # model_name="gpt-4"\n    openai_api_key=api_key,\n    temperature=0.5,\n    # max_tokens=100,\n)\n\n## Initialize the workflow\nflow = Flow(\n    llm=llm,\n    max_loops=2,\n    dashboard=True,\n    # stopping_condition=None,  # You can define a stopping condition as needed.\n    # loop_interval=1,\n    # retry_attempts=3,\n    # retry_interval=1,\n    # interactive=False,  # Set to \'True\' for interactive mode.\n    # dynamic_temperature=False,  # Set to \'True\' for dynamic temperature handling.\n)\n\n# out = flow.load_state("flow_state.json")\n# temp = flow.dynamic_temperature()\n# filter = flow.add_response_filter("Trump")\nout = flow.run("Generate a 10,000 word blog on health and wellness.")\n# out = flow.validate_response(out)\n# out = flow.analyze_feedback(out)\n# out = flow.print_history_and_memory()\n# # out = flow.save_state("flow_state.json")\n# print(out)\n\n\n\n```\n\n\n## `GodMode`\n- A powerful tool for concurrent execution of tasks using multiple Language Model (LLM) instances.\n\n```python\nfrom swarms.swarms import GodMode\nfrom swarms.models import OpenAIChat\n\napi_key = ""\n\nllm = OpenAIChat(\n    openai_api_key=api_key\n)\n\n\nllms = [\n    llm,\n    llm,\n    llm\n]\n\ngod_mode = GodMode(llms)\n\ntask = \'Generate a 10,000 word blog on health and wellness.\'\n\nout = god_mode.run(task)\ngod_mode.print_responses(task)\n```\n\n------\n\n### `SequentialWorkflow`\n- Execute tasks step by step by passing in an LLM and the task description!\n- Pass in flows with various LLMs\n- Save and restore Workflow states!\n```python\nfrom swarms.models import OpenAIChat\nfrom swarms.structs import Flow\nfrom swarms.structs.sequential_workflow import SequentialWorkflow\n\n# Example usage\napi_key = (\n    ""  # Your actual API key here\n)\n\n# Initialize the language flow\nllm = OpenAIChat(\n    openai_api_key=api_key,\n    temperature=0.5,\n    max_tokens=3000,\n)\n\n# Initialize the Flow with the language flow\nflow1 = Flow(llm=llm, max_loops=1, dashboard=False)\n\n# Create another Flow for a different task\nflow2 = Flow(llm=llm, max_loops=1, dashboard=False)\n\n# Create the workflow\nworkflow = SequentialWorkflow(max_loops=1)\n\n# Add tasks to the workflow\nworkflow.add("Generate a 10,000 word blog on health and wellness.", flow1)\n\n# Suppose the next task takes the output of the first task as input\nworkflow.add("Summarize the generated blog", flow2)\n\n# Run the workflow\nworkflow.run()\n\n# Output the results\nfor task in workflow.tasks:\n    print(f"Task: {task.description}, Result: {task.result}")\n\n```\n\n### `OmniModalAgent`\n- OmniModal Agent is an LLM that access to 10+ multi-modal encoders and diffusers! It can generate images, videos, speech, music and so much more, get started with:\n\n```python\nfrom swarms.models import OpenAIChat\nfrom swarms.agents import OmniModalAgent\n\napi_key = "SK-"\n\nllm = OpenAIChat(model_name="gpt-4", openai_api_key=api_key)\n\nagent = OmniModalAgent(llm)\n\nagent.run("Create a video of a swarm of fish")\n\n```\n\n---\n\n## Documentation\n- For documentation, go here, [swarms.apac.ai](https://swarms.apac.ai)\n\n\n## Contribute\n\nWe\'re always looking for contributors to help us improve and expand this project. If you\'re interested, please check out our [Contributing Guidelines](CONTRIBUTING.md) and our [contributing board](https://github.com/users/kyegomez/projects/1)\n\n\n# License\nMIT\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/swarms',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
