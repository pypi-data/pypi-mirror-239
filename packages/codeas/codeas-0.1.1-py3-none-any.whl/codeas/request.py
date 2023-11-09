import logging
from typing import Optional, Union

from pydantic import BaseModel

from codeas._templates import TEMPLATE
from codeas.entities import Entity, Module


class Request(BaseModel):
    """Class for executing LLM requests on entities and modules.

    Attributes
    ----------
    instructions : str
        the instructions for the request
    context : str
        the context of the request. It can be "code", "docs", or "tests".
    guideline_prompt : Optional[str]
        the prompt to be used as a guideline for the model, by default None
    model : object
        the model to use for executing the request
    target : str
        the target of the request. It can be "code", "docs", or "tests".
    """

    instructions: str
    context: str
    guideline_prompt: Optional[str]
    model: object
    target: str

    def execute(self, entity: Union[Entity, Module], verbose: bool = True):
        if isinstance(entity, Entity):
            logging.info(f"Executing request for {entity.node.name}")
        elif isinstance(entity, Module):
            logging.info(f"Executing request for {entity.name}")

        entity_context = entity.get(self.context)
        prompt = TEMPLATE.format(
            context=self.context,
            CONTEXT=self.context.upper(),
            entity_context=entity_context,
            instructions=self.instructions,
            guideline_prompt=self.guideline_prompt,
            target=self.target,
        )
        if verbose:
            logging.info(f"Prompt:\n {prompt}")

        logging.info("Model output: \n")
        output = self.model.predict(prompt)

        if self.target in ["code", "tests"]:
            output = self._parse_output(output)

        entity.modify(self.target, output)

    def _parse_output(self, output: str):
        return output.replace("```python", "").replace("```", "").replace("CODE:", "")
