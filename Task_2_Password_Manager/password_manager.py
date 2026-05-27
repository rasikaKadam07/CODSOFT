# password_manager.py
# Complete Password Manager with Encryption

import os
import json
import random
import string
import hashlib
from datetime import datetime
from cryptography.fernet import Fernet
import pyperclip
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

class PasswordManager:
    """Main Password Manager Class with Encryption"""
    
    def __init__(self):
        self.data_folder = "data"
        self.key_file = os.path.join(self.data_folder, "secret.key")
        self.vault_file = os.path.join(self.data_folder, "vault.enc")
        self.master_password_file = os.path.join(self.data_folder, "master.hash")
        
        # Create data folder if it doesn't exist
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)
        
        self.key = None
        self.cipher = None
        self.current_user = None
    
    def setup_master_password(self):
        """First time setup - create master password"""
        console.print(Panel.fit("[bold yellow]First Time Setup[/bold yellow]", border_style="yellow"))
        console.print("[cyan]You need to create a master password to secure your vault.[/cyan]\n")
        
        while True:
            master_pw = Prompt.ask("Create master password", password=True)
            confirm_pw = Prompt.ask("Confirm master password", password=True)
            
            if master_pw == confirm_pw and len(master_pw) >= 6:
                # Hash the master password
                hashed = hashlib.sha256(master_pw.encode()).hexdigest()
                with open(self.master_password_file, 'w') as f:
                    f.write(hashed)
                
                # Generate encryption key
                self.key = Fernet.generate_key()
                with open(self.key_file, 'wb') as f:
                    f.write(self.key)
                
                self.cipher = Fernet(self.key)
                
                # Create empty vault
                self.save_vault({})
                
                console.print("[green]✓ Master password created successfully![/green]")
                return True
            else:
                console.print("[red]Passwords don't match or too short! Use at least 6 characters.[/red]")
    
    def login(self):
        """Login with master password"""
        console.print(Panel.fit("[bold blue]Password Manager Login[/bold blue]", border_style="blue"))
        
        # Check if this is first time setup
        if not os.path.exists(self.master_password_file):
            return self.setup_master_password()
        
        # Load encryption key
        try:
            with open(self.key_file, 'rb') as f:
                self.key = f.read()
            self.cipher = Fernet(self.key)
        except FileNotFoundError:
            console.print("[red]Corrupted installation! Please delete 'data' folder and restart.[/red]")
            return False
        
        # Verify master password
        master_pw = Prompt.ask("Enter master password", password=True)
        with open(self.master_password_file, 'r') as f:
            stored_hash = f.read()
        
        if hashlib.sha256(master_pw.encode()).hexdigest() == stored_hash:
            console.print("[green]✓ Login successful![/green]\n")
            return True
        else:
            console.print("[red]✗ Wrong master password![/red]")
            return False
    
    def load_vault(self):
        """Load and decrypt the vault"""
        try:
            with open(self.vault_file, 'rb') as f:
                encrypted_data = f.read()
            
            decrypted_data = self.cipher.decrypt(encrypted_data)
            return json.loads(decrypted_data.decode())
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def save_vault(self, vault):
        """Encrypt and save the vault"""
        json_data = json.dumps(vault, indent=2)
        encrypted_data = self.cipher.encrypt(json_data.encode())
        
        with open(self.vault_file, 'wb') as f:
            f.write(encrypted_data)
    
    def check_password_strength(self, password):
        """Check password strength and return score"""
        score = 0
        feedback = []
        
        # Length check
        if len(password) >= 12:
            score += 25
        elif len(password) >= 8:
            score += 15
        else:
            feedback.append("Use at least 8 characters (12+ recommended)")
        
        # Uppercase check
        if any(c.isupper() for c in password):
            score += 25
        else:
            feedback.append("Add uppercase letters")
        
        # Lowercase check
        if any(c.islower() for c in password):
            score += 15
        else:
            feedback.append("Add lowercase letters")
        
        # Digit check
        if any(c.isdigit() for c in password):
            score += 20
        else:
            feedback.append("Add numbers")
        
        # Special character check
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if any(c in special_chars for c in password):
            score += 15
        else:
            feedback.append("Add special characters (!@#$% etc.)")
        
        # Determine strength level
        if score >= 80:
            strength = "[bold green]Very Strong ✓✓[/bold green]"
            color = "green"
        elif score >= 60:
            strength = "[bold yellow]Strong ✓[/bold yellow]"
            color = "yellow"
        elif score >= 40:
            strength = "[bold orange1]Weak ⚠[/bold orange1]"
            color = "orange1"
        else:
            strength = "[bold red]Very Weak ✗[/bold red]"
            color = "red"
        
        return score, strength, feedback, color
    
    def generate_password(self, length=16):
        """Generate a strong random password"""
        # Define character sets
        uppercase = string.ascii_uppercase
        lowercase = string.ascii_lowercase
        digits = string.digits
        special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Ensure at least one from each category
        password = [
            random.choice(uppercase),
            random.choice(lowercase),
            random.choice(digits),
            random.choice(special)
        ]
        
        # Fill the rest randomly
        all_chars = uppercase + lowercase + digits + special
        password.extend(random.choice(all_chars) for _ in range(length - 4))
        
        # Shuffle to avoid predictable pattern
        random.shuffle(password)
        
        return ''.join(password)
    
    def add_password(self):
        """Add a new password to the vault"""
        console.print(Panel.fit("[bold cyan]Add New Password[/bold cyan]", border_style="cyan"))
        
        service = Prompt.ask("Service/Website name (e.g., Gmail, Netflix)")
        
        # Check if service already exists
        vault = self.load_vault()
        if service in vault:
            if not Confirm.ask(f"[yellow]Service '{service}' already exists. Override?[/yellow]"):
                return
        
        username = Prompt.ask("Username/Email")
        
        # Password generation option
        console.print("\n[1] Generate strong password")
        console.print("[2] Enter my own password")
        choice = Prompt.ask("Choose", choices=["1", "2"])
        
        if choice == "1":
            length = int(Prompt.ask("Password length", default="16"))
            password = self.generate_password(length)
            console.print(f"\n[green]Generated Password:[/green] {password}")
            
            # Copy to clipboard
            pyperclip.copy(password)
            console.print("[dim]✓ Copied to clipboard![/dim]")
            
            # Show strength
            score, strength, feedback, color = self.check_password_strength(password)
            console.print(f"Strength: {strength}")
        else:
            password = Prompt.ask("Enter your password", password=True)
        
        # Optional: Add notes
        notes = Prompt.ask("Additional notes (optional)", default="")
        
        # Save to vault
        vault[service] = {
            'username': username,
            'password': password,
            'notes': notes,
            'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.save_vault(vault)
        console.print(f"[green]✓ Password for '{service}' saved securely![/green]")
    
    def view_passwords(self):
        """View all saved passwords"""
        vault = self.load_vault()
        
        if not vault:
            console.print("[yellow]No passwords saved yet![/yellow]")
            return
        
        # Create table
        table = Table(title="[bold magenta]Your Password Vault[/bold magenta]")
        table.add_column("#", style="cyan", width=4)
        table.add_column("Service", style="green", width=20)
        table.add_column("Username", style="yellow", width=25)
        table.add_column("Password", style="red", width=20)
        table.add_column("Last Updated", style="blue", width=20)
        
        for idx, (service, data) in enumerate(vault.items(), 1):
            # Mask password for display (show only first 4 chars)
            masked_pw = data['password'][:4] + "..." if len(data['password']) > 4 else "***"
            table.add_row(
                str(idx),
                service,
                data['username'],
                masked_pw,
                data.get('updated', data.get('created', 'N/A'))[:10]
            )
        
        console.print(table)
        
        # Option to view/copy a specific password
        if Confirm.ask("\nView or copy a password?"):
            choice = int(Prompt.ask("Enter number", choices=[str(i) for i in range(1, len(vault)+1)]))
            service_name = list(vault.keys())[choice - 1]
            password = vault[service_name]['password']
            
            console.print(f"\n[bold]Service:[/bold] {service_name}")
            console.print(f"[bold]Username:[/bold] {vault[service_name]['username']}")
            console.print(f"[bold]Password:[/bold] [cyan]{password}[/cyan]")
            if vault[service_name].get('notes'):
                console.print(f"[bold]Notes:[/bold] {vault[service_name]['notes']}")
            
            if Confirm.ask("Copy password to clipboard?"):
                pyperclip.copy(password)
                console.print("[green]✓ Password copied![/green]")
    
    def delete_password(self):
        """Delete a password from vault"""
        vault = self.load_vault()
        
        if not vault:
            console.print("[yellow]No passwords to delete![/yellow]")
            return
        
        # Show existing services
        console.print("\n[bold]Saved services:[/bold]")
        for idx, service in enumerate(vault.keys(), 1):
            console.print(f"  {idx}. {service}")
        
        choice = Prompt.ask("Enter number to delete", choices=[str(i) for i in range(1, len(vault)+1)])
        service_name = list(vault.keys())[int(choice) - 1]
        
        if Confirm.ask(f"[red]Are you sure you want to delete '{service_name}'?[/red]"):
            del vault[service_name]
            self.save_vault(vault)
            console.print(f"[green]✓ '{service_name}' deleted successfully![/green]")
    
    def search_password(self):
        """Search for a specific service"""
        vault = self.load_vault()
        
        if not vault:
            console.print("[yellow]No passwords saved yet![/yellow]")
            return
        
        search_term = Prompt.ask("Enter service name to search").lower()
        
        results = {k: v for k, v in vault.items() if search_term in k.lower()}
        
        if not results:
            console.print(f"[red]No results found for '{search_term}'[/red]")
            return
        
        table = Table(title=f"[bold]Search Results: '{search_term}'[/bold]")
        table.add_column("Service", style="green")
        table.add_column("Username", style="yellow")
        
        for service, data in results.items():
            table.add_row(service, data['username'])
        
        console.print(table)
    
    def show_strength_report(self):
        """Show password strength report for all saved passwords"""
        vault = self.load_vault()
        
        if not vault:
            console.print("[yellow]No passwords to analyze![/yellow]")
            return
        
        table = Table(title="[bold]Password Strength Report[/bold]")
        table.add_column("Service", style="cyan", width=20)
        table.add_column("Strength Score", style="yellow", width=15)
        table.add_column("Rating", style="green", width=15)
        
        weak_passwords = []
        
        for service, data in vault.items():
            score, strength, _, _ = self.check_password_strength(data['password'])
            table.add_row(service, f"{score}/100", strength)
            
            if score < 50:
                weak_passwords.append(service)
        
        console.print(table)
        
        if weak_passwords:
            console.print("\n[yellow]⚠ Weak passwords found for:[/yellow]")
            for wp in weak_passwords:
                console.print(f"  • {wp}")
            console.print("\n[dim]Consider regenerating these passwords for better security.[/dim]")

def main():
    """Main program loop"""
    console.print(Panel.fit("[bold magenta]🔐 PROFESSIONAL PASSWORD MANAGER 🔐[/bold magenta]", border_style="magenta"))
    console.print("[dim]Secure • Encrypted • Easy to Use[/dim]\n")
    
    pm = PasswordManager()
    
    # Login or setup
    if not pm.login():
        return
    
    while True:
        console.print("\n" + "="*50)
        console.print("[bold]Main Menu[/bold]")
        console.print("="*50)
        console.print("[1] 🔑 Add New Password")
        console.print("[2] 👁️  View All Passwords")
        console.print("[3] 🔍 Search Password")
        console.print("[4] 🗑️  Delete Password")
        console.print("[5] 📊 Password Strength Report")
        console.print("[6] 🔒 Generate Random Password")
        console.print("[7] 💪 Check Password Strength")
        console.print("[8] 🚪 Exit")
        console.print("="*50)
        
        choice = Prompt.ask("Choose option", choices=["1","2","3","4","5","6","7","8"])
        
        if choice == "1":
            pm.add_password()
        elif choice == "2":
            pm.view_passwords()
        elif choice == "3":
            pm.search_password()
        elif choice == "4":
            pm.delete_password()
        elif choice == "5":
            pm.show_strength_report()
        elif choice == "6":
            length = int(Prompt.ask("Password length", default="16"))
            password = pm.generate_password(length)
            console.print(f"\n[bold green]Generated Password:[/bold green] {password}")
            pyperclip.copy(password)
            console.print("[green]✓ Copied to clipboard![/green]")
            
            # Show strength
            score, strength, feedback, color = pm.check_password_strength(password)
            console.print(f"Strength: {strength}")
        elif choice == "7":
            password = Prompt.ask("Enter password to check", password=True)
            score, strength, feedback, color = pm.check_password_strength(password)
            console.print(f"\nScore: {score}/100")
            console.print(f"Strength: {strength}")
            
            if feedback:
                console.print("\n[yellow]Suggestions to improve:[/yellow]")
                for f in feedback:
                    console.print(f"  • {f}")
        elif choice == "8":
            console.print("\n[bold blue]Goodbye! Keep your passwords safe! 🔐[/bold blue]")
            break

if __name__ == "__main__":
    main()


    # TEMPORARY TEST - Remove after testing
if __name__ == "__main__":
    pm = PasswordManager()
    
    # Test various lengths
    test_lengths = [4, 8, 12, 16, 20, 50]
    for l in test_lengths:
        pw = pm.generate_password(l)
        print(f"Length {l}: {pw} (actual length: {len(pw)})")
    
    print("\n✓ Test complete! Password generator is working.")