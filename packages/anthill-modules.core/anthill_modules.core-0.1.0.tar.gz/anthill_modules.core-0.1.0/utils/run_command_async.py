import asyncio


async def run_command_async(command):
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()

    if stdout:
        return stdout.decode()
    elif stderr:
        return stderr.decode()
    else:
        return None
