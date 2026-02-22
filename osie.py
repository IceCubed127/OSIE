import os
import webbrowser
from pathlib import Path
import time
import requests
from tqdm import tqdm
from colorama import init, Fore, Style
init(autoreset=True)
def download_file(url,filename):
    download_path = Path.home() / "Downloads" / "OSIE" / "ISOs" / filename
    temp_path = Path.home() / "Downloads" / "OSIE" / "ISOs" / (filename + '.osiedownload')
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
                path = Path(os.getcwd()) / "OSIE" / "OpenCore" / "macrecovery.py"
                
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
                print(Fore.GREEN + f"Download completed Successfully. Files are saved at {Path(os.getcwd()) / "OSIE" / "OpenCore"}")
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
                path = Path(os.getcwd()) / "OSIE" / "OpenCore" / "macrecovery.py"
                
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
                print(Fore.GREEN + f"Download completed Successfully. Files are saved at {Path(os.getcwd()) / "OSIE" / "OpenCore"}")
            else:
                print(Fore.CYAN + "Returning to main menu...")
                return main()
    elif choice == '3':
        print(Fore.CYAN + "Choose a Linux Distribution:")
        print(Fore.CYAN + "1. Ubuntu\n2.Fedora\n3. Arch Linux\n4. Kali Linux\n5. Debian\n6. Linux Mint\n7. Pop!_OS\n8. Zorin OS\n9. Exit")
        linux_choice = input(Fore.MAGENTA + "Choose a distribution (1-9): ")
        if linux_choice == '1':
            print(Fore.YELLOW + "")
            print(Fore.CYAN + "1. Ubuntu 24.04.3 LTS\n2. Ubuntu 25.10\n3. Ubuntu 22.04 LTS (Jammy Jellyfish)\n4. Ubuntu Server 24.04.3 LTS\n5. Ubuntu Server 25.10\n6. Other Ubuntu Versions\n7. Exit")
            ubuntu_choice = input(Fore.MAGENTA + "Choose an Ubuntu Version:")
            match ubuntu_choice:
                case '1':
                    url = 'https://releases.ubuntu.com/24.04.3/ubuntu-24.04.3-desktop-amd64.iso'
                    filename = 'ubuntu-24.04.3-desktop-amd64.iso'
                    return download_file(url,filename)
                case '2':
                    url = "https://releases.ubuntu.com/25.10/ubuntu-25.10-desktop-amd64.iso"
                    filename = "ubuntu-25.10-desktop-amd64.iso"
                    return download_file(url,filename)
                case '3':
                    url = "https://releases.ubuntu.com/22.04/ubuntu-22.04.5-desktop-amd64.iso"
                    filename = "ubuntu-22.04.5-desktop-amd64.iso"
                    return download_file(url,filename)
                case '4':
                    url = "https://releases.ubuntu.com/24.04.3/ubuntu-24.04.3-live-server-amd64.iso"
                    filename = "ubuntu-24.04.3-live-server-amd64.iso"
                    return download_file(url,filename)
                case '5':
                    url = "https://releases.ubuntu.com/25.10/ubuntu-25.10-live-server-amd64.iso"
                    filename = "ubuntu-25.10-live-server-amd64.iso"
                    return download_file(url,filename)
                case '6':
                    print(Fore.YELLOW + "Redirecting to Ubuntu releases page...")
                    time.sleep(3)
                    webbrowser.open("https://releases.ubuntu.com/")
                case '7':
                    print(Fore.CYAN + "Returning to main menu...")
                    return main()
                case _:
                    print(Fore.RED + "Invalid choice. Please choose a valid option.")
                    return install_os('3')
        elif linux_choice == '2':
            print(Fore.CYAN + "1. Fedora 43 Desktop\n2. Fedora 43 Workstation\n3. Fedora 43 Server\n4. Fedora 43 CoreOS\n5. Other Fedora Versions\n6. Exit")
            choice = input(Fore.MAGENTA + "Choose a Fedora Version:")
            match choice:
                case '1':
                    url = "https://download.fedoraproject.org/pub/fedora/linux/releases/43/KDE/x86_64/iso/Fedora-KDE-Desktop-Live-43-1.6.x86_64.iso"
                    download_file(url,"fedora-43-desktop.iso")
                case '2':
                    url = "https://download.fedoraproject.org/pub/fedora/linux/releases/43/Workstation/x86_64/iso/Fedora-Workstation-Live-43-1.6.x86_64.iso"
                    download_file(url,"fedora-43-workstation.iso")
                case '3':
                    webbrowser.open("https://www.fedoraproject.org/server/download/")
                case '4':
                    url = "https://builds.coreos.fedoraproject.org/prod/streams/stable/builds/43.20260119.3.1/x86_64/fedora-coreos-43.20260119.3.1-live-iso.x86_64.iso"
                    download_file(url, "fedora-coreos-43.iso")
                case '5':
                    print(Fore.YELLOW + "Redirecting to Fedora releases page...")
                    time.sleep(3)
                    webbrowser.open("https://www.fedoraproject.org/#editions")
                case '6':
                    print(Fore.CYAN + "Returning to main menu...")
                    return main()
                case _:
                    print(Fore.RED + "Invalid choice. Please choose a valid option.")
                    return install_os('3')
        elif linux_choice == '3':
            url = "https://geo.mirror.pkgbuild.com/iso/2026.02.01/archlinux-x86_64.iso"
            return download_file(url,"archlinux-x86_64.iso")
        elif linux_choice == '4':
            print(Fore.CYAN + "1. Kali Linux Installer (x86_64)\n2. Kali Linux NetInstaller\n3. Kali Linux Installer (ARM64)\n4. VMware Image\n5. VirtualBox Image\n6. Hyper-V Image\n7. Exit")
            choice = input(Fore.MAGENTA + "Choose an option (1-6): ")
            match choice:
                case '1':
                    url = "https://cdimage.kali.org/kali-2025.4/kali-linux-2025.4-installer-amd64.iso"
                    return download_file(url,"kali-linux-installer-amd64.iso")
                case '2':
                    url = "https://cdimage.kali.org/kali-2025.4/kali-linux-2025.4-installer-netinst-amd64.iso"
                    return download_file(url, "kali-linux-netinstaller-amd64.iso")
                case '3':
                    url = "https://cdimage.kali.org/kali-2025.4/kali-linux-2025.4-installer-arm64.iso"
                    return download_file(url, "kali-linux-installer-arm64.iso")
                case '4':
                    download_file("https://cdimage.kali.org/kali-2025.4/kali-linux-2025.4-vmware-amd64.7z", "kali-linux-vmware-amd64.7z")
                    print(Fore.YELLOW + "Please extract the archive and import the .vmx file into VMware to use the image.")
                case '5':
                    download_file("https://cdimage.kali.org/kali-2025.4/kali-linux-2025.4-virtualbox-amd64.7z", "kali-linux-virtualbox-amd64.7z")
                    print(Fore.YELLOW + "Please extract the archive and import the .vbox file into VirtualBox to use the image.")
                case '6':
                    download_file("https://cdimage.kali.org/kali-2025.4/kali-linux-2025.4-hyperv-amd64.7z", "kali-linux-hyperv-amd64.7z")
                    print(Fore.YELLOW + "Please extract the archive and import the .xml file into Hyper-V to use the image.")
                case '7':
                    print(Fore.CYAN + "Returning to main menu...")
                    return main()
                case _:
                    print(Fore.RED + "Invalid choice. Please choose a valid option.")
                    return install_os('3')
        elif linux_choice == '5':
            return download_file("https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-13.3.0-amd64-netinst.iso", "debian-13.3.0-amd64-netinst.iso")
        elif linux_choice == '6':
            print(Fore.CYAN + "1. Cinnamon - Modern themed fully featured desktop\n2. MATE - Traditional & Faster Desktop\n3. Xfce - Lightweight Desktop Environment\n4. Exit")
            choice = input(Fore.MAGENTA + "Choose a desktop environment (1-4): ")
            match choice:
                case '1':
                    print(Fore.GREEN + "Verify Checksum here: https://linuxmint.com/edition.php?id=326")
                    return download_file("https://pub.linuxmint.io/stable/22.3/linuxmint-22.3-cinnamon-64bit.iso", "linuxmint-22.3-cinnamon-64bit.iso")
                case '2':
                    print(Fore.GREEN + "Verify Checksum here: https://linuxmint.com/edition.php?id=328")
                    return download_file("https://pub.linuxmint.io/stable/22.3/linuxmint-22.3-mate-64bit.iso", "linuxmint-22.3-mate-64bit.iso")
                case '3':
                    print(Fore.GREEN + "Verify Checksum here: https://linuxmint.com/edition.php?id=327")
                    return download_file("https://pub.linuxmint.io/stable/22.3/linuxmint-22.3-xfce-64bit.iso", "linuxmint-22.3-xfce-64bit.iso")
                case '4':
                    print(Fore.CYAN + "Returning to main menu...")
                    return main()
                case _:
                    print(Fore.RED + "Invalid choice. Please choose a valid option.")
                    return install_os('3')
        elif linux_choice == '7':
            print(Fore.CYAN + "1. LTS (Intel, AMD and Nvidia 10 Series and Lower)\n2. LTS for Nvidia GPUs 16 Series and Higher\n3. LTS for ARM64 Devices\n4. LTS for ARM64 With Nvidia GPUs\n5. Exit")
            choice = input(Fore.MAGENTA + "Choose an option (1-5): ")
            match choice:
                case '1':
                    return download_file("https://iso.pop-os.org/24.04/amd64/generic/23/pop-os_24.04_amd64_generic_23.iso", "popos-24.04-amd64-generic.iso")
                case '2':
                    return download_file("https://iso.pop-os.org/24.04/amd64/nvidia/23/pop-os_24.04_amd64_nvidia_23.iso", "popos-24.04-amd64-nvidia.iso")
                case '3':
                    return download_file("https://iso.pop-os.org/24.04/arm64/generic/3/pop-os_24.04_arm64_generic_3.iso", "popos-24.04-arm64-generic.iso")
                case '4':
                    return download_file("https://iso.pop-os.org/24.04/arm64/nvidia/3/pop-os_24.04_arm64_nvidia_3.iso", "popos-24.04-arm64-nvidia.iso")
                case '5':
                    print(Fore.CYAN + "Returning to main menu...")
                    return main()
                case _:
                    print(Fore.RED + "Invalid choice. Please choose a valid option.")
                    return install_os('3')
        elif linux_choice == '8':
            return download_file("https://mirrors.edge.kernel.org/zorinos-isos/18/Zorin-OS-18-Core-64-bit-r3.iso", "zorin-os-18-core-64-bit.iso")
        elif linux_choice == '9':
            print(Fore.CYAN + "Returning to main menu...")
            return main()
        else:
            print(Fore.RED + "Invalid choice. Please choose a valid option.")
            return install_os('3')
    elif choice == '4':
        main()
    else:
        print(Fore.RED + "Invalid choice. Please try again.")
        return install_os()

