from instaloader.instaloader import Instaloader
from instaloader.structures import Profile


L = Instaloader(download_video_thumbnails=False, download_geotags=False, download_comments=False, save_metadata=False, compress_json=False)


class Instagram:

    def __init__(self):
        self.target = ""
        self.user = "89fede_"
        self.profilo = ""


    def get_posts(self):
        """ ottengo tutti i post di un profilo, dato username - LOGIN REQUIRED """
        posts = self.profilo.get_posts()
        L.interactive_login(self.user)
        for post in posts:  
            try:            
                L.download_post(post=post, target=self.target)
            except KeyboardInterrupt:
                print("\nexiting...")
                break
            except:
                print("Errore nel Download dei Posts!")


    @staticmethod
    def get_user_profile(target):
        """ ottengo Profilo, dato username """
        return Profile.from_username(L.context, target)


    def download_stories(self):
        """ DOWNLOAD STORIES -> LOGIN REQUIRED """
        if self.profilo.has_public_story:
            try:
                L.interactive_login(self.user)
                L.download_stories(userids=[self.profilo], filename_target=f"{self.target}") 
            except KeyboardInterrupt:
                print("\nexiting...")
        else:
            print(f"{self.profilo} non ha storie pubbliche al momento!")


    def download_igtv(self):
        """ Scarico IGTV """
        if self.profilo.igtvcount != 0:
            try:
                print("Sto scaricando...")
                L.download_igtv(profile=self.profilo)
            except KeyboardInterrupt:
                print("\nexiting...")
        else:
            print("Non ci sono IGTV video da scaricare...")    


    def get_profile_picture(self):
        """ Scarico Foto Profilo """
        L.download_profilepic(profile=self.profilo)


    def get_profile_info(self):
        try:
            print(f"""
    {self.profilo.username}:
    
Nome: {self.profilo.full_name}
ID: {self.profilo.userid}
Followers: {self.profilo.followers}
Seguiti: {self.profilo.followees}
Bio: {self.profilo.biography}
Verificato: {self.profilo.is_verified}
Storie Pubbliche: {self.profilo.has_public_story}
Privato: {self.profilo.is_private}
            """)            
        except:
            print("Errore...")


    def start(self):
        try:
            # self.user = input("Inserisci il tuo Username: ")
            self.target = input("inserisci l'Username Target: ")
            self.profilo = self.get_user_profile(self.target)
            scelta = input("""\n
SELEZIONA AZIONE DA ESEGUIRE:
1- SCARICA TUTTI I POST DI UN 'TARGET' (COMPRESI IGTV E VIDEO)
2- SCARICA LE STORIE ATTUALI DI UN 'TARGET'
3- SCARICA IGTV DI 'TARGET'
4- SCARICA FOTO PROFILO DI 'TARGET'
5- INFORMAZIONI SUL PROFILO
    """)
        except:
            print("Errore nell'inserimento dati!")
        else:
            if scelta == "1":
                self.get_posts()
            elif scelta == "2":
                self.download_stories()
            elif scelta == "3":
                self.download_igtv()
            elif scelta == "4":
                self.get_profile_picture()
            elif scelta == "5":
                self.get_profile_info()
            else:
                print("Scelta non valida!")


if __name__ == "__main__":
    insta = Instagram()
    insta.start()