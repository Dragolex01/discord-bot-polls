import discord
from discord.ext import commands
import matplotlib.pyplot as plt

from functions import *
import secrets

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

# polls = {}

polls = {
    "test": {
        "options": [
            {"option": "option1", "votes": [0]},
            {"option": "option2", "votes": [0]}
        ],
        "finished": False
    }
}

# ¿crear un diccionario con option-->votes en otra variable?

# Turn on bot message
@bot.event
async def on_ready():
    print(f"Encendido! {bot.user}")

# Create new poll
@bot.command()
async def create(ctx, poll_name: str):
    if poll_name in polls:
        await ctx.send(f"Ya existe una encuesta con el nombre '{poll_name}'.")
    else:
        polls[poll_name] = {"options": [], "finished": False} # Añadir votos
        await ctx.send(f"Encuesta '{poll_name}' creada exitosamente.")

# Add to poll
@bot.command()
async def add(ctx, poll_name: str, *, option: str):
    new_option = {"option": option, "votes": []}

    if poll_name not in polls:
        await ctx.send(f"La encuesta '{poll_name}' no existe.")
        # polls[poll_name] = {"options": [], "finished": False}
    elif polls[poll_name]["finished"]:
        await ctx.send(f"La encuesta '{poll_name}' ya ha sido finalizada.")
    else:
        polls[poll_name]["options"].append(new_option) # Los votos ahora estan fuera de "options" pero debe estar dentro, por que los votos es para cada opcion, no por pelicula
        await ctx.send(f"Opción añadida a la encuesta '{poll_name}': {option}")

# Remove from poll
@bot.command()
async def remove(ctx, poll_name: str, position: int):
    if poll_name not in polls:
        await ctx.send(f"No existe una encuesta llamada '{poll_name}'.")
    elif polls[poll_name]["finished"]:
        await ctx.send(f"La encuesta '{poll_name}' ya ha sido finalizada.")
    else:
        try:
            removed_option = polls[poll_name]["options"].pop(position - 1)
            await ctx.send(f"Opción eliminada de la encuesta '{poll_name}': {removed_option}")
        except IndexError:
            await ctx.send(f"La posición {position} no es válida en la encuesta '{poll_name}'.")

# Vote a poll
@bot.command()
async def vote(ctx, poll_name:str, option, vote:int):
    if poll_name in polls:
        if polls[poll_name]["finished"]:
            await ctx.send(f"La encuesta {poll_name} ya ha finalizado")
        else:
            for opt in polls[poll_name]["options"]:
                if opt['option'] == option:
                    opt['votes'] = opt['votes'][0] + vote
                    await ctx.send(f"Voto añadido a {option} correctamente")
                    return
                
            await ctx.send(f"No se ha encontrado la película '{option}' en '{poll_name}'")
    else:
        await ctx.send(f"No se ha encontrado la encuesta '{poll_name}'")
        

    # if vote >= 0 and vote <= 5:
    #     polls[poll_name]["vote"].append(vote) # Deber ser 1 por persona
    #     polls[poll_name]["options"]
    #     votes = [option['votes'] for option in polls[poll_name]["options"]]
    # else:
    #     await ctx.send("La votación debe ser una puntuación enter 1 y 5")

# Finish poll
@bot.command()
async def finish(ctx, poll_name: str):
    if poll_name not in polls:
        await ctx.send(f"No existe una encuesta llamada '{poll_name}'.")
    elif polls[poll_name]["finished"]:
        await ctx.send(f"La encuesta '{poll_name}' ya ha sido finalizada.")
    else:
        polls[poll_name]["finished"] = True

        response = f"Encuesta '{poll_name}' finalizada. Resultados:\n"
        await ctx.send(poll_visualizer(polls, poll_name, response))
        # results = "\n".join([f"{i+1}. {option}" for i, option in enumerate(polls[poll_name]["options"])])
        # await ctx.send(f"Encuesta '{poll_name}' finalizada. Resultados:\n{results}")

# List poll
@bot.command()
async def list(ctx, poll_name: str):
    if poll_name not in polls:
        await ctx.send(f"No existe una encuesta llamada '{poll_name}'. Usa el comando `$create {poll_name}` para crearla primero.")
    elif polls[poll_name]["finished"]:
        await ctx.send(f"La encuesta '{poll_name}' ya ha sido finalizada. Usa `$finish {poll_name}` para ver los resultados.")
    else:
        if len(polls[poll_name]["options"]) == 0:
            await ctx.send(f"La encuesta '{poll_name}' no tiene opciones añadidas todavía.")
        else:
            # options = "\n".join([f"{i+1}. {option}" for i, option in enumerate(polls[poll_name]["options"][0]["option"])])
            response = f"Opciones de la encuesta '{poll_name}':\n"

            await ctx.send(poll_visualizer(polls, poll_name, response))

# Show poll graphic
@bot.command()
async def show1(ctx, poll_name: str):
    if poll_name in polls:
        votes = []
        labels = []

        # Obtener votos y opciones
        for option in polls[poll_name]["options"]:
            votes.append(option['votes'])
            labels.append(option['option'])

        print(f">>>>votes: {votes}")

        # Crear la gráfica de tarta
        plt.figure(figsize=(8, 8))  # Tamaño de la figura (opcional)
        plt.pie(votes, labels=labels, autopct='%1.1f%%', colors=['skyblue', 'orange'])


        # Añadir título
        plt.title(f'Gráfico de Tarta - Encuesta: TEST')

        # Mostrar la gráfica
        plt.show()
    else:
        await ctx.send(f"No hay suficientes votos para la encuesta {poll_name}")



bot.run(secrets.TOKEN)





# si creamos una encuesta que ha sido finalizada, ¿crear otra de cero y borrar anterior? ¿se reabre la encuesta con sus opciones?