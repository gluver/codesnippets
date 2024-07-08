#Download page  link for following .debs from https://download.docker.com/linux/ubuntu/dists/bionic/pool/stable/arm64/
import requests
import re
from bs4 import BeautifulSoup
import wget
ARCH='arm64'
DISTRIB='bionic'
DRY_RUN=False
# URL to fetch the HTML page
url = f"https://download.docker.com/linux/ubuntu/dists/{DISTRIB}/pool/stable/{ARCH}"

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Find all the links in the HTML
links = soup.find_all("a")
hrefs = [link.get('herf') for link in links]
# Regular expressions to match the package names
package_patterns = [
    r"containerd\.io_(\d+\.\d+\.\d+)[~]?.*\.deb",
    r"docker-ce_(\d+\.\d+\.\d+)~.*\.deb",
    r"docker-ce-cli_(\d+\.\d+\.\d+)~.*\.deb",
    r"docker-buildx-plugin_(\d+\.\d+\.\d+)[~]?.*\.deb",
    r"docker-compose-plugin_(\d+\.\d+\.\d+)~.*\.deb",
]

# Dictionary to store the latest version of each package
latest_packages = {}

# Iterate over the links and find the latest version of each package
for link in links:
    href = link.get("href")
    for pattern in package_patterns:
        match = re.match(pattern, href)
        if match:
            package_name = pattern.split("_")[0]
            #remove the '.' and '-' from the version number
            version = match.group(1).replace(".","").replace("-","")
            if package_name not in latest_packages or (version > latest_packages[package_name]["version"]):
                latest_packages[package_name] = {
                    "version": version,
                    "arch": ARCH,
                    "href": href
                }

# Download the latest versions of the packages

for package_name, package_info in latest_packages.items():
    package_url = f"{url}/{package_info['href']}"
    if DRY_RUN:
        print(f"wget {package_url}")
    else:
        wget.download(package_url, package_info["href"])

# Install the downloaded packages
install_command = "sudo dpkg -i "
for package_name, package_info in latest_packages.items():
    package_file = package_info["href"]
    install_command += f"./{package_file} "

print("Run the following command to install the latest versions of the packages:")
print(install_command)
print('\n')
