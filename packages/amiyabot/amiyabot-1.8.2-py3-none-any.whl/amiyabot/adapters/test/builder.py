import base64

from amiyabot.builtin.messageChain import Chain
from amiyabot.builtin.messageChain.element import *
from amiyabot import log


async def build_message_send(chain: Chain, custom_chain: Optional[CHAIN_LIST] = None):
    chain_list = custom_chain or chain.chain
    chain_data = []
    voice_list = []

    if chain_list:
        for item in chain_list:
            # At
            if isinstance(item, At):
                chain_data.append({'type': 'text', 'data': f'@{chain.data.nickname}'})

            # AtAll
            if isinstance(item, AtAll):
                chain_data.append({'type': 'text', 'data': '@All'})

            # Face
            if isinstance(item, Face):
                chain_data.append({'type': 'text', 'data': f'[{item.face_id}]'})

            # Text
            if isinstance(item, Text):
                chain_data.append({'type': 'text', 'data': item.content})

            # Image
            if isinstance(item, Image):
                img = await item.get()
                chain_data.append({'type': 'image', 'data': await append_image(img)})

            # Voice
            if isinstance(item, Voice):
                voice_list.append(send_msg([{'type': 'text', 'data': '[voice]'}]))

            # Html
            if isinstance(item, Html):
                result = await item.create_html_image()
                if result:
                    chain_data.append({'type': 'image', 'data': await append_image(result)})

    return send_msg(chain_data), voice_list


async def append_image(img: Union[bytes, str]):
    if isinstance(img, bytes):
        img = 'data:image/png;base64,' + base64.b64encode(img).decode()
    return img


def send_msg(chain_data: list):
    return json.dumps({'event': 'message', 'event_data': chain_data}, ensure_ascii=False)
