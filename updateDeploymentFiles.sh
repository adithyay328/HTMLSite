# Run this on a machine running ubuntu to
# place the deployment files in the correct
# directory on the server for nginx
# to host them

# First, delete any existing files
# in the deployment directory
DEPLOYMENT_DIR="/var/www/html/adiy.io"

# Delete the existing files
rm -rf $DEPLOYMENT_DIR

# Make the directory
mkdir $DEPLOYMENT_DIR

# Copy the files over
cp -r serve/** $DEPLOYMENT_DIR

# Also, push our nginx config
# to the server
NGINX_CONFG_FILE="/etc/nginx/conf.d/adiyio.conf"

# Delete the existing config
rm -rf $NGINX_CONFG_FILE

# Copy the new config
cp adiyio.conf $NGINX_CONFG_FILE

# Restart nginx
nginx -s reload
