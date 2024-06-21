# HyperDtct: Hypervisor-Based Ransomware Detection
This repository is part of a bachelor's thesis on the detection of ransomware using hypervisor-based introspection and introduces *HyperDtct*, a wrapper for the debugger HyperDbg.

This repository contains the code for the controller and the client machine. The following image illustrates the architecture of *HyperDtct* considered during implementation:

![Architecture](/assets/Implementation.png)

Additionally, the collected logs and the considered samples are also included in this repository. 
This repository contains ransomware samples. Please handle them with care and do not execute them on a productive system.

# Setup Client
The client is a Windows machine, serving as the sandbox for the monitored samples.
It uses HyperDbg to monitor the system calls of an executable and sends the data to the controller.
Two users are required: an administrator user and a standard user called *Client*. The followin steps are executed by the administrator user.

1. Clone this repository to the main drive:
```bash
    cd C:\
    git clone https://github.com/Cyber-Tracer/HyperDtct.git
```

2. Install HyperDbg and move the latest release’s directory to C:\HyperDtct\HyperDbg.
3. Download the latest release of EfiGuard, and set up a bootable loader thumb drive. Move EfiDSEFix.exe to C:\HyperDtct\client\System\EfiDSEFix.exe. Configure the BIOS to boot on the thumb drive first.
4. Configure autologon and startup task. Replace USERNAME and PASSWORD with the administrator user’s credentials.
```bash
    C:\HyperDtct\client\System\setup\configure_autologin.bat USERNAME PASSWORD
    C:\HyperDtct\client\System\setup\setup_logging_task.ps1 -username USERNAME
```
5. Store the credentials of the Client user using the following command:
```bash
    py C:\HyperDtct\client\System\runas.py store_creds
```
6. Disable the screen saver, standby mode, and Windows Defender:
```bash
    C:\HyperDtct\client\System\setup\setup_power_settings.ps1
    C:\HyperDtct\client\System\setup\disable_ms_defender.ps1
```
7. Populate the client with files for the ransomware to encrypt:
```bash
    py C:\HyperDtct\client\System\setup\download_govdocs.py 0 100 C:\Users\Client\Documents
```
8. Use 7-Zip to create a backup of these files to another drive:
```bash
    7z.exe a -mx1 D:\FileBackup\Documents.7z C:\Users\Client\Documents\
```
9. Configure access rights for the Client user:
```bash
    icacls C:\HyperDtct /deny Client:(F) /q
    icacls D:\ /deny Client:(F) /q
```
10. To start monitoring, reboot the system.

# Setup Controller
During the thesis, the controller was implemented on a ressource-constrained Ubuntu 22.04 machine, reporesented by a raspberry pi 3B+. However, the controller can be run on any Ubuntu system.
1. Clone this repository
2. Configure the network settings of the controller. The configuration can be changed, however, it must match the controller ip defined on the client.
```bash
    sudo HyperDtct/controller/setup/setup_network.sh
    sudo HyperDtct/controller/setup/setup_ufw.sh
```
3. To create the zipped files to be sent to the client, run the following:
```bash
    cd /home/logger/HyperDtct/controller
    mkdir -p input_zipped/V2
    cd input
    python3 to_zipped.py --directory V2/ --output_directory ../input_zipped/V2/
```
4. To start monitoring the client for the zipped samples, run the following:
```bash
    python3 start_server.py --input input_zipped/V2/ --log_dir /configured/output/dir
```

### Monitoring V1 - V3 Samples
The monitoring sessions for the samples considered in V2 to V3-1 are already configured in shell scripts corresponding to the version. To start monitoring, for example, V2, run the following:
```bash
    cd HyperDtct/controller
    ./V2.sh
```
These scripts were written to facilitate monitoring on the controller machine considered during the theses. Therefore, they mount an externam thumb drive, output the logs to it, and unmount it again. Also, start_server.py is run as the logger user. Therefore, these scripts may need to be adjusted to run on a different machine.
Aso consider, that in V1, the executables for LibreOffice need to be added to the input directory, as they are too large to be included in the repository. They can be found here: https://portableapps.com/apps/office/libreoffice_portable

# Detection
The main part of this work is contained within the directory `/controller/detection`. It contains the considered models and evaluations for the detection of the considered samples.
The required packages are listed in the `requirements.txt` file. To train the models, run `controller/detection/train_models.py`. The script supports the following arguments:
- *--version*: The version of the samples to be considered, 1 to 3.
- *--log_dir*: Directory where the logs for the different versions are stored. Points to `../logs`by default.
- *--output_dir*: Directory where the models are stored. Points to `./models/trained` by default.
