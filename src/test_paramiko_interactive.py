import paramiko


def handler(title, instructions, prompt_list):
    print("TITLE:", repr(title))
    print("INSTR:", repr(instructions))

    responses = []

    for prompt, echo in prompt_list:
        print("PROMPT:", repr(prompt), echo)

        if "password" in prompt.lower():
            responses.append("YOUR_PASSWORD")      # <-- Replace with the actual password
        else:
            responses.append("")

    return responses


client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

transport = None

try:
    client.connect(
        hostname="172.29.1.59",
        username="root",
        password=None,
        allow_agent=False,
        look_for_keys=False,
    )

except paramiko.BadAuthenticationType as e:
    print("Allowed:", e.allowed_types)

    transport = client.get_transport()

    transport.auth_interactive(
        "root",
        handler,
    )

    print("AUTH SUCCESS")

    channel = transport.open_session()
    channel.get_pty()
    channel.invoke_shell()

    print(channel.recv(65535).decode())

except Exception as e:
    print(type(e), e)