def check_rpi():
    if os.name == 'nt':
        path = r"C:\Program Files (x86)\Raspberry Pi Imager\rpi-imager.exe"
        if not os.path.exists(path):
            print(Fore.YELLOW + "Raspberry Pi Imager was not found. Please enter the path to 'rpi-imager.exe'. Press enter to download the installer.")
            new_path = input(Fore.MAGENTA + "Path: ").strip('"')
            if new_path.strip() == "":
                download_file("https://downloads.raspberrypi.com/imager/imager_latest.exe", "rpi-imager-install.exe")
                input(Fore.CYAN + "Press Enter to continue. Please ensure that the Imager is now installed before you proceed.")
                return check_rpi()
            else:
                if os.path.exists(new_path) and new_path.endswith("rpi-imager.exe"):
                    return new_path
        else:
            return path
    elif os.name == 'posix':
        path = "/Applications/Raspberry Pi Imager.app/Contents/MacOS/rpi-imager"
        if not os.path.exists(path):
            print(Fore.YELLOW + "Raspberry Pi Imager was not found. Please enter the path to 'rpi-imager'. Press enter to download the installer.")
            new_path = input(Fore.MAGENTA + "Path: ").strip('"')
            if new_path.strip() == "":
                webbrowser.open("https://downloads.raspberrypi.com/imager/imager_latest.dmg")
                input(Fore.CYAN + "Press Enter to continue. Please ensure that the Imager is now installed before you proceed.")
                return check_rpi()
            else:
                if os.path.exists(new_path) and new_path.endswith("rpi-imager"):
                    return new_path
        else:
            return path
    else:
        import shutil
        path = shutil.which("rpi-imager")
        if path:
            return path
        else:
            print(Fore.YELLOW + "Raspberry Pi Imager was not found. Please enter the path to 'rpi-imager'. Press enter to download.")
            new_path = input(Fore.MAGENTA + "Path: ").strip('"')
            if new_path.strip() == "":
                os.system("sudo apt-get update && sudo apt-get install rpi-imager -y")
                input(Fore.CYAN + "Press Enter to continue. Please ensure that the Imager is now installed before you proceed.")
                return check_rpi()
            else:
                if os.path.exists(new_path) and os.access(new_path, os.X_OK):
                    return new_path
    

