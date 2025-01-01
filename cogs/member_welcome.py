# cogs/member_welcome.py
import discord
from discord.ext import commands
from config import GUILD_ID, CHANNEL_ID, TARGET_MEMBER_COUNT
from database import record_member_join

class MemberWelcomeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild = self.bot.get_guild(GUILD_ID)
        channel = guild.get_channel(CHANNEL_ID)

        if guild is not None and channel is not None:
            remaining_members = TARGET_MEMBER_COUNT - len(guild.members)
            await channel.send(
                f"ようこそ {member.mention} さん！現在のメンバー数: {len(guild.members)}人。\n"
                f"あと {remaining_members} 人で {TARGET_MEMBER_COUNT}人達成です！"
            )

        join_date = member.joined_at.strftime('%Y-%m-%d %H:%M:%S')
        record_member_join(member.id, join_date)

        # 1000人超えたらお祝い
        if len(guild.members) >= TARGET_MEMBER_COUNT:
            await self.celebrate_1000_members(guild, channel)

    async def celebrate_1000_members(self, guild, channel):
        await channel.send(
            f"🎉🎉🎉 {TARGET_MEMBER_COUNT}人達成！🎉🎉🎉\n"
            f"{guild.name}のメンバーが{TARGET_MEMBER_COUNT}人になりました！皆さんありがとうございます！"
        )

    @commands.command(name='1000')
    async def member_count_command(self, ctx):
        """現在のメンバー数を表示。"""
        guild = ctx.guild
        if guild:
            remaining_members = TARGET_MEMBER_COUNT - len(guild.members)
            await ctx.send(
                f"現在のメンバー数: {len(guild.members)}人。\n"
                f"あと {remaining_members} 人で {TARGET_MEMBER_COUNT}人達成です！"
            )
        else:
            await ctx.send("このコマンドはサーバー内でのみ使用できます。")

    @commands.command(name='progress')
    async def progress_command(self, ctx):
        """1000人達成までの進捗率を表示。"""
        guild = ctx.guild
        if guild:
            current_member_count = len(guild.members)
            progress_percentage = (current_member_count / TARGET_MEMBER_COUNT) * 100
            await ctx.send(f"{TARGET_MEMBER_COUNT}人達成までの現在の進捗率: {progress_percentage:.2f}%")
        else:
            await ctx.send("このコマンドはサーバー内でのみ使用できます。")

async def setup(bot: commands.Bot):
    await bot.add_cog(MemberWelcomeCog(bot))
