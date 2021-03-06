from main import bot
from discord.ext import commands
from services.cat.api import get_cat_image
from services.hug.utils import remove_invocation, find_user, InvalidUserException
from services.config import CONFIG


# TODO Implement error handling for cat commands
class Wholesome(commands.Cog):
    """
        A collection of wholesome commands intended to spread happy feelings
    """

    @bot.group(
        invoke_without_command=True,
        enabled = CONFIG["commands"]["cat"]["enabled"]
    )
    async def cat(self, ctx):
        """
            Post a random image or gif of a cat from https://cataas.com
        """
        async with ctx.typing():
            cat = await get_cat_image()

        await ctx.send(file=cat)

    @cat.command(
        enabled = CONFIG["commands"]["cat"]["enabled"]
    )
    async def gif(self, ctx):
        """
            Post a random gif of a cat from https://cataas.com
        """
        async with ctx.typing():
            cat = await get_cat_image(gif=True)

        await ctx.send(file=cat)

    @commands.before_invoke(remove_invocation)
    @commands.command(
        enabled = CONFIG["commands"]["hug"]["enabled"]
    )
    async def hug(self, ctx, target):
        """
            Send a virtual hug to someone
        """
        try:
            user = await find_user(ctx.guild, target)
            await ctx.send(f"{user.mention} {ctx.message.author.name} sent you a virtual hug! :heart:")
        except InvalidUserException:
            await ctx.send(f'User not found. Check that the user is valid.```{ctx.message.content}```')
        except Exception as e:
            print(e)