def extract_os_image(path=None):
    rpi = check_rpi()
    pass #TODO: Should take the file path of the OS image as an argument. If not found, then should prompt the user to provide the path.

def ascii(clear=False):
    if clear:
        os.system('cls' if os.name == 'nt' else 'clear')
    print(r"""                                                                      
                                                                      
     OOOOOOOOO         SSSSSSSSSSSSSSS  IIIIIIIIII EEEEEEEEEEEEEEEEEEEEEE
   OO:::::::::OO     SS:::::::::::::::S I::::::::I E::::::::::::::::::::E
 OO:::::::::::::OO  S:::::SSSSSS::::::S I::::::::I E::::::::::::::::::::E
O:::::::OOO:::::::O S:::::S     SSSSSSS II::::::II EE::::::EEEEEEEEE::::E
O::::::O   O::::::O S:::::S               I::::I     E:::::E       EEEEEE
O:::::O     O:::::O S:::::S               I::::I     E:::::E             
O:::::O     O:::::O  S::::SSSS            I::::I     E::::::EEEEEEEEEE   
O:::::O     O:::::O   SS::::::SSSSS       I::::I     E:::::::::::::::E   
O:::::O     O:::::O     SSS::::::::SS     I::::I     E:::::::::::::::E   
O:::::O     O:::::O        SSSSSS::::S    I::::I     E::::::EEEEEEEEEE   
O:::::O     O:::::O             S:::::S   I::::I     E:::::E             
O::::::O   O::::::O             S:::::S   I::::I     E:::::E       EEEEEE
O:::::::OOO:::::::O SSSSSSS     S:::::S II::::::II EE::::::EEEEEEEE:::::E
 OO:::::::::::::OO  S::::::SSSSSS:::::S I::::::::I E::::::::::::::::::::E
   OO:::::::::OO    S:::::::::::::::SS  I::::::::I E::::::::::::::::::::E
     OOOOOOOOO       SSSSSSSSSSSSSSS    IIIIIIIIII EEEEEEEEEEEEEEEEEEEEEE
                                                                      
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