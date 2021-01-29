from instaloader.instaloader import Instaloader
from instaloader.structures import Profile

from itertools import islice
from math import ceil

L = Instaloader()


class Instagram:

    def __init__(self):
        self. target = ""
        self.user = ""


    def get_posts(self):
        """ ottengo tutti i post di un profilo, dato username - LOGIN REQUIRED """
        profile = Profile.from_username(L.context, self.target)
        posts = profile.get_posts()
        L.interactive_login(self.user)
        for post in posts:  
            try:            
                L.download_post(post=post, target=self.target)
            except KeyboardInterrupt:
                print("\nexiting...")
                break


    def get_user_id(self):
        """ ottengo ID di in profilo, dato username """
        return Profile.from_username(L.context, self.target)


    def download_stories(self):
        """ DOWNLOAD STORIES -> LOGIN REQUIRED """
        user_id = self.get_user_id()
        if user_id.has_public_story:
            try:
                L.interactive_login(self.user)
                L.download_stories(userids=[user_id], filename_target=f"{self.target}") 
            except KeyboardInterrupt:
                print("\nexiting...")
        else:
            print(f"{self.target} non ha storie pubbliche al momento!")


    def download_igtv(self):
        """ Scarico IGTV """
        profile = Profile.from_username(L.context, self.target)
        try:
            print("Sto scaricando...")
            L.download_igtv(profile=profile)
        except KeyboardInterrupt:
            print("\nexiting...")       


    def get_profile_picture(self):
        """ Scarico Foto Profilo """
        profile = Profile.from_username(L.context, self.target)
        L.download_profilepic(profile=profile)


    def start(self):
        self.user = input("Inserisci il tuo Username: ")
        self.target = input("inserisci l'Username Target: ")
        scelta = input("""\n
            SELEZIONA AZIONE DA ESEGUIRE:
            1- SCARICA TUTTI I POST DI UN 'TARGET' (COMPRESI IGTV E VIDEO)
            2- SCARICA LE STORIE ATTUALI DI UN 'TARGET'
            3- SCARICA IGTV DI 'TARGET'
            4- SCARICA FOTO PROFILO DI 'TARGET'
            """)
        if scelta == "1":
            self.get_posts()
        elif scelta == "2":
            self.download_stories()
        elif scelta == "3":
            self.download_igtv()
        elif scelta == "4":
            self.get_profile_picture()
        else:
            print("Scelta non valida!")



""" Scopro se il Profilo è privato """
# profile = Profile.from_username(L.context, '89fede_')
# print(profile.is_private)


""" URL foto profilo """
# profile = Profile.from_username(L.context, 'sara_mory')
# print(profile.profile_pic_url)


""" get_posts()/get_saved_posts()/get_igtv_posts()/get_followees() """
# user = '89fede_'
# L.interactive_login(user)
# profile = Profile.from_username(L.context, 'sara_mory')
# print(profile.get_followees())


if __name__ == "__main__":
    insta = Instagram()
    insta.start()