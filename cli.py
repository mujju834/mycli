import os
import click
import shutil
import platform
import subprocess
import requests

@click.group()
def cli():
    """A Comprehensive Windows-like CLI Tool."""
    pass

# -----------------------
# File Management Commands
# -----------------------

@cli.command()
@click.argument('path', default='.')
def dir(path):
    """List directory contents."""
    with os.scandir(path) as entries:
        for entry in entries:
            entry_type = 'DIR' if entry.is_dir() else 'FILE'
            click.echo(f"{entry_type} - {entry.name}")

@cli.command()
@click.argument('source')
@click.argument('destination')
def copy(source, destination):
    """Copy a file."""
    shutil.copy(source, destination)
    click.echo(f"Copied {source} to {destination}")

@cli.command()
@click.argument('source')
@click.argument('destination')
def move(source, destination):
    """Move a file."""
    shutil.move(source, destination)
    click.echo(f"Moved {source} to {destination}")

@cli.command()
@click.argument('path')
def delete(path):
    """Delete a file."""
    os.remove(path)
    click.echo(f"Deleted {path}")

@cli.command()
@click.argument('path', default='.')
def mkdir(path):
    """Create a directory."""
    os.makedirs(path, exist_ok=True)
    click.echo(f"Created directory: {path}")

@cli.command()
@click.argument('path')
def rmdir(path):
    """Remove a directory."""
    shutil.rmtree(path)
    click.echo(f"Removed directory: {path}")

# --------------------
# System Information
# --------------------

@cli.command()
def systeminfo():
    """Display system information."""
    info = platform.uname()
    click.echo(f"System: {info.system}")
    click.echo(f"Node: {info.node}")
    click.echo(f"Release: {info.release}")
    click.echo(f"Version: {info.version}")
    click.echo(f"Machine: {info.machine}")
    click.echo(f"Processor: {info.processor}")

@cli.command()
def whoami():
    """Show the current user."""
    click.echo(f"Current user: {os.getlogin()}")

@cli.command()
def uptime():
    """Show system uptime."""
    result = subprocess.run(['uptime'], capture_output=True, text=True)
    click.echo(result.stdout.strip())

# --------------------
# Network Commands
# --------------------

@cli.command()
@click.argument('host')
def ping(host):
    """Ping a host."""
    result = subprocess.run(['ping', '-c', '4', host], capture_output=True, text=True)
    click.echo(result.stdout)

@cli.command()
def ipconfig():
    """Show IP configuration."""
    result = subprocess.run(['ipconfig'], capture_output=True, text=True)
    click.echo(result.stdout)

@cli.command()
@click.argument('url')
def download(url):
    """Download a file from the internet."""
    response = requests.get(url)
    filename = url.split('/')[-1]
    with open(filename, 'wb') as file:
        file.write(response.content)
    click.echo(f"Downloaded {filename}")

# ----------------------
# Disk and System Control
# ----------------------

@cli.command()
@click.argument('path', default='.')
def diskusage(path):
    """Show disk usage."""
    total, used, free = shutil.disk_usage(path)
    click.echo(f"Total: {total // (2**30)} GB")
    click.echo(f"Used: {used // (2**30)} GB")
    click.echo(f"Free: {free // (2**30)} GB")

@cli.command()
@click.argument('seconds', type=int)
def shutdown(seconds):
    """Shutdown the computer after a delay."""
    click.echo(f"Shutting down in {seconds} seconds...")
    os.system(f"shutdown /s /t {seconds}")

@cli.command()
def reboot():
    """Reboot the computer."""
    click.echo("Rebooting...")
    os.system("shutdown /r /t 0")

# -------------------
# Miscellaneous Tools
# -------------------

@cli.command()
def clear():
    """Clear the console."""
    os.system('cls' if os.name == 'nt' else 'clear')

@cli.command()
@click.argument('message')
def echo(message):
    """Print a message to the console."""
    click.echo(message)

@cli.command()
def date():
    """Show the current date and time."""
    result = subprocess.run(['date'], capture_output=True, text=True)
    click.echo(result.stdout.strip())

@cli.command()
@click.argument('cmd')
def run(cmd):
    """Run a custom shell command."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    click.echo(result.stdout)

@cli.command()
def weather():
    """Display the weather using a simple API."""
    city = click.prompt('Enter your city', type=str)
    api_key = 'your_api_key_here'  # Get an API key from OpenWeatherMap or similar services
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url).json()

    if response.get('cod') != 200:
        click.echo(f"Error: {response.get('message')}")
    else:
        temp = response['main']['temp']
        weather_desc = response['weather'][0]['description']
        click.echo(f"The weather in {city}: {temp}°C, {weather_desc}")

# -------------------
# Main Entry Point
# -------------------

if __name__ == '__main__':
    cli()
