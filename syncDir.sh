# Syncs this dir to the server to make
# site available

rsync -r --delete ../HTMLSite root@webserver.wg.adiy.io:~/
