import openai

from ..constants import DEFAULT_MODEL
from ..prompts import DEFAULT_PROMPT

class OpenAIClient:
    """OpenAI Client"""

    def __init__(self, openai_api_key: str):
        openai.api_key = openai_api_key
        
        # model prices as of 10/23
        self.prices = {
            "gpt-3.5-turbo-4k": [0.0015, 0.002],
            "gpt-3.5-turbo-16k": [0.003, 0.004],
            "ft-gpt-3.5-turbo": [0.012, 0.016],
            "ft-babbage-002": [0.0016, 0.0016],
            "ft-davinci-002": [0.012, 0.012],
            "gpt-4-8k": [0.03, 0.06],
            "gpt-4-32k": [0.06, 0.12],
        }

    def fetch_unix_command(
            self, 
            user_input: str = "", 
            system_prompt: str = DEFAULT_PROMPT,
            model: str = DEFAULT_MODEL,
            temperature: float = 0,
            max_tokens: int = 250,
        ) -> str:
        """
        Converts natural language user input to a corresponding UNIX command.
        """
        
        unix_command: str = self._fetch_from_gpt(
            user_input=user_input,
            system_prompt=system_prompt,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        
        return unix_command.strip()

    def _fetch_from_gpt(
            self,
            user_input,
            system_prompt,
            model, 
            temperature,
            max_tokens,
        ) -> str:
        """
        fetch from gpt
        """

        try:
            completion = openai.ChatCompletion.create(
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ]
            )
        except openai.InvalidRequestError:
            print("Error when fetching from OpenAI.")
            
        try:
            result = completion.choices[0].message.content
            usage = completion.usage
        except KeyError as e:
            print(e)

        total_tokens = usage.total_tokens
        total_cost = self.get_total_cost_of_tokens_used(
            model="gpt-3.5-turbo-4k",
            prompt_tokens=usage.prompt_tokens,
            completion_tokens=usage.completion_tokens,
        )
        print("  => Tokens: " + str(total_tokens))
        print("  => Cost:   $" + str(total_cost))

        return result
    
    def get_total_cost_of_tokens_used(
            self, 
            model,
            prompt_tokens: int, 
            completion_tokens: int,
        ):
        """
        Get total cost of using an OpenAI model for a given request.
        """

        try:
            price_per_1k_tokens: list = self.prices[model]
        except KeyError:
            return {"error": "Model does not exist."}

        price_per_token_input = price_per_1k_tokens[0] / 1000
        price_per_token_output = price_per_1k_tokens[1] / 1000

        estimated_cost_input = price_per_token_input * prompt_tokens
        estimated_cost_output = price_per_token_output * completion_tokens

        total_cost = estimated_cost_input + estimated_cost_output
        return "{:.3f}".format(total_cost)