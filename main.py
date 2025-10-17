import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button
import json
import os
import random

intents = discord.Intents.all()
intents.members = True 
bot = commands.Bot(command_prefix="+", intents=intents,help_command=None)
tree = bot.tree

# --------------------------------------------------------------------------------------------------------------------------------------------
CONFIG_FILE = "data.json"

if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "w") as f:
        json.dump({}, f)

def load_configs():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_configs():
    with open(CONFIG_FILE, "w") as f:
        json.dump(configs, f, indent=4)
        print("✅ data.json sauvegardé avec succès.")

configs = load_configs()


class WelcomeConfig:
    def __init__(self, welcome_channel_id=None, goodbye_channel_id=None):
        self.welcome_channel_id = welcome_channel_id
        self.goodbye_channel_id = goodbye_channel_id

    def to_dict(self):
        return {
            "welcome_channel_id": self.welcome_channel_id,
            "goodbye_channel_id": self.goodbye_channel_id
        }

    @staticmethod
    def from_dict(data):    
        return WelcomeConfig(
            welcome_channel_id=data.get("welcome_channel_id"),
            goodbye_channel_id=data.get("goodbye_channel_id")
        )
class GreetConfig:
    def __init__(self, greet_channel_id=None):
        self.greet_channel_id = greet_channel_id

    def to_dict(self):
        return {
            "greet_channel_id": self.greet_channel_id
        }

    @staticmethod
    def from_dict(data):    
        return GreetConfig(
            greet_channel_id=data.get("greet_channel_id")
        )
    
    
