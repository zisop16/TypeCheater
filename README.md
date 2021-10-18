
Have you ever wanted to impress your friends by getting large, insane typeracer scores? Now you can!

## Getting started

### For those inexeperienced with code or who do not wish to install Python
1. Create a project folder where all downloads will go

2. Download tpBOT.exe and chromedriver.exe from [Releases](https://github.com/zisop16/TypeCheater/releases)

Note: only download chromedriver.exe if you are using Chrome version 83. We highly recommend you check your Chrome version before you download chromedriver.exe. To do this, go to settings in chrome (in the top right, by clicking the ... button), navigate to "About Chrome," and then look for the first number in the version number (should be 83, 82, 81, etc.). If you have Chrome version 83, feel free to download chromedriver.exe from [Releases](https://github.com/zisop16/TypeCheater/releases). Otherwise, navigate to the [Chromedriver installation page](https://chromedriver.chromium.org/downloads) and download the version which matches with your Chrome version.

3. Place both chromedriver.exe and tpBOT.exe into your project folder
4. Download Tesseract-OCR-w64 [here](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.0-alpha.20200328.exe).

Note: if you need to install a 32-bit version of Tesseract, navigate [here](https://github.com/tesseract-ocr/tessdoc) to install it. Dwnloading a 32 bit version will require you to install it to a different path: `C:\Program Files (x86)\Tesseract-OCR`

5. Install tesseract by launching the download. Make sure to install it to the following path (if you are installing the 64-bit version): `C:\Program Files\Tesseract-OCR`. If you installed the 32-bit version, install to `C:\Program Files (x86)\Tesseract-OCR`

6. Setup is complete.

### For those experienced with code or have both Python and pip
Note: We highly recommend this method to run, as running a python file will be much faster than the exe.

1. Download the source code folder from [Releases](https://github.com/zisop16/TypeCheater/releases)

Note: only download chromedriver.exe if you are using Chrome version 83. We highly recommend you check your Chrome version before you download chromedriver.exe. To do this, go to settings in chrome (in the top right, by clicking the ... button), navigate to "About Chrome," and then look for the first number in the version number (should be 83, 82, 81, etc.). If you have Chrome version 83, feel free to download chromedriver.exe from [Releases](https://github.com/zisop16/TypeCheater/releases). Otherwise, navigate to the [Chromedriver installation page](https://chromedriver.chromium.org/downloads) and download the version which matches with your Chrome version.

2. Extract

3. Download Tesseract-OCR-w64 [here](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.0-alpha.20200328.exe).

Note: if you need to install a 32-bit version of Tesseract, navigate [here](https://github.com/tesseract-ocr/tessdoc) to install it. Dwnloading a 32 bit version will require you to install it to a different path: `C:\Program Files (x86)\Tesseract-OCR`

4. Install tesseract by launching the download. Make sure to install it to the following path (if you are installing the 64-bit version): `C:\Program Files\Tesseract-OCR`. If you installed the 32-bit version, install to `C:\Program Files (x86)\Tesseract-OCR`

5. Setup is complete.

## Usage

### For those inexeperienced with code or who do not wish to install Python
1. Open the project folder. It should contain chromedriver.exe and tpBOT.exe.
2. Run the project by double-clicking on tpBOT.exe. You may need to do this several times (it takes a while to run using this method) in order to give the bot network permissions.
3. The first successful time you run the project, it will create a config.txt in your folder. It should look something like this:
```
{
    "Username": "Bot",
    "Password": "",
    "Words Per Minute": 150,
    "Characters per key input": 5
}
```
4. Don't add anything (unless you know what you're doing and are making changes to tpBOT.py as well). All you should do in this file is change your username, password, desired words per minute, and characters per key input. Feel free to experiment around to see what all of these do. If you wish, you can play with a blank password (like in the example) if you don't have an account or wish to play as a guest.
5. Don't change any file names.
6. The second time you run (assuming config.txt has been set up correctly), the bot should function correctly, logging what's happening as it goes. Check your open applications, as tpBOT.exe should have opened chromedriver.exe, where you will be able to visually see what's happening. After the first race, the command line will prompt you to type in "Y" or "N" to continue towards solving the captcha.
7. THE BOT IS ABLE TO SOLVE CAPTCHAS, BUT ONLY EVERY ONCE IN A WHILE. Essentially, the bot will continue to retry solving captchas until
it gets one correct. After one captcha is solved (if you are playing on an account), you no longer need to verify your account again. Please be patient with captcha solving; you may need to run the bot several times before it will be able to successfully attempt the captcha.
8. That's all there is! Keep in mind that setting too high of a WPM (~550+) will cause the site to detect that you are botting. There is no harm if this happens, all it does is cause the bot to quit and make you run it again.

### For those experienced with code or have both Python and pip

1. Open the extracted folder with all the source code.
2. ONLY IF YOU HAVE PYTHON AND PIP, run [setup.bat](/setup.bat)
2. To run, either call in your command prompt `cd PATH_TO_EXTRACTED_FOLDER`, then `py tpBOT.py`
   OR simply run [run.bat](/run.bat)
3. The first time you run the project, it will create a config.txt in your folder. It should look something like this:
```
{
    "Username": "Bot",
    "Password": "",
    "Words Per Minute": 150,
    "Characters per key input": 5
}
```
4. Treat this as a .json; feel free to modify any definitions tto your liking. If you wish, you can play with a blank password (like in the example) if you don't have an account or wish to play as a guest.
5. The second time you run (assuming config.txt has been set up correctly), the bot should function correctly, logging what's happening as it goes. Check your open applications, as tpBOT.exe should have opened chromedriver.exe, where you will be able to visually see what's happening. After the first race, the command line will prompt you to type in "Y" or "N" to continue towards solving the captcha.
6. THE BOT IS ABLE TO SOLVE CAPTCHAS, BUT ONLY EVERY ONCE IN A WHILE. Essentially, the bot will continue to retry solving captchas until
it gets one correct. After one captcha is solved (if you are playing on an account), you no longer need to verify your account again. Please be patient with captcha solving; you may need to run the bot several times before it will be able to successfully attempt the captcha.
7. That's all there is! Keep in mind that setting too high of a WPM (~550+) will cause the site to detect that you are botting. There is no harm if this happens, all it does is cause the bot to quit and make you run it again.

## License

This project is licensed under the GNU v3 license. See [LICENSE](LICENSE) for more details.

