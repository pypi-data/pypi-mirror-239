from discord.ext import commands

class OnMessage(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
    
    @commands.Cog.listener()
    async def on_message(self, message) -> None:
        user_function = self.client.callables["on_message"]
        
        if user_function is None:
            return
    
        if message.author == self.client.user:
            return

        try:
            response = user_function(message)

            if response is None:
                return

            await message.channel.send(response)

        except Exception as e:
            error_type = type(e).__name__
            self.client.logger.error(f"{error_type} in function '{user_function.__name__}': {e}")

# add cog extension to "client" (the bot)
# NOTE: THIS CODE RUNS FROM THE DIRECTORY THAT "main.py" IS IN
async def setup(client):
    await client.add_cog(OnMessage(client))