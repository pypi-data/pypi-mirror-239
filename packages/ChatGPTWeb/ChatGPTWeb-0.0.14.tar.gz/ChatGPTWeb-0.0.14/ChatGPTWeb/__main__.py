from ChatGPTWeb import chatgpt
from ChatGPTWeb.config import MsgData,Personality
import asyncio
import aioconsole

session_token=[
    ""
]

personality_definition = Personality(
    [
        {
            "name":"one",
            'value':'one value'
            },
        {
            "name":"two",
            "value":'two value'
        }
        ])

proxy = {
    "http":"http://127.0.0.1:1090",
    "https":"https://127.0.0.1:1090"
}
proxy = {"server": "http://127.0.0.1:1090"}
chat = chatgpt(session_token=session_token,proxy=proxy,headless=False,begin_sleep_time=False)
#,log_status=False
async def main():
    
    c_id = await aioconsole.ainput("your conversation_id if you have:")
    p_id = await aioconsole.ainput("your parent_message_id if you have:")
    data:MsgData = MsgData(conversation_id=c_id,p_msg_id=p_id)
    while 1:
        print("\n------------------------------")
        data.msg_send = await aioconsole.ainput("input：")
        print("------------------------------\n")
        if data.msg_send == "quit":
            break
        elif data.msg_send == "re":
            data.msg_type = "back_loop"
            data.p_msg_id = await aioconsole.ainput("your parent_message_id if you go back:")
        elif data.msg_send == "reset":
            data = await chat.back_init_personality(data)
            print(f"ChatGPT:{data.msg_recv}")
            continue
        elif data.msg_send == "init_personality":
            data.msg_send = "your ..."
            data = await chat.init_personality(data)
            print(f"ChatGPT:{data.msg_recv}")
            continue
        elif data.msg_send == "history":
            print(await chat.show_chat_history(data))
            continue
        data = await chat.continue_chat(data)
        print(f"ChatGPT:{data.msg_recv}")
        
        
loop = asyncio.get_event_loop()
loop.run_until_complete(main())           
    