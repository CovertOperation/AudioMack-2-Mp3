# AudioMack-2-Mp3
Downloading and converting mp3 from audiomack

# Install requirements

```
pip install selenium webdriver-manager requests ffmpeg-python python-dotenv
```


# Step 1: Download FFmpeg from Gyan.dev
Go to the FFmpeg Build Page on Gyan.dev.

Scroll down to the "FFmpeg Builds" section and find the "Release Builds" category.

Click on the "Windows Builds" link.

You'll see several options; for most users, you'll want to download the "ffmpeg-release-essentials.zip" (it contains essential libraries and codecs).

Find the section called "ffmpeg-release" and click the link for "essentials build" (typically named something like ffmpeg-release-essentials.zip).

Download the .zip file to your computer.




# Step 2: Extract the ZIP File
After downloading the ffmpeg-release-essentials.zip file, navigate to the location where you downloaded the file.

Right-click the downloaded ZIP file and select "Extract All" or use any unzip tool like WinRAR or 7-Zip to extract the contents.

Extract the contents to a folder, for example, C:\ffmpeg\.

After extracting, you should see a folder named ffmpeg-release-essentials, which contains subfolders like bin, doc, and presets.

Inside the extracted folder, go to the bin folder. This is where the FFmpeg executable files (ffmpeg.exe, ffprop.exe, etc.) are located. The path to the FFmpeg binaries might look like this:

```
C:\ffmpeg\ffmpeg-release-essentials\bin
```


# Step 3: Add FFmpeg to Your Windows Environment Variables
Now that you've downloaded and extracted FFmpeg, the next step is to add the FFmpeg bin folder to your system's environment variables so that FFmpeg can be run from the Command Prompt (and from other programs) without needing to specify the full path every time.

Open System Properties:

Press Win + X and select "System" from the menu.

In the System window, click on "Advanced system settings" on the left sidebar.

Environment Variables:

In the System Properties window, go to the Advanced tab and click on the "Environment Variables..." button at the bottom.

Edit the Path Variable:

In the Environment Variables window, scroll down to the "System variables" section and select the variable called Path, then click Edit.

Add New Path:

In the Edit Environment Variable window, click New.

Paste the full path to the bin directory you extracted earlier. For example, if you extracted FFmpeg to C:\ffmpeg, the bin directory path would be:

```
C:\ffmpeg\ffmpeg-release-essentials\bin
```

# Step 4: Verify FFmpeg is Accessible
To make sure that FFmpeg has been successfully added to the Path, follow these steps:

Open Command Prompt:

Press Win + R, type cmd, and press Enter. This will open the Command Prompt.

Check FFmpeg Version:

Type the following command and press Enter:

nginx
Copy
ffmpeg -version
If FFmpeg has been installed and added to the system path correctly, you should see output with the FFmpeg version information, something like this:

vbnet
Copy
ffmpeg version 5.0 Copyright (c) 2000-2023 the FFmpeg developers
built with gcc 10.x.x (GCC)
configuration: --prefix=/usr/local --disable-static --enable-shared ...
If you see this, that means FFmpeg is installed correctly and you can use it from anywhere on your computer.


# Step 5: Troubleshooting
If FFmpeg is not recognized, it’s likely that the path wasn't added properly. Here's what to check:

Check the Path: Ensure the path you added to the Path variable is correct, and it points to the bin folder that contains ffmpeg.exe. Double-check that there are no typos.

Restart your Computer: Sometimes, environment variable changes don't take effect immediately. Restart your computer to ensure that the new path is properly applied.

Test in New Command Prompt: If you still see issues, try opening a new Command Prompt window (after restarting your computer) and running the ffmpeg -version command again.
