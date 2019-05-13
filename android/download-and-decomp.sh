APP_ID=$1
set -e
echo "Downloading $APP_ID..."
rm -r target/ 2>/dev/null || echo "No target directory, nothing to clean"
mkdir target
pushd target
gplaycli -d "$APP_ID" -c ../gplaycli.conf
d2j-dex2jar -f *.apk
java -jar ../fernflower.jar *.jar decomp/
popd
