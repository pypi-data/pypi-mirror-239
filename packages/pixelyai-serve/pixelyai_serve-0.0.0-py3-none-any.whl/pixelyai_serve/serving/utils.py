import gradio_client as gc
import json
from typing import List
import gradio as gr
import subprocess
import functools
from EasyDel.serve.utils import seafoam

END_OF_MESSAGE_TURN_HUMAN = '<|END_OF_MESSAGE_TURN_HUMAN|>'
END_OF_MESSAGE = '<|END_OF_MESSAGE|>'

FOUND_SYSTEM_MESSAGE = (
    "you will get extra information to use in order to chat with users and answer the questions without"
    " mentioning the extra information if you been wanted to introduce yourself "
    "your Name is PixelyAI you are developed By a team of Researchers at LucidBrain Company Located in "
    "Dubai otherwise you dont have to introduce yourself just answer the question"
)

DEFAULT_SYSTEM_PROMPT = (
    "You are a helpful, respectful and honest assistant and act as wanted, if you been wanted to introduce yourself "
    "your Name is PixelyAI you are developed By a team of Researchers at LucidBrain Company Located in "
    "Dubai otherwise you dont have to introduce yourself just answer the question"
)


class BaseClassAgent:
    def count_tokens(self, prompt, user_id, data, system, *_):
        history = data.split('<|END_OF_MESSAGE|>') if data != '' else []
        system = system if system != '' else DEFAULT_SYSTEM_PROMPT
        his = []
        for hs in history:
            if hs != '':
                his.append(hs.split('<|END_OF_MESSAGE_TURN_HUMAN|>'))
        history = his
        string = self.prompt_llama2_model(
            message=prompt,
            chat_history=history or [],
            system_prompt=system
        )
        return len(self.tokenizer.encode(string))

    @staticmethod
    def get_available_backends(url="https://api.pixelyai.com/api/gradio/"):
        return get_available_backends(url=url)

    @staticmethod
    def set_available_backend(url_backend: str, url="https://api.pixelyai.com/api/gradio/", method='put'):
        set_available_backend(url_backend=url_backend, url=url, method=method)

    def launch(self,
               share_chat: bool = False,
               share_inst: bool = False,
               share_custom: bool = True
               ):
        share_kwargs = {}
        assert not share_chat or not share_inst, 'you have to pass at least one of sharing options True'
        if share_chat:
            self.create_gradio_ui_chat().launch(share=True)
            share_kwargs['chat'] = self.create_gradio_ui_chat.share_url
        if share_inst:
            self.create_gradio_ui_instruct().launch(share=True)
            share_kwargs['inst'] = self.create_gradio_ui_instruct.share_url
        if share_custom:
            self.gradio_app_custom.launch(share=True)
            share_kwargs['custom'] = self.gradio_app_custom.share_url
        return share_kwargs

    def create_gradio_pixely_ai(self):
        with gr.Blocks(theme=seafoam) as block:
            gr.Markdown("# <h1> <center>Powered by [EasyDeL](https://github.com/erfanzar/EasyDel) </center> </h1>")

            with gr.Row():
                with gr.Column():
                    prompt = gr.Textbox(show_label=True, placeholder='Message Box', container=True,
                                        label="Message Box")
                    user_id = gr.Textbox(show_label=True, placeholder='UserId', container=True, value='',
                                         label="UserId")
                    data = gr.Textbox(show_label=True, placeholder='Data', container=True, value='', label="Data")
                    system = gr.Textbox(show_label=True, placeholder='System', container=True, value='', label="System")
                    response = gr.TextArea(show_label=True, placeholder='Response', container=True,
                                           label="Response")
                    submit = gr.Button(variant="primary")
            with gr.Row():
                with gr.Accordion('Advanced Options', open=False):
                    max_new_tokens = gr.Slider(value=self.config.max_new_tokens, maximum=10000,
                                               minimum=self.config.max_stream_tokens,
                                               label='Max New Tokens', step=self.config.max_stream_tokens)

                    greedy = gr.Checkbox(value=False, label='Greedy Search')
                    status = gr.Button(value='Status')
                    token_counter = gr.Button(value='Token Counter')
                    token_counter_prompt = gr.Button(value='Token Prompt Counter')
                    display = gr.TextArea(show_label=True, placeholder='Display', container=True,
                                          label="Display")

            inputs = [prompt, user_id, data, system, max_new_tokens, greedy]
            _ = prompt.submit(fn=self.process_gradio_custom, inputs=inputs, outputs=[prompt, response])
            _ = submit.click(fn=self.process_gradio_custom, inputs=inputs, outputs=[prompt, response])
            _ = token_counter.click(fn=lambda p: len(self.tokenizer.encode(p)), inputs=[prompt], outputs=[display])
            _ = status.click(fn=lambda: str(self.status()), outputs=[display])
            _ = token_counter_prompt.click(fn=self.count_tokens, inputs=inputs, outputs=display)
            block.queue()
        return block

    @staticmethod
    def format_chat(history: List[List[str]], prompt: str, system: str = None) -> str:
        return prompt_model(message=prompt, system_prompt=system, chat_history=history)

    @staticmethod
    def prompt_model(message: str, chat_history, system_prompt: str):
        return prompt_model(message=message, chat_history=chat_history, system_prompt=system_prompt)


