from quart import Quart, render_template, request
import aiohttp

app = Quart(__name__, static_folder='static', static_url_path='')

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route("/Release")
async def releases():
    return await render_template("Release")

@app.route("/Packages")
async def packages():
    if "Sileo" in request.headers.get('User-Agent'):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://getzbra.com/repo/Packages') as resp:
                    zebra = (await resp.text()).replace("./", "https://getzbra.com/repo/")
                    final = ""
                    for i in zebra.splitlines(True):
                        if i.startswith("Section"):
                            final += "Section: This repo does not support Sileo.\n"
                        elif i.startswith("Description"):
                            final += "Description: This repo does not support Sileo and never will support Sileo. Please install Zebra (this package) or any package manager that is not Sileo to enjoy my tweaks.\n"
                        elif i.startswith("Name"):
                            final += "Name: Zebra\n"
                        elif i.startswith("Depiction"):
                            final += ""
                        else:
                            final += i
                    return final
        except:
            return await render_template("Packages")
    else:
        return await render_template("Packages")