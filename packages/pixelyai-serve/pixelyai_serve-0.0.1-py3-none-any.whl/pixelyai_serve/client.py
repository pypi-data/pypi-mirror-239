from lib.python.pixelyai_serve.serving import utils


def main():
    print(utils.ai_client_token_counter(
        'who donald trump?',
        contexts=[
            open('dummy-data/metavers-ae.md', 'r').read()
        ],
        max_new_tokens=512,
        url_client=utils.get_available_backends()['available_backends'][-1],
        debug=True
    ))


if __name__ == "__main__":
    main()
