import os

def install_os():
    #TODO: Should return the file path of the installed OS image
    print("1. Windows")
    print("2. MacOS")
    print("3. Linux")
    print("4. Go back to main menu")
    choice = input("Choose an Operating System (1-4): ")
    if choice == '1':
        print("Select Windows Version:")
        print("1. Windows XP")
        print("2. Windows 10")
        print("3. Windows 11")
        win_choice = input("Choose a version (1-3): ")
        if win_choice == '1':
            print("Choose language for Windows XP Service Pack 3")
            lang={"Arabic":"ar*74065", "Czech":"cs*73965", "Danish":"da*73968", "German":"de*73985", "Greek":"el*73988", "English":"en*73974", "Spanish":"es*74009", "Finnish":"fi*73979", "French":"fr*73982","Hebrew":"he*74143", "Hungarian":"hu*73991", "Italian":"it*73994", "Japanese":"ja*74058", "Korean":"ko*87427", "Dutch":"nl*73971", "Norwegian":"no*74000", "Polish":"pl*74003", "Portuguese-Brazil":"pt-br*74137", "Portuguese-Portugal":"pt-pt*74006","Russian":"ru*74146", "Swedish":"sv*74012", "Turkish":"tr*74085", "zh-hans":"zh-hans*74070", "Chinese-Hong Kong SAR":"zh-hk*74075", "Chinese-Traditional":"zh-tw*74140"}
            print(", ".join(lang))
            lang_choice = input("Enter language: ")
            if lang_choice in lang:
                lang_choice = lang[lang_choice].split('*')
                url = f'https://drive.massgrave.dev/{lang_choice[0]}_windows_xp_professional_with_service_pack_3_x86_cd_vl_x14-{lang_choice[1]}.iso'
            else:
                print("Invalid language choice. Please try again.")
                return install_os()
                        

        elif win_choice == '2':
            pass  #TODO: Implement Windows 10 installation logic
        elif win_choice == '3':
            pass  #TODO: Implement Windows 11 installation logic
        else:
            print("Invalid choice. Please choose a valid option.")
            return install_os()
    elif choice == '2':
        pass
    elif choice == '3':
        pass
    elif choice == '4':
        return
    else:
        print("Invalid choice. Please try again.")
        return install_os()

def extract_os_image(path=None):
    pass #TODO: Should take the file path of the OS image as an argument. If not found, then should prompt the user to provide the path.

def ascii(clear=False):
    if clear:
        os.system('cls' if os.name == 'nt' else 'clear')
    print(r"""                                                                      
                                                                      
     OOOOOOOOO        SSSSSSSSSSSSSSS IIIIIIIIIIEEEEEEEEEEEEEEEEEEEEEE
   OO:::::::::OO    SS:::::::::::::::SI::::::::IE::::::::::::::::::::E
 OO:::::::::::::OO S:::::SSSSSS::::::SI::::::::IE::::::::::::::::::::E
O:::::::OOO:::::::OS:::::S     SSSSSSSII::::::IIEE::::::EEEEEEEEE::::E
O::::::O   O::::::OS:::::S              I::::I    E:::::E       EEEEEE
O:::::O     O:::::OS:::::S              I::::I    E:::::E             
O:::::O     O:::::O S::::SSSS           I::::I    E::::::EEEEEEEEEE   
O:::::O     O:::::O  SS::::::SSSSS      I::::I    E:::::::::::::::E   
O:::::O     O:::::O    SSS::::::::SS    I::::I    E:::::::::::::::E   
O:::::O     O:::::O       SSSSSS::::S   I::::I    E::::::EEEEEEEEEE   
O:::::O     O:::::O            S:::::S  I::::I    E:::::E             
O::::::O   O::::::O            S:::::S  I::::I    E:::::E       EEEEEE
O:::::::OOO:::::::OSSSSSSS     S:::::SII::::::IIEE::::::EEEEEEEE:::::E
 OO:::::::::::::OO S::::::SSSSSS:::::SI::::::::IE::::::::::::::::::::E
   OO:::::::::OO   S:::::::::::::::SS I::::::::IE::::::::::::::::::::E
     OOOOOOOOO      SSSSSSSSSSSSSSS   IIIIIIIIIIEEEEEEEEEEEEEEEEEEEEEE
                                                                      
        Operating Systems Installation and Extraction Utility   """)

def main():
    ascii(clear=True)
    print("1. Install Operating System")
    print("2. Extract Operating System Image")
    print("3. Install and Extract Operating System Image")
    print("4. Exit")
    choice = input("Select an option (1-4): ")
    if choice == '1':
        install_os()
    elif choice == '2':
        extract_os_image()
    elif choice == '3':
        extract_os_image(install_os())
    elif choice == '4':
        print("Exiting...")
        return
    else:
        print("Invalid choice. Please try again.")
        return main()

if __name__ == "__main__":
    main()