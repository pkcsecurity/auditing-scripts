# Automated android decompilation

These scripts automate the process of downloading an APK from the Play store and decompile it, by combining gplaycli, dex2jar, and fernflower.

- `sh setup.sh`: run this to download the necessary packages
- `sh download-and-decompile.sh com.venmo`: to download venmo, which has the play store ID com.venmo (You can see this in its play store URL: https://play.google.com/store/apps/details?id=com.venmo)
