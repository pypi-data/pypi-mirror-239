from EasyDel import PyTorchServer
import logging
from .utils import BaseClassAgent, DEFAULT_SYSTEM_PROMPT

logging.basicConfig(
    level=logging.INFO
)


class InTimeDataFinderPytorchServerLlama2Type(PyTorchServer, BaseClassAgent):
    def __init__(self, config=None):
        super().__init__(config=config)
        self.gradio_app_custom = self.create_gradio_pixely_ai()

    def process_gradio_custom(self, prompt, user_id, data, system, max_new_tokens, greedy):
        history = data.split('<|END_OF_MESSAGE|>') if data != '' else []
        system = system if system != '' else DEFAULT_SYSTEM_PROMPT
        his = []
        for hs in history:
            if hs != '':
                his.append(hs.split('<|END_OF_MESSAGE_TURN_HUMAN|>'))
        history = his
        string = self.format_chat(
            prompt=prompt,
            history=history or [],
            system=system
        )
        responses = ''

        for response in self.process(
                max_new_tokens=max_new_tokens,
                max_length=self.config.max_length,
                string=string,
                stream=True,
                temperature=self.config.temperature,
                top_p=self.config.top_p,
                top_k=self.config.top_k,
        ):
            responses += response
            yield '', responses
        return '', responses