@bot.event
async def on_ready():
    await bot.wait_until_ready()
    print(f"[+] Connecté en tant que {bot.user}")
    await tree.sync()
    print("✅ Slash commands prêtes !")
    bot.add_view(TicketView())

    activity = discord.Streaming(
    name="with nakken",
    url="https://twitch.tv/xlookup",
    )
    await bot.change_presence(activity=activity, status=discord.Status.online)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return


    if "t.me/" in message.content:
        if hasattr(message.author, "guild_permissions") and message.author.guild_permissions.administrator:
            return
        try:
            await message.delete()
            await message.channel.send(f"{message.author.mention} **[-] les liens d'invitation Discord ne sont pas autorisés.**")
        except discord.Forbidden:
            pass
    if "discord.gg" in message.content:
        if hasattr(message.author, "guild_permissions") and message.author.guild_permissions.administrator:
            return
        try:
            await message.delete()
            await message.channel.send(f"{message.author.mention} **[-] les liens d'invitation Discord ne sont pas autorisés.**")
        except discord.Forbidden:
            pass
    await bot.process_commands(message)

    if "discordapp.com" in message.content:
        if hasattr(message.author, "guild_permissions") and message.author.guild_permissions.administrator:
            return

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("[-] Vous n'avez pas la permission d'utiliser cette commande.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("[-] Commande non trouvée.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("[-] Argument manquant pour cette commande.")
    else:
        await ctx.send(f"[-] Une erreur est survenue : {str(error)}")
@bot.event
async def on_member_join(member: discord.Member):
    guild_id = str(member.guild.id)
    config_data = configs.get(guild_id, {}).get("welcome")
    if config_data:
        config = WelcomeConfig.from_dict(config_data)
        if config.welcome_channel_id:
            channel = bot.get_channel(config.welcome_channel_id)
            if channel:
                embed = discord.Embed(
                    title=f"Bienvenue {member.display_name} dans le serveur **{member.guild.name}**",
                    description=f" N'oublie pas de lire le règlement ! \nL'équipe de **{member.guild.name}** reste à ta disposition pour tout renseignement.",
                    color=discord.Color(0x4F00B4)
                )
                embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
                embed.set_footer(text="xProtect | by nakken_")
                await channel.send(embed=embed)
    greet_list = configs.get(guild_id, {}).get("greet", [])
    for channel_id in greet_list:
        greet_channel = bot.get_channel(channel_id)
        if greet_channel:
            ping_message = f"{member.mention}"
            sent_message = await greet_channel.send(ping_message)
            await sent_message.delete()
@bot.event
async def on_member_remove(member: discord.Member):
    guild_id = str(member.guild.id)
    config_data = configs.get(guild_id, {}).get("welcome")
    if config_data:
        config = WelcomeConfig.from_dict(config_data)
        if config.goodbye_channel_id:
            channel = bot.get_channel(config.goodbye_channel_id)
            if channel:
                embed = discord.Embed(
                    title=f"{member.display_name} a quitté le serveur.",
                    description=f"A bientôt {member.display_name}...",
                    color=discord.Color(0x4F00B4)
                )
                embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
                embed.set_footer(text="xProtect | by nakken_")
                await channel.send(embed=embed)

@tree.command(name="help", description="affiche la liste des commandes slash.")
@app_commands.describe()
async def help_command(interaction: discord.Interaction):
    
    embed = discord.Embed(title="Liste des commandes slash disponibles", color=0x4F00B4)
    embed.add_field(name="/setup_welcome", value="Configurer les salons de bienvenue et de départ.", inline=False)
    embed.add_field(name="/setup_greet", value="Configurer les salons à ping lorsqu'un membre rejoint le serveur.", inline=False)
    embed.add_field(name="/setup_ticket", value="Configurer le système de tickets.", inline=False)
    embed.add_field(name="/delete_greet", value="Supprimer la configuration du salon de greet.", inline=False)
    embed.add_field(name="/delete_all_greet", value="Supprimer la configuration de tous les salons de greet.", inline=False)
    embed.add_field(name="/show_all_greet", value="Afficher tous les salons de greet configurés.", inline=False)
    embed.add_field(name="/help", value="Afficher cette liste d'aide.", inline=False)
    embed.add_field(name="+help", value="Affiche les commandes restantes.", inline=False)
    embed.set_footer(text="xProtect | by nakken_")
    await interaction.response.send_message(embed=embed, ephemeral=True)
    
@tree.command(name="setup_welcome", description="Configurer les salons de bienvenue et de départ")
@app_commands.describe(
    welcome_channel="Salon pour les messages de bienvenue",
    goodbye_channel="Salon pour les messages de départ"
)
async def setupwelcome(interaction: discord.Interaction, welcome_channel: discord.TextChannel, goodbye_channel: discord.TextChannel):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("[-] Seuls les administrateurs peuvent utiliser cette commande.", ephemeral=True)
        return
    guild_id = str(interaction.guild_id)
    configs[guild_id] = configs.get(guild_id, {})
    configs[guild_id]["welcome"] = WelcomeConfig(welcome_channel.id, goodbye_channel.id).to_dict()
    save_configs()
    await interaction.response.send_message(
        f"**[+] Configuration enregistrée :**\nBienvenue → {welcome_channel.mention}\nDépart → {goodbye_channel.mention}",
        ephemeral=True
    )

@tree.command(name="setup_greet", description="Configurer les salons à ping lorsqu'un membre rejoint le serveur")
@app_commands.describe(
    greet_channel="Salon à ajouter à la liste des salons à ping lorsqu'un membre rejoint le serveur",
)
async def setup_greet(interaction: discord.Interaction, greet_channel: discord.TextChannel):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("[-] Seuls les administrateurs peuvent utiliser cette commande.", ephemeral=True)
        return
    guild_id = str(interaction.guild_id)
    configs[guild_id] = configs.get(guild_id, {})
    greet_list = configs[guild_id].get("greet", [])

    if not greet_list:
        greet_list = []
    if greet_channel.id not in greet_list:
        greet_list.append(greet_channel.id)
        configs[guild_id]["greet"] = greet_list
        save_configs()
        await interaction.response.send_message(
            f"**[+] Salon ajouté à la liste des greet :** {greet_channel.mention}",
            ephemeral=True
        )
    else:
        await interaction.response.send_message(
            f"[-] Ce salon est déjà dans la liste des greet.",
            ephemeral=True
        )

@tree.command(name="delete_greet", description="Supprimer la configuration du salon de greet")
@app_commands.describe(
    greet_channel="Salon à supprimer de la configuration"
)
async def delete_greet(interaction: discord.Interaction, greet_channel: discord.TextChannel):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("[-] Seuls les administrateurs peuvent utiliser cette commande.", ephemeral=True)
        return
    guild_id = str(interaction.guild_id)
    if guild_id in configs and "greet" in configs[guild_id]:
        del configs[guild_id]["greet"][greet_channel.id]
        save_configs()
        await interaction.response.send_message(
            f"**[+] Configuration supprimée pour le salon :** {greet_channel.mention}",
            ephemeral=True
        )
    else:
        await interaction.response.send_message(
            "[-] Aucune configuration de greet trouvée pour ce serveur.",
            ephemeral=True
        )
@tree.command(name="delete_all_greet", description="Supprimer la configuration de tous les salons de greet")
@app_commands.describe()
async def delete_all_greet(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("[-] Seuls les administrateurs peuvent utiliser cette commande.", ephemeral=True)
        return
    guild_id = str(interaction.guild_id)
    if guild_id in configs and "greet" in configs[guild_id]:
        del configs[guild_id]["greet"]
        save_configs()
        await interaction.response.send_message(
            "**[+] Tout les greet ont été supprimés.**",
            ephemeral=True
        )
    else:
        await interaction.response.send_message(
            "[-] Aucune configuration de greet trouvée pour ce serveur.",
            ephemeral=True
        )

@tree.command(name="giveaway", description="Créer un giveaway dans le salon actuel.")
@app_commands.describe(
    prize="Le prix du giveaway",
    duration="La durée du giveaway",
    unité="Unité de temps pour la durée",
    winners="Le nombre de gagnants"
)
async def giveaway(interaction: discord.Interaction, prize: str, duration: int, unité: str, winners: int):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("[-] Seuls les administrateurs peuvent utiliser cette commande.", ephemeral=True)
        return

    if unité not in ["secondes", "minutes", "heures", "jours"]:
        await interaction.response.send_message("[-] Unité de temps invalide. Utilisez 'secondes', 'minutes', 'heures' ou 'jours'.", ephemeral=True)
        return

    time_multipliers = {
        "secondes": 1,
        "minutes": 60,
        "heures": 3600,
        "jours": 86400
    }
    total_seconds = duration * time_multipliers[unité]

    embed = discord.Embed(
        title="⚡️ Giveaway ⚡️",
        description=f"**Prix :** {prize}\n**Durée :** {duration} {unité}\n**Nombre de gagnants :** {winners}\n\nRéagissez avec 🎉 pour participer !",
        color=0x4F00B4
    )
    embed.set_footer(text="xProtect | by nakken_")
    giveaway_message = await interaction.channel.send(embed=embed)
    await giveaway_message.add_reaction("⚡️")

    await interaction.response.send_message("**[+] Giveaway créé avec succès !**", ephemeral=True)

    await discord.utils.sleep_until(discord.utils.utcnow() + discord.timedelta(seconds=total_seconds))

    giveaway_message = await interaction.channel.fetch_message(giveaway_message.id)
    users = set()
    for reaction in giveaway_message.reactions:
        if str(reaction.emoji) == "⚡️":
            async for user in reaction.users():
                if not user.bot:
                    users.add(user)

    if len(users) == 0:
        await interaction.channel.send("[-] Personne n'a participé au giveaway.")
        return

    winners_list = random.sample(users, min(winners, len(users)))
    winner_mentions = ", ".join(winner.mention for winner in winners_list)

    await interaction.channel.send(f"🎉 Félicitations {winner_mentions} ! Vous avez gagné **{prize}** ! 🎉")





@tree.command(
    name="delete_giveaway",
    description="Supprimer un giveaway en cours dans le salon actuel. (Administrateur uniquement)"
)
@app_commands.describe(
    message_id="L'ID du message du giveaway à supprimer"
)
async def delete_giveaway(interaction: discord.Interaction, message_id: str):
    """Supprime un message de giveaway en fonction de son ID."""
    
    # Vérification des permissions
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message(
            "[-] Seuls les administrateurs peuvent utiliser cette commande.",
            ephemeral=True
        )

    try:
        # Tentative de conversion de l’ID en entier
        message_id_int = int(message_id)

        # Récupération du message
        giveaway_message = await interaction.channel.fetch_message(message_id_int)

        # Suppression du message
        await giveaway_message.delete()
        await interaction.response.send_message(
            "**[+] Giveaway supprimé avec succès !**",
            ephemeral=True
        )

    except ValueError:
        await interaction.response.send_message(
            "[-] L'ID du message doit être un nombre valide.",
            ephemeral=True
        )

    except discord.NotFound:
        await interaction.response.send_message(
            "[-] Message de giveaway non trouvé.",
            ephemeral=True
        )

    except discord.Forbidden:
        await interaction.response.send_message(
            "[-] Je n'ai pas la permission de supprimer ce message.",
            ephemeral=True
        )

    except Exception as e:
        await interaction.response.send_message(
            f"[-] Une erreur est survenue : `{e}`",
            ephemeral=True
        )

@tree.command()
@app_commands.describe()
async def show_all_greet(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("[-] Seuls les administrateurs peuvent utiliser cette commande.", ephemeral=True)
        return
    guild_id = str(interaction.guild_id)
    greet_list = configs.get(guild_id, {}).get("greet", [])
    
    if not greet_list:
        await interaction.response.send_message("[-] Aucune configuration de greet trouvée pour ce serveur.", ephemeral=True)
        return

    greet_channels = [f"<#{channel_id}>" for channel_id in greet_list if bot.get_channel(channel_id)]
    
    if not greet_channels:
        await interaction.response.send_message("[-] Aucun salon de greet configuré.", ephemeral=True)
        return

    embed = discord.Embed(title="Salons de Greet Configurés", description="\n".join(greet_channels), color=0x4F00B4)
    embed.set_footer(text="xProtect | by nakken_")
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.command()
async def help(ctx):
    if ctx.author.guild_permissions.administrator:
        embed = discord.Embed(title="Commandes ADMIN disponibles", description="", color=0x4F00B4)
        embed.set_footer(text="xProtect | Dev by nakken")
        embed.add_field(name="+clear", value="1-Supprime les messages du salon actuel et duplique les permissions.", inline=False)
        embed.add_field(name="+close", value="2-Supprime le salon actuel.", inline=False)
        embed.add_field(name="+lock", value="3-Verrouille le salon actuel.", inline=False)
        embed.add_field(name="+unlock", value="4-Déverrouille le salon actuel.", inline=False)
        embed.add_field(name="+show", value="5-Rend le salon visible.", inline=False)
        embed.add_field(name="+hide", value="6-Rend le salon invisible.", inline=False)
        embed.add_field(name="+ban <@membre>", value="7-Bannit un membre du serveur.", inline=False)
        embed.add_field(name="+mute <@membre>", value="8-mute un membre du serveur.", inline=False)
        embed.add_field(name="+unmute <@membre>", value="9-unmute un membre du serveur.", inline=False)
        embed.add_field(name="+tempmute <@membre>", value="10-mute un membre du serveur pendant une certaine durée.", inline=False)
        embed.add_field(name="+vip <@membre>", value="11-Donne le rôle VIP à un membre.", inline=False)
        embed.add_field(name="+unvip <@membre>", value="12-Enlève le rôle VIP à un membre.", inline=False)
        embed.add_field(name="+delete <nombre>", value="13-supprime un nombre de messages dans le channel.", inline=False)
        embed.add_field(name="/help", value="14-affiche la liste des commandes slash.", inline=False)
        embed.color = 0x4F00B4
        await ctx.send(embed=embed)
        await ctx.send("https://imgur.com/a/9HzTBme")
    else:
        await ctx.send("[-] Vous n'avez pas la permission admin.")


# --------------------------------------------------------------------------------------------------------------------------------------------

@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    embed = discord.Embed(title="Ping test", description=f"Latence: {latency} ms", color=0x4F00B4
)
    await ctx.send(embed=embed)


@bot.command()
async def clear(ctx):
    if ctx.author.guild_permissions.manage_messages:
        channel = ctx.channel
        new_channel = await channel.clone()
        await channel.delete()
        await new_channel.send("**[+] Clear effectué.**")
    else:
        await ctx.send("[-] Vous n'avez pas la permission de gérer les messages.")

@bot.command()
async def close(ctx):
    if ctx.author.guild_permissions.manage_messages:
        channel = ctx.channel
        await channel.delete()
    else:
        await ctx.send("[-] Vous n'avez pas la permission de gérer les messages.")

@bot.command()
async def lock(ctx):
    if ctx.author.guild_permissions.manage_channels:
        channel = ctx.channel
        role = ctx.guild.default_role
        await channel.set_permissions(role, send_messages=False)
        await ctx.send("**[+] Le salon est maintenant verrouillé.**")
    else:
        await ctx.send("[-] Vous n'avez pas la permission de gérer les salons.")

@bot.command()
async def unlock(ctx):
    if ctx.author.guild_permissions.manage_channels:
        channel = ctx.channel
        role = ctx.guild.default_role
        await channel.set_permissions(role, send_messages=True)
        await ctx.send("**[+] Le salon est maintenant déverrouillé.**")
    else:
        await ctx.send("[-] Vous n'avez pas la permission de gérer les salons.")

@bot.command()
async def show(ctx):
    if ctx.author.guild_permissions.manage_channels:
        channel = ctx.channel
        role = ctx.guild.default_role
        await channel.set_permissions(role, view_channel=True)
        await ctx.send("**[+] Le salon est maintenant visible.**")
    else:
        await ctx.send("[-] Vous n'avez pas la permission de gérer les salons.")

@bot.command()
async def hide(ctx):
    if ctx.author.guild_permissions.manage_channels:
        channel = ctx.channel
        role = ctx.guild.default_role
        await channel.set_permissions(role, view_channel=False)
        await ctx.send("**[+] Le salon est maintenant invisible.**")
    else:
        await ctx.send("[-] Vous n'avez pas la permission de gérer les salons.")


@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    if ctx.author.guild_permissions.ban_members:
        await member.ban(reason=reason)
        await ctx.send(f"**[+] {member.name} a été banni.**")
    else:
        await ctx.send("[-] Vous n'avez pas la permission de bannir des membres.")


@bot.command()
async def mute(ctx, member: discord.Member):
    if ctx.author.guild_permissions.manage_roles:
        mute_role = discord.utils.get(ctx.guild.roles, name="[!] Muted")
        if not mute_role:
            mute_role = await ctx.guild.create_role(name="[!] Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(mute_role, speak=False, send_messages=False, read_message_history=True)
        await member.add_roles(mute_role)
        await ctx.send(f"**[+] {member.name} ne peut plus parler.**")
    else:
        await ctx.send("[-] Vous n'avez pas la permission de gérer les rôles.")

@bot.command()
async def unmute(ctx, member: discord.Member):
    if ctx.author.guild_permissions.manage_roles:
        mute_role = discord.utils.get(ctx.guild.roles, name="[!] Muted")
        if mute_role in member.roles:
            await member.remove_roles(mute_role)
            await ctx.send(f"**[+] {member.name} peut à nouveau parler.**")
        else:
            await ctx.send("[-] Le membre n'est pas muté.")

@bot.command()
async def tempmute(ctx, member: discord.Member, duration: int):
    if ctx.author.guild_permissions.manage_roles:
        mute_role = discord.utils.get(ctx.guild.roles, name="[!] Muted")
        if not mute_role:
            mute_role = await ctx.guild.create_role(name="[!] Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(mute_role, speak=False, send_messages=False, read_message_history=True)
        await member.add_roles(mute_role)
        await ctx.send(f"**[+] {member.name} est mute pour {duration} minutes.**")
        await discord.utils.sleep_until(discord.utils.utcnow() + discord.timedelta(minutes=duration))
        await member.remove_roles(mute_role)
        await ctx.send(f"**[+] {member.name} n'est plus mute.**")
    else:
        await ctx.send("[-] Vous n'avez pas la permission de gérer les rôles.")

@bot.command()
async def vip(ctx, member: discord.Member):
    if ctx.author.guild_permissions.manage_roles:
        vip_role = discord.utils.get(ctx.guild.roles, name="VIP")
        if not vip_role:
            vip_role = await ctx.guild.create_role(name="VIP")
        await member.add_roles(vip_role)
        await ctx.send(f"**[+] {member.name} a été promu VIP.**")
    else:
        await ctx.send("[-] Vous n'avez pas la permission de gérer les rôles.")

@bot.command()
async def unvip(ctx, member: discord.Member):
    if ctx.author.guild_permissions.manage_roles:
        vip_role = discord.utils.get(ctx.guild.roles, name="VIP")
        if vip_role in member.roles:
            await member.remove_roles(vip_role)
            await ctx.send(f"**[+] {member.name} n'est plus VIP.**")
        else:
            await ctx.send("[-] Le membre n'est pas VIP.")
    else:
        await ctx.send("[-] Vous n'avez pas la permission de gérer les rôles.")
@bot.command()
async def delete(ctx, *, nb: int = 1):
    if ctx.author.guild_permissions.manage_messages:
        if nb < 1 or nb > 100:
            await ctx.send("[-] Vous devez spécifier un nombre entre 1 et 100.")
            return
        deleted = await ctx.channel.purge(limit=nb + 1)
        await ctx.send(f"**[+] {len(deleted) - 1} messages supprimés.**", delete_after=5)
    else:
        await ctx.send("[-] Vous n'avez pas la permission de gérer les messages.")

@tree.command(name="say", description="Fait parler le bot dans le salon actuel.")
@app_commands.describe(message="Le message que le bot doit envoyer")
async def say(interaction: discord.Interaction, message: str):
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message("[-] Vous n'avez pas la permission de gérer les messages.", ephemeral=True)
        return
    await interaction.channel.send(message)
    await interaction.response.send_message("[+] Message envoyé.", ephemeral=True)

@tree.command(name="setup_ticket", description="Configurer le système de tickets.")
@app_commands.describe(
    category="La catégorie où seront créés les tickets",
    staff_roles="Les rôles staff autorisés (IDs séparés par des espaces, ne rien entrer pour aucun rôle)",
    channel="Le salon où envoyer le bouton"
)
async def setup_ticket(interaction: discord.Interaction, category: discord.CategoryChannel, channel: discord.TextChannel, staff_roles: str):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("[-] Seuls les administrateurs peuvent utiliser cette commande.", ephemeral=True)
        return
    guild_id = str(interaction.guild_id)
    role_ids = [int(rid) for rid in staff_roles.split() if rid.isdigit()]
    
    configs[guild_id] = configs.get(guild_id, {})
    configs[guild_id]["ticket"] = {
        "category_id": category.id,
        "staff_roles": role_ids,
        "button_channel_id": channel.id
    }
    save_configs()

    view = TicketView()


    embed = discord.Embed(
        title="[+] Tickets ",
        description="Cliquez sur le bouton ci-dessous pour créer un ticket.\nNotre équipe vous répondra rapidement !",
        color=discord.Color(0x4F00B4)
    )
    embed.set_footer(text="xProtect | by nakken_")

    await channel.send(embed=embed, view=view)
    await interaction.response.send_message("✅ Système de ticket configuré.", ephemeral=True)

# ---------- Vue du bouton ----------

class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketButton())

class TicketButton(Button):
    def __init__(self):
        super().__init__(label="🎫 Créer un ticket", style=discord.ButtonStyle.grey, custom_id="open_ticket")

    async def callback(self, interaction: discord.Interaction):
        guild_id = str(interaction.guild_id)
        config = configs.get(guild_id, {}).get("ticket")

        if not config:
            await interaction.response.send_message("⚠️ Le système de tickets n'est pas configuré.", ephemeral=True)
            return

        guild = interaction.guild
        user = interaction.user

        existing_channel = discord.utils.get(guild.text_channels, name=f"ticket-{user.name.lower()}")
        if existing_channel:
            await interaction.response.send_message(f"📌 Tu as déjà un ticket ouvert : {existing_channel.mention}", ephemeral=True)
            return

        category = guild.get_channel(config["category_id"])
        if not category:
            await interaction.response.send_message("⚠️ Catégorie introuvable.", ephemeral=True)
            return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        for role_id in config["staff_roles"]:
            role = guild.get_role(role_id)
            if role:
                overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

        channel = await guild.create_text_channel(f"{user.name}", category=category, overwrites=overwrites)


        staff_pings = " ".join([f"||<@&{role_id}>||" for role_id in config["staff_roles"]])
        await channel.send(f"{staff_pings}\n- **Ticket ouvert par {user.mention}** ")


        ticket_embed = discord.Embed(
            title="[+] Nouveau Ticket",
            description=f"Merci d'expliquer votre problème en détail. Un membre du staff prendra en charge votre demande sous peu !",
            color=discord.Color(0x4F00B4)
        )
        ticket_embed.set_footer(text="xProtect | by nakken_")
        ticket_embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)

        await channel.send(embed=ticket_embed)
                   
        close_button = Button(label="🔒 Fermer le ticket", style=discord.ButtonStyle.danger)

        async def close_callback(interaction_close: discord.Interaction):
            if not interaction_close.user.guild_permissions.administrator:
                await interaction_close.response.send_message("[-] Seul un membre du staff peut fermer le ticket.", ephemeral=True)
                return
            await channel.delete()

        close_button.callback = close_callback

        view = View()
        view.add_item(close_button)

        await channel.send("** Clique ici pour fermer le ticket :**", view=view)
        await interaction.response.send_message(f"[+] Ton ticket est créé : {channel.mention}", ephemeral=True)

TOKEN = "Ton Token ici"
bot.run(TOKEN)











