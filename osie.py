import os
import webbrowser
from pathlib import Path
import time
import requests
from tqdm import tqdm
from colorama import init, Fore, Style
init(autoreset=True)
def download_file(url,filename):
    download_path = Path.home() / "Downloads" / filename
    temp_path = Path.home() / "Downloads" / (filename + '.osiedownload')
    max_retries = 3

    print(f"Downloading to {download_path}...")
    for attempt in range(1,max_retries+1):
        try:
            resume_pos = temp_path.stat().st_size if temp_path.exists() else 0
            headers ={}
            if resume_pos > 0:
                headers['Range'] = f'bytes={resume_pos}-'
                print(f"Resuming download from {resume_pos/(1024*1024):.2f} MB...")
            response = requests.get(url, stream=True, headers=headers,timeout=30)
            response.raise_for_status()
            if 'content-length' in response.headers:
                total_size = int(response.headers.get('content-length', 0)) + resume_pos
            else:
                total_size = resume_pos

            mode = 'ab' if resume_pos > 0 else 'wb'
            with open(temp_path, mode) as f, tqdm(
                desc=filename,
                total = total_size,
                initial=resume_pos,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for data in response.iter_content(chunk_size = 1024):
                    size = f.write(data)
                    bar.update(size)

                temp_path.rename(download_path)
                print(Fore.GREEN + "Download completed.")
                return str(download_path)

        except KeyboardInterrupt:
                print(Fore.RED + "\n\nDownload interrupted by user. Cleaning Up.")
                temp_path.unlink(missing_ok = True)
                print(Fore.GREEN + "Cleaned up partial files. Exiting...")
                return None
        
        except (requests.exceptions.RequestException, IOError) as e:
            if attempt <= max_retries:
                print(Fore.RED + f"\n\nDownload failed: {e}")
                print(Fore.YELLOW + f"Retrying... (Attempt {attempt} of {max_retries})")
                time.sleep(5)
            else:
                print(Fore.RED + f"\n\nDownload failed after {max_retries} attempts: {e}")
                if temp_path.exists():
                    print(Fore.YELLOW + f"File is partially complete and unusable at this point. Please rerun the program to resume downloading.")
                return None

def install_os(choice=None):
    #TODO: Should return the file path of the installed OS image
    print(Fore.CYAN + "\n1. Windows")
    print(Fore.CYAN + "2. MacOS")
    print(Fore.CYAN + "3. Linux")
    print(Fore.CYAN + "4. Go back to main menu")
    
    choice = input(Fore.MAGENTA + "Choose an Option (1-4): ") if not choice else choice
    if choice == '1':
        print(Fore.CYAN + "Select Windows Version:")
        print(Fore.CYAN + "1. Windows 11")
        print(Fore.CYAN + "2. Windows 10")
        print(Fore.CYAN + "3. Windows XP")
        win_choice = input(Fore.MAGENTA + "Choose a version (1-3): ")
        if win_choice == '1':
            url = 'https://archive.org/download/win-11-23h2/Win11_23H2_English_x64.iso'
            filename = 'windows_11_23h2.iso'
            return download_file(url,filename)
        elif win_choice == '2':
            url = 'https://archive.org/download/en-us_windows_10_consumer_editions_version_22h2_updated_feb_2023_x64_dvd_c29e4bb3/en-us_windows_10_consumer_editions_version_22h2_updated_feb_2023_x64_dvd_c29e4bb3.iso'
            filename = 'windows_10_22h2.iso'
            return download_file(url,filename)
                        
        elif win_choice == '3':
            print(Fore.CYAN + "Choose language for Windows XP Service Pack 3")
            lang={"Arabic":"ar*74065", "Czech":"cs*73965", "Danish":"da*73968", "German":"de*73985", "Greek":"el*73988", "English":"en*73974", "Spanish":"es*74009", "Finnish":"fi*73979", "French":"fr*73982","Hebrew":"he*74143", "Hungarian":"hu*73991", "Italian":"it*73994", "Japanese":"ja*74058", "Korean":"ko*87427", "Dutch":"nl*73971", "Norwegian":"no*74000", "Polish":"pl*74003", "Portuguese-Brazil":"pt-br*74137", "Portuguese-Portugal":"pt-pt*74006","Russian":"ru*74146", "Swedish":"sv*74012", "Turkish":"tr*74085", "zh-hans":"zh-hans*74070", "Chinese-Hong Kong SAR":"zh-hk*74075", "Chinese-Traditional":"zh-tw*74140"}
            print(Fore.CYAN + ", ".join(lang))
            language = input(Fore.MAGENTA + "Enter language: ")
            if language.capitalize() in lang:
                lang_choice = lang[language.capitalize()].split('*')
                url = f'https://drive.massgrave.dev/{lang_choice[0]}_windows_xp_professional_with_service_pack_3_x86_cd_vl_x14-{lang_choice[1]}.iso'
                webbrowser.open(url)
                print(Fore.YELLOW + "\nNote: If the download destination is not your downloads folder, please cancel the download and move it there else the program fails to detect file.")
                print(Fore.CYAN + f"Downloading Windows XP Service Pack 3 in {language.capitalize()}...")
                time.sleep(30) #Allow user to enable download from browser
                while any((Path.home() / "Downloads").glob("*.crdownload")) and not (Path.home() / "Downloads" / f"{lang_choice[0]}_windows_xp_professional_with_service_pack_3_x86_cd_vl_x14-{lang_choice[1]}.iso").exists():
                    time.sleep(30)
                else:
                    if not any((Path.home() / "Downloads").glob("*.crdownload")) and not (Path.home() / "Downloads" / f"{lang_choice[0]}_windows_xp_professional_with_service_pack_3_x86_cd_vl_x14-{lang_choice[1]}.iso").exists():
                        print(Fore.RED + "Download failed or file not found. Please try again.")
                        return install_os('1')
                print(Fore.GREEN + "Download completed.")
                download_path = str(Path.home() / "Downloads" / f"{lang_choice[0]}_windows_xp_professional_with_service_pack_3_x86_cd_vl_x14-{lang_choice[1]}.iso")
                return download_path
            else:
                print(Fore.RED + "Invalid language choice. Please try again.")
                return install_os('1')
        else:
            print(Fore.RED + "Invalid choice. Please choose a valid option.")
            return install_os('1')
    elif choice == '2':
        if os.name == 'nt': #Windows
            print(Fore.YELLOW + "Note: Installation of MacOS is not recommended via ISO images. Hence, a recovery image will be downloaded instead using OpenCore tools. This is the vanilla partition and does not have OpenCore EFI files, therefore should work exactly like an installer downloaded on MacOS.")
            user_input = input(Fore.MAGENTA + "Do you wish to continue? (y/n): ")
            if user_input.lower() == 'y':
                path = Path(os.getcwd()) / "OSIE-OpenCore" / "macrecovery.py"
                
                # Check if file already exists
                if path.exists():
                    print(Fore.GREEN + "macrecovery.py already exists. Skipping download.")
                else:
                    print(Fore.CYAN + "Starting Dependency Download (Credits: OpenCore Team @ https://github.com/acidanthera/OpenCorePkg)\n\n")
                    try:
                        response=requests.get("https://raw.githubusercontent.com/acidanthera/OpenCorePkg/refs/heads/master/Utilities/macrecovery/macrecovery.py", stream=True, timeout=30)
                        response.raise_for_status()
                        size=int(response.headers.get('content-length', 0))
                        with open(path, 'wb') as f, tqdm(
                            desc="macrecovery.py",
                            total=size,
                            unit='iB',
                            unit_scale=True,
                            unit_divisor=1024,
                        ) as bar:
                            for data in response.iter_content(chunk_size=1024):
                                size = f.write(data)
                                bar.update(size)
                        print(Fore.GREEN+"Dependencies downloaded successfully.")
                    except requests.exceptions.RequestException as e:
                        print(Fore.RED + f"Failed to download dependencies: {e}")
                        return install_os('2')
                
                print(Fore.CYAN + "\n\n====================== MacOS Version ======================")
                print(Fore.CYAN + "1. Tahoe\n2. Sequoia\n3. Sonoma\n4. Ventura\n5. Monterey\n6. Big Sur\n7. Catalina\n8. Mojave\n9. High Sierra\n10. Sierra\n11. El Capitan\n12. Yosemite\n13. Mavericks\n14. Mountain Lion\n15. Lion\n16. Exit")
                mac_choice = input(Fore.MAGENTA + "Choose a version (1-16): ")
                match mac_choice:
                    case '1':
                        os.system('py macrecovery.py -b Mac-CFF7D910A743CAAF -m 00000000000000000 -os latest download')
                    case '2':
                        os.system('py macrecovery.py -b Mac-937A206F2EE63C01 -m 00000000000000000 download')
                    case '3':
                        os.system('py macrecovery.py -b Mac-226CB3C6A851A671 -m 00000000000000000 download')
                    case '4':
                        os.system('py macrecovery.py -b Mac-4B682C642B45593E -m 00000000000000000 download')
                    case '5':
                        os.system('py macrecovery.py -b Mac-FFE5EF870D7BA81A -m 00000000000000000 download')
                    case '6':
                        os.system('py macrecovery.py -b Mac-42FD25EABCABB274 -m 00000000000000000 download')
                    case '7':
                        os.system('py macrecovery.py -b Mac-00BE6ED71E35EB86 -m 00000000000000000 download')
                    case '8':
                        os.system('py macrecovery.py -b Mac-7BA5B2DFE22DDD8C -m 00000000000KXPG00 download')
                    case '9':
                        os.system('py macrecovery.py -b Mac-7BA5B2D9E42DDD94 -m 00000000000J80300 download')
                    case '10':
                        os.system('py macrecovery.py -b Mac-77F17D7DA9285301 -m 00000000000J0DX00 download')
                    case '11':
                        os.system('py macrecovery.py -b Mac-FFE5EF870D7BA81A -m 00000000000GQRX00 download')
                    case '12':
                        os.system('py macrecovery.py -b Mac-E43C1C25D4880AD6 -m 00000000000GDVW00 download')
                    case '13':
                        os.system('py macrecovery.py -b Mac-F60DEB81FF30ACF6 -m 00000000000FNN100 download')
                    case '14':
                        os.system('py macrecovery.py -b Mac-7DF2A3B5E5D671ED -m 00000000000F65100 download')
                    case '15':
                        os.system('py macrecovery.py -b Mac-2E6FAB96566FE58C -m 00000000000F25Y00 download')
                    case '16':
                        print(Fore.CYAN + "Returning to main menu...")
                        return main()
                    case _:
                        print(Fore.CYAN + "Invalid Input. Please enter a valid option")
                        return install_os('2')
                print(Fore.GREEN + f"Download completed Successfully. Files are saved at {Path(os.getcwd()) / "OSIE-OpenCore"}")
            else:
                print(Fore.CYAN + "Returning to main menu...")
                return main()
        elif os.name == 'posix': # MacOSX
            try:
                os.system('softwareupdate --list-full-installers; echo; echo "Please enter version number you wish to download:"; read REPLY; [ -n "$REPLY" ] && softwareupdate --fetch-full-installer --full-installer-version "$REPLY"')
            except Exception as e:
                print(Fore.RED + f"An error occurred: {e}")
            else:
                print(Fore.GREEN + "Download completed successfully. Files are stored in Applications folder.")
        else: #Probably Linux or some other unsupported OS.
            print(Fore.YELLOW + "Note: Installation of MacOS is not recommended via ISO images. Hence, a recovery image will be downloaded instead using OpenCore tools. This is the vanilla partition and does not have OpenCore EFI files, therefore should work exactly like an installer downloaded on MacOS.")
            user_input = input(Fore.MAGENTA + "Do you wish to continue? (y/n): ")
            if user_input.lower() == 'y':
                path = Path(os.getcwd()) / "OSIE-OpenCore" / "macrecovery.py"
                
                # Check if file already exists
                if path.exists():
                    print(Fore.GREEN + "macrecovery.py already exists. Skipping download.")
                else:
                    print(Fore.CYAN + "Starting Dependency Download (Credits: OpenCore Team @ https://github.com/acidanthera/OpenCorePkg)\n\n")
                    try:
                        response=requests.get("https://raw.githubusercontent.com/acidanthera/OpenCorePkg/refs/heads/master/Utilities/macrecovery/macrecovery.py", stream=True, timeout=30)
                        response.raise_for_status()
                        size=int(response.headers.get('content-length', 0))
                        with open(path, 'wb') as f, tqdm(
                            desc="macrecovery.py",
                            total=size,
                            unit='iB',
                            unit_scale=True,
                            unit_divisor=1024,
                        ) as bar:
                            for data in response.iter_content(chunk_size=1024):
                                size = f.write(data)
                                bar.update(size)
                        print(Fore.GREEN+"Dependencies downloaded successfully.")
                    except requests.exceptions.RequestException as e:
                        print(Fore.RED + f"Failed to download dependencies: {e}")
                        return install_os('2')
                
                print(Fore.CYAN + "\n\n====================== MacOS Version ======================")
                print(Fore.CYAN + "1. Tahoe\n2. Sequoia\n3. Sonoma\n4. Ventura\n5. Monterey\n6. Big Sur\n7. Catalina\n8. Mojave\n9. High Sierra\n10. Sierra\n11. El Capitan\n12. Yosemite\n13. Mavericks\n14. Mountain Lion\n15. Lion\n16. Exit")
                mac_choice = input(Fore.MAGENTA + "Choose a version (1-16): ")
                match mac_choice:
                    case '1':
                        os.system('python3 ./macrecovery.py -b Mac-CFF7D910A743CAAF -m 00000000000000000 -os latest download')
                    case '2':
                        os.system('python3 ./macrecovery.py -b Mac-7BA5B2D9E42DDD94 -m 00000000000000000 download')
                    case '3':
                        os.system('python3 ./macrecovery.py -b Mac-827FAC58A8FDFA22 -m 00000000000000000 download')
                    case '4':
                        os.system('python3 ./macrecovery.py -b Mac-B4831CEBD52A0C4C -m 00000000000000000 download')
                    case '5':
                        os.system('python3 ./macrecovery.py -b Mac-E43C1C25D4880AD6 -m 00000000000000000 download')
                    case '6':
                        os.system('python3 ./macrecovery.py -b Mac-2BD1B31983FE1663 -m 00000000000000000 download')
                    case '7':
                        os.system('python3 ./macrecovery.py -b Mac-00BE6ED71E35EB86 -m 00000000000000000 download')
                    case '8':
                        os.system('python3 ./macrecovery.py -b Mac-7BA5B2DFE22DDD8C -m 00000000000KXPG00 download')
                    case '9':
                        os.system('python3 ./macrecovery.py -b Mac-BE088AF8C5EB4FA2 -m 00000000000J80300 download')
                    case '10':
                        os.system('python3 ./macrecovery.py -b Mac-77F17D7DA9285301 -m 00000000000J0DX00 download')
                    case '11':
                        os.system('python3 ./macrecovery.py -b Mac-FFE5EF870D7BA81A -m 00000000000GQRX00 download')
                    case '12':
                        os.system('python3 ./macrecovery.py -b Mac-E43C1C25D4880AD6 -m 00000000000GDVW00 download')
                    case '13':
                        os.system('python3 ./macrecovery.py -b Mac-F60DEB81FF30ACF6 -m 00000000000FNN100 download')
                    case '14':
                        os.system('python3 ./macrecovery.py -b Mac-7DF2A3B5E5D671ED -m 00000000000F65100 download')
                    case '15':
                        os.system('python3 ./macrecovery.py -b Mac-C3EC7CD22292981F -m 00000000000F0HM00 download')
                    case '16':
                        print(Fore.CYAN + "Returning to main menu...")
                        return main()
                    case _:
                        print(Fore.CYAN + "Invalid Input. Please enter a valid option")
                        return install_os('2')
                print(Fore.GREEN + f"Download completed Successfully. Files are saved at {Path(os.getcwd()) / "OSIE-OpenCore"}")
            else:
                print(Fore.CYAN + "Returning to main menu...")
                return main()
    elif choice == '3':
        pass #TODO: add linux downloads here
    elif choice == '4':
        main()
    else:
        print(Fore.RED + "Invalid choice. Please try again.")
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
    print(Fore.CYAN + "1. Install Operating System")
    print(Fore.CYAN + "2. Extract Operating System Image")
    print(Fore.CYAN + "3. Install and Extract Operating System Image")
    print(Fore.CYAN + "4. Exit")
    choice = input(Fore.MAGENTA + "Select an option (1-4): ")
    if choice == '1':
        install_os()
    elif choice == '2':
        extract_os_image()
    elif choice == '3':
        extract_os_image(install_os())
    elif choice == '4':
        print(Fore.CYAN + "Exiting...")
        return
    else:
        print(Fore.RED + "Invalid choice. Please try again.")
        return main()

if __name__ == "__main__":
    main()