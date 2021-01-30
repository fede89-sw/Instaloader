from instaloader.exceptions import ConnectionException, ProfileNotExistsException, QueryReturnedNotFoundException
from instaloader.instaloader import Instaloader
from instaloader.structures import Profile
from rich.console import Console
import os, sys


L = Instaloader(download_video_thumbnails=False, download_geotags=False, download_comments=False, save_metadata=False, compress_json=False)
console = Console()


class Instagram:

    OPENING = 0

    def __init__(self):
        self.target = ""
        self.user = ""
        self.profilo = ""


    def get_posts(self):
        """ ottengo tutti i post di un profilo, dato username - LOGIN REQUIRED """
        posts = self.profilo.get_posts()
        for post in posts:  
            try:            
                L.download_post(post=post, target=self.target)
            except KeyboardInterrupt:
                console.print("\nexiting...", style="italic red")
                input()
                break
            except:
                console.print("Errore nel Download dei Posts!", style="italic red")
                input()


    @staticmethod
    def get_user_profile(target):
        """ ottengo un istanza di Profilo, dato username """
        return Profile.from_username(L.context, target)


    def download_stories(self):
        """ DOWNLOAD STORIES -> LOGIN REQUIRED """
        if self.profilo.has_public_story:
            try:
                L.download_stories(userids=[self.profilo], filename_target=f"{self.target}") 
            except KeyboardInterrupt:
                console.print("\nexiting...", style="italic red")
                input()
                sys.exit()
        else:
            console.print(f"{self.profilo} non ha storie pubbliche al momento!", style="italic #d75f00")
            input()


    def download_igtv(self):
        """ Scarico IGTV """
        if self.profilo.igtvcount != 0:
            try:
                console.print("Sto scaricando...", style="italic blue")
                L.download_igtv(profile=self.profilo)
            except KeyboardInterrupt:
                console.print("\nexiting...", style="italic red")
                input()
                sys.exit()
        else:
            console.print("Non ci sono IGTV video da scaricare...", style="italic #d75f00")
            input()


    def get_profile_picture(self):
        """ Scarico Foto Profilo """
        L.download_profilepic(profile=self.profilo)


    def get_profile_info(self):
        try:
            console.print(f"""
    [italic #d75f00]{self.profilo.username}[/italic #d75f00]:
    
[bold blue]Nome:[/bold blue] {self.profilo.full_name}
[bold blue]ID:[/bold blue] {self.profilo.userid}
[bold blue]Followers:[/bold blue] {self.profilo.followers}
[bold blue]Seguiti:[/bold blue] {self.profilo.followees}
[bold blue]Bio:[/bold blue] \n{self.profilo.biography}
[bold blue]Verificato:[/bold blue] {self.profilo.is_verified}
[bold blue]Storie Pubbliche:[/bold blue] {self.profilo.has_public_story}
[bold blue]Privato:[/bold blue] {self.profilo.is_private}
            """, justify="center")
            input()     
        except:
            console.print("Errore...", style="italic red")
            input()

    
    def get_similar_profile(self):
        """ LOGIN REQUIRED """     
        account_simili = self.profilo.get_similar_accounts()
        print("Account Simili: ")
        for account in account_simili:
            print(account.username)
        input()


    def target_data(self):
            self.target = input("Inserisci l'Username Target: ")
            try:
                self.profilo = self.get_user_profile(self.target)
            except QueryReturnedNotFoundException as e:
                console.print(f"Errore! Utente non trovato...{e}", style="italic red")
                input()
                sys.exit()
            except ConnectionException as e:
                console.print(f"Errore! Connessione non riuscita...{e}", style="italic red")
                input()
                sys.exit()
            except ProfileNotExistsException as e:
                console.print(f"Errore! Il Profilo '{self.target}' non esiste ...{e}", style="italic red")
                input()
                sys.exit()
            except:
                console.print("Errore nell'inserimento dati!", style="italic red")
                input()
                sys.exit()
            else:
                console.print(f"Target Acquisito: [bold blue]{self.target}[/bold blue]")
                input()
                self.start()

    @staticmethod
    def get_saved_posts():
        num = input("Inserisci quanti Post vuoi salvare (noo speficare se li vuoi tutti): ")
        if num:
            L.download_saved_posts(max_count=int(num))
        else:
            L.download_saved_posts()  
        

    def start(self):
        try:
            if Instagram.OPENING == 0:
                Instagram.OPENING = 1
                self.user = input("Inserisci il tuo Username: ")
                L.interactive_login(self.user)
                self.target_data()
            os.system("cls")
            console.print(f"""\n
                SELEZIONA AZIONE DA ESEGUIRE: :smiley:

                [green]0[/green]- CAMBIA TARGET
                [green]1[/green]- INFORMAZIONI SUL PROFILO
                [green]2[/green]- LISTA PROFILI 'SIMILI'
                [green]3[/green]- SCARICA FOTO PROFILO DI '[green]{self.target}[/green]'
                [green]4[/green]- SCARICA LE STORIE ATTUALI DI UN '[green]{self.target}[/green]'
                [green]5[/green]- SCARICA IGTV DI '[green]{self.target}[/green]'
                [green]6[/green]- SCARICA TUTTI I POST DI UN '[green]{self.target}[/green]' (COMPRESI VIDEO)
                [green]7[/green]- SCARICA TUTTI I TUOI POST SALVATI
                    """,
                    style="bold white on dark_blue", 
                    justify="center")
            scelta = input()
        except KeyboardInterrupt:
            console.print("\nexiting...", style="italic red")
            input()
            sys.exit()
        except:
            console.print("Errore nell'inserimento dati!", style="italic red")
            input()
        else:
            if scelta == "0":
                self.target_data() 
            if scelta == "1":
                self.get_profile_info() 
            elif scelta == "2":
                self.get_similar_profile()
            elif scelta == "3":
                self.get_profile_picture()
            elif scelta == "4":
                self.download_stories()
            elif scelta == "5":
                self.download_igtv()
            elif scelta == "6":
                self.get_posts()
            elif scelta == "7":
                self.get_saved_posts()
                
            else:
                print("Scelta non valida!")
                input()


if __name__ == "__main__":
    insta = Instagram()
    while True:
        try:
            insta.start()
        except KeyboardInterrupt:
            console.print("\nexiting...", style="italic red")
            break
        