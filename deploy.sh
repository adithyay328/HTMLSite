python3 sitemapGen.py
./syncDir.sh
ssh root@webserver.wg.adiy.io 'cd /root/HTMLSite && ./updateDeploymentFiles.sh'
