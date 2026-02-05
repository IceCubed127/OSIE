import os
import webbrowser
from pathlib import Path
import time
import requests
from tqdm import tqdm

def install_os():
    #TODO: Should return the file path of the installed OS image
    print("\n1. Windows")
    print("2. MacOS")
    print("3. Linux")
    print("4. Go back to main menu")
    choice = input("Choose an Option (1-4): ")
    if choice == '1':
        print("Select Windows Version:")
        print("1. Windows 11")
        print("2. Windows 10")
        print("3. Windows XP")
        win_choice = input("Choose a version (1-3): ")
        if win_choice == '1':
            pass  #TODO: Implement Windows 11 installation logic
        elif win_choice == '2':
            url = 'https://archive.org/download/en-us_windows_10_consumer_editions_version_22h2_updated_feb_2023_x64_dvd_c29e4bb3/en-us_windows_10_consumer_editions_version_22h2_updated_feb_2023_x64_dvd_c29e4bb3.iso'
            filename = 'windows_10_22h2.iso'
            download_path = Path.home() / "Downloads" / filename
            temp_path = Path.home() / "Downloads" / (filename + '.osiedownload')
            max_retries = 3

            print(f"Downloading Windows 10 to {download_path}...")
            for attempt in range(1,max_retries+1):
                    try:
                        resume_pos = temp_path.stat().st_size if temp_path.exists() else 0
                        headers = {}
                        if resume_pos > 0:
                            headers['Range'] = f'bytes={resume_pos}-'
                            print(f"Resuming download from {resume_pos/(1024*1024):.2f} MB...")

                        response = requests.get(url, stream=True, headers=headers, timeout=30)
                        response.raise_for_status()

                        if 'content-length' in response.headers:
                            total_size = int(response.headers.get('content-length', 0)) + resume_pos
                        else:
                            total_size = resume_pos

                        mode = 'ab' if resume_pos > 0 else 'wb'
                        with open(temp_path, mode) as f, tqdm(
                            desc=filename,
                            total=total_size,
                            initial=resume_pos,
                            unit='iB',
                            unit_scale=True,
                            unit_divisor=1024,
                        ) as bar:
                            for data in response.iter_content(chunk_size = 1024):
                                size = f.write(data)
                                bar.update(size)

                        # Rename to final filename on successful completion
                        temp_path.rename(download_path)
                        print("Download completed.")
                        return str(download_path)

                    except KeyboardInterrupt:
                        print("\n\nDownload interrupted by user. Cleaning Up.")
                        temp_path.unlink(missing_ok=True)
                        print("Cleaned up partially downloaded file. Exiting...")
                        return None
                    
                    except (requests.exceptions.RequestException, IOError) as e:
                        if attempt <= max_retries:
                            print(f"\n\nDownload failed: {e}")
                            print(f"Retrying... (Attempt {attempt} of {max_retries})")
                            time.sleep(5)
                        else:
                            print(f"\n\nDownload failed after {max_retries} attempts: {e}")
                            if temp_path.exists():
                                print(f"File is partially complete and unusable at this point. Please rerun the program to resume downloading.")
                            return None
                        
        elif win_choice == '3':
            print("Choose language for Windows XP Service Pack 3")
            lang={"Arabic":"ar*74065", "Czech":"cs*73965", "Danish":"da*73968", "German":"de*73985", "Greek":"el*73988", "English":"en*73974", "Spanish":"es*74009", "Finnish":"fi*73979", "French":"fr*73982","Hebrew":"he*74143", "Hungarian":"hu*73991", "Italian":"it*73994", "Japanese":"ja*74058", "Korean":"ko*87427", "Dutch":"nl*73971", "Norwegian":"no*74000", "Polish":"pl*74003", "Portuguese-Brazil":"pt-br*74137", "Portuguese-Portugal":"pt-pt*74006","Russian":"ru*74146", "Swedish":"sv*74012", "Turkish":"tr*74085", "zh-hans":"zh-hans*74070", "Chinese-Hong Kong SAR":"zh-hk*74075", "Chinese-Traditional":"zh-tw*74140"}
            print(", ".join(lang))
            language = input("Enter language: ")
            if language.capitalize() in lang:
                lang_choice = lang[language.capitalize()].split('*')
                url = f'https://drive.massgrave.dev/{lang_choice[0]}_windows_xp_professional_with_service_pack_3_x86_cd_vl_x14-{lang_choice[1]}.iso'
                webbrowser.open(url)
                print("\nNote: If the download destination is not your downloads folder, please cancel the download and move it there else the program fails to detect file.")
                print(f"Downloading Windows XP Service Pack 3 in {language.capitalize()}...")
                time.sleep(30) #Allow user to enable download from browser
                while any((Path.home() / "Downloads").glob("*.crdownload")) and not (Path.home() / "Downloads" / f"{lang_choice[0]}_windows_xp_professional_with_service_pack_3_x86_cd_vl_x14-{lang_choice[1]}.iso").exists():
                    time.sleep(30) # Timeout for 30 seconds
                else:
                    if not any((Path.home() / "Downloads").glob("*.crdownload")) and not (Path.home() / "Downloads" / f"{lang_choice[0]}_windows_xp_professional_with_service_pack_3_x86_cd_vl_x14-{lang_choice[1]}.iso").exists():
                        print("Download failed or file not found. Please try again.")
                        return install_os()
                print("Download completed.")
                download_path = str(Path.home() / "Downloads" / f"{lang_choice[0]}_windows_xp_professional_with_service_pack_3_x86_cd_vl_x14-{lang_choice[1]}.iso")
                return download_path
            else:
                print("Invalid language choice. Please try again.")
                return install_os()
        else:
            print("Invalid choice. Please choose a valid option.")
            return install_os()
    elif choice == '2':
        pass
    elif choice == '3':
        pass
    elif choice == '4':
        main()
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