def format_chat_for_ai_client(user: List[str], assistance: List[str]):
    history = ''
    for c1, c2 in zip(user, assistance):
        history += f'{c1}{END_OF_MESSAGE_TURN_HUMAN}{c2}{END_OF_MESSAGE}'
    return history


def in_check(
        response: str,
        question: str,
        non_legal_point: List[str] = None
):
    if non_legal_point is None:
        non_legal_point = [
            'the answer to the question is "no"',
            'The context does not provide',
            'the context provided does not provide any information that would allow '
            'you to determine the answer',
            'it is not possible to answer the question',
            'The given context does not provide any information about',
            'I can only respond with a "no" based on the provided context',
            'I can only respond with a "no"',
            'Answer: No,',
            'it is not related to the provided contex',
            'is not mentioned anywhere in the provided context',
            'my answer would be "no"',
            'the context does not mention anything',
            'not related to the context provided',
            'not related to the provided contex',
            'i cannot answer your question',
            'The context mentions nothing about',
            'I cannot provide an answer to the question',
            'I cannot provide an answer',
            'not mentioned in the provided context',
            'not mentioned in the context',
            'Please go ahead and ask your question',
            'context provided does not mention'
        ]
    found = True
    _s = (f'"{question}" is not provided', f'{question} is not provided', f'The answer to "{question}?" is NO',
          f'The answer to "{question}" is NO')
    for s in _s:
        non_legal_point.append(s)
    for point in non_legal_point:
        if point.lower() in response.lower():
            found = False
    return found


def prompt_model(message: str, chat_history, system_prompt: str) -> str:
    texts = [f'<s>[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\n\n']
    do_strip = False
    for user_input, response in chat_history:
        user_input = user_input.strip() if do_strip else user_input
        do_strip = True
        texts.append(f'{user_input} [/INST] {response.strip()} </s><s>[INST] ')
    message = message.strip() if do_strip else message
    texts.append(f'{message} [/INST]')
    return ''.join(texts)


def get_available_backends(url="https://api.pixelyai.com/api/gradio/"):
    result = subprocess.run(
        ['curl', '-X', 'GET', f'{url}', '-H', "accept: application/json"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    ).stdout.decode('utf-8')
    print(result)
    return json.loads(result)


def set_available_backend(url_backend: str, url="https://api.pixelyai.com/api/gradio/", method='put'):
    assert method in ['put', 'delete']
    result = subprocess.run(
        ['curl', '-X', 'POST', f'{url}', '-H', "accept: application/json", '-H', 'Content-Type: application/json',
         '-d', '{'
               f'"url":"{url_backend}",'
               f'"method":"{method}"'
               '}'],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    ).stdout.decode('utf-8')
    return json.loads(result)


def delete_all_of_the_backends(url="https://api.pixelyai.com/api/gradio/"):
    for i in get_available_backends(url=url)['available_backends']:
        _ = set_available_backend(i, method='delete')
        print(f'{i} Deleted Successfully')


def remove_deprecated_backends(url: str = "https://api.pixelyai.com/api/gradio/"):
    for url_backend in get_available_backends(url=url)['available_backends']:
        try:
            client = gc.Client(url_backend, verbose=False)
        except ValueError:
            print(f'URL : {url_backend} is deprecated [REMOVING]')
            set_available_backend(url_backend=url_backend, method='delete', url=url)
    return get_available_backends(url=url)


def ai_client(
        prompt: str,
        url_client: str,
        conversation_history: List[dict] = None,
        contexts=None,
        debug: bool = False,
        max_new_tokens: int = 1024
):
    if conversation_history is None:
        conversation_history = []
    history = format_chat_for_ai_client(
        user=[f['user'] for f in conversation_history],
        assistance=[f['assistance'] for f in conversation_history]
    )
    is_found, generated_response, client = False, None, gc.Client(url_client, verbose=False, max_workers=128)
    if isinstance(contexts, list):
        if len(contexts) == 0:
            contexts = None
    if contexts is not None:
        for context in contexts:
            instruct_check = (
                "\nContext =>\n{context}\nQuestion => \n"
                'can you answer to question ("{question}") only and only by using the provided context?\n'
                'if the question is not related to context or not about the context you have to response NO'
            )

            gprs_func = functools.partial(
                client.predict,
                instruct_check.format(question=prompt, context=context),  # str in 'Message Box' Textbox component
                "",  # str in 'UserId' Textbox component
                history,  # str in 'Data' Textbox component
                "you will be given a context and a question try to answer as good as possible and only use context"
                "provided information",  # str in 'System' Textbox component
                64,  # int | float (numeric value between 64 and 10000) in 'Max New Tokens' Slider component
                False,
            )

            generated_response = gprs_func(fn_index=0)[-1]
            # generated_response_tokens = gprs_func(fn_index=4)
            is_found = in_check(generated_response, prompt)
            if debug:
                print(generated_response)
                print(is_found)
            if is_found:
                grf_func = functools.partial(
                    client.predict,
                    prompt,  # str in 'Message Box' Textbox component
                    "",  # str in 'UserId' Textbox component
                    f"Here's Extra information:\n{context}{END_OF_MESSAGE_TURN_HUMAN}Great, thank you for providing me with this "
                    f"additional information.",  # str in 'Data' Textbox component
                    FOUND_SYSTEM_MESSAGE
                    ,  # str in 'System' Textbox component
                    max_new_tokens,
                    # int | float (numeric value between 64 and 10000) in 'Max New Tokens' Slider component
                    False,
                )
                generated_response = grf_func(fn_index=0)[-1]
                # generated_response_tokens = grf_func(fn_index=4)

                break
        if not is_found:
            nfgr_response = functools.partial(
                client.predict,
                prompt,  # str in 'Message Box' Textbox component
                "",  # str in 'UserId' Textbox component
                history,  # str in 'Data' Textbox component
                DEFAULT_SYSTEM_PROMPT,  # str in 'System' Textbox component
                max_new_tokens,  # int | float (numeric value between 64 and 10000) in 'Max New Tokens' Slider component
                False,
            )
            generated_response = nfgr_response(fn_index=0)[-1]
            # generated_response_tokens = nfgr_response(fn_index=4)

    else:
        gr_func = functools.partial(
            client.predict,
            prompt,  # str in 'Message Box' Textbox component
            "",  # str in 'UserId' Textbox component
            history,  # str in 'Data' Textbox component
            DEFAULT_SYSTEM_PROMPT,  # str in 'System' Textbox component
            max_new_tokens,  # int | float (numeric value between 64 and 10000) in 'Max New Tokens' Slider component
            False,
        )
        generated_response = gr_func(fn_index=0)[-1]
        # generated_response_tokens = gr_func(fn_index=4)

        is_found = False
    return generated_response, is_found


def ai_client_token_counter(
        prompt: str,
        url_client: str,
        conversation_history: List[dict] = None,
        contexts=None,
        max_new_tokens: int = 1024,
        **kwargs
):
    possibilities = []
    if conversation_history is None:
        conversation_history = []
    history = format_chat_for_ai_client(
        user=[f['user'] for f in conversation_history],
        assistance=[f['assistance'] for f in conversation_history]
    )
    is_found, generated_response, client = False, None, gc.Client(url_client, verbose=False, max_workers=128)
    if isinstance(contexts, list):
        if len(contexts) == 0:
            contexts = None
    if contexts is not None:
        for context in contexts:
            instruct_check = (
                "\nContext =>\n{context}\nQuestion => \n"
                'can you answer to question ("{question}") only and only by using the provided context?\n'
                'if the question is not related to context or not about the context you have to response NO'
            )

            gprs_func = functools.partial(
                client.predict,
                instruct_check.format(question=prompt, context=context),  # str in 'Message Box' Textbox component
                "",  # str in 'UserId' Textbox component
                history,  # str in 'Data' Textbox component
                "you will be given a context and a question try to answer as good as possible and only use context"
                "provided information",  # str in 'System' Textbox component
                64,  # int | float (numeric value between 64 and 10000) in 'Max New Tokens' Slider component
                False,
            )
            possibilities.append(gprs_func(fn_index=4))

            grf_func = functools.partial(
                client.predict,
                prompt,  # str in 'Message Box' Textbox component
                "",  # str in 'UserId' Textbox component
                f"Here's Extra information:\n{context}{END_OF_MESSAGE_TURN_HUMAN}Great, thank you for providing me with this "
                f"additional information.",  # str in 'Data' Textbox component
                FOUND_SYSTEM_MESSAGE
                ,  # str in 'System' Textbox component
                max_new_tokens,
                # int | float (numeric value between 64 and 10000) in 'Max New Tokens' Slider component
                False,
            )

            possibilities.append(grf_func(fn_index=4))

        nfgr_response = functools.partial(
            client.predict,
            prompt,  # str in 'Message Box' Textbox component
            "",  # str in 'UserId' Textbox component
            history,  # str in 'Data' Textbox component
            DEFAULT_SYSTEM_PROMPT,  # str in 'System' Textbox component
            max_new_tokens,  # int | float (numeric value between 64 and 10000) in 'Max New Tokens' Slider component
            False,
        )
        possibilities.append(nfgr_response(fn_index=4))

    gr_func = functools.partial(
        client.predict,
        prompt,  # str in 'Message Box' Textbox component
        "",  # str in 'UserId' Textbox component
        history,  # str in 'Data' Textbox component
        DEFAULT_SYSTEM_PROMPT,  # str in 'System' Textbox component
        max_new_tokens,  # int | float (numeric value between 64 and 10000) in 'Max New Tokens' Slider component
        False,
    )

    possibilities.append(gr_func(fn_index=4))

    return set(sorted(possibilities))
