# ness6rest.py - a REST interface to Nessus 6

### Dependencies:

* Nessus 6.0.1
* Python 2.7+ or 3.3+
* requests module (install via pip)
* The dependencies can be satisfied via `pip install -r requirements.txt`

### Features:

* Logins

  ```python
  scan = nessrest.Scanner(url="https://nessusscanner:8834", login="username", password="password")

  creds = [credentials.Windows(username="administrator", password="foobar"),
           credentials.Windows(username="administrator", password="barfoo"),
           credentials.SSH(username="nessususer", password="foobar")]

  scan.policy_add_creds(credentials=creds)
  ```
* Build policies

  ```python
  scan.upload(upload_file="file.audit")
  scan._policy_add_audit(category="Windows", filename="file.audit")
  scan.policy_add(name="Scripted Scan", plugins="21156")
  ```

* Launch scans

  ```python
  scan.scan_add(targets="192.168.0.1")
  scan.scan_run()
  ```

* Parse scan results

  ```python
  scan.scan_results()
  ```

* Download KB for target

  ```python
  kbs = scan.download_kbs()

  for hostname in kbs.keys():
      f = open(hostname, "w")
      f.write(kbs[hostname])
      f.close()
  ```

* Output for ticketing/wiki format

### Feature Requests:

* Deleting of scan/schedule/policy
* Ability to change "tag" from CLI via config/CLI arg
* Enforce supported versions of Nessus

### Notes:
* Proxies are not supported, although transparent proxies should work... transparently

# nessrest - an example client

### Dependencies:
* argparse module (install via pip)

### Suggested installation:

* Find the path to your "site-packages" with: `python -c "import sys; print(sys.path)"`
* Symlink `ness6rest.py` in the Git repo in the "site-packages" or "dist-packages" directory.
* Test by issuing `import ness6rest` inside the Python interactive
  interperter.

### InsecureRequestWarning

If you're running Nessus with a self-signed certificate, and you wish to squelch the InsecureRequestWarnings that the requests library uses, you can add the following line after the import requests line in ness6rest.py:
`requests.packages.urllib3.disable_warnings()`

This will disable invalid cerficate warnings and should be used with caution.

### Configuration file:

* Copy `ness_rest.conf.example` to `ness_rest.conf` and configure for your scanner.
* There are several valid paths for the location of the config file(in order):
* The path passed from the CLI with `--config`
* A permanent config file is searched for in the following locations:
    * `$HOME/.ness_rest.conf`
    * `$HOME/.ness_rest/ness_rest.conf`
    * `/etc/ness_rest.conf`
    * `/etc/ness_rest/ness_rest.conf`
    * `$PWD/ness_rest.conf`

### Building modules:

* To build a package to install via `pip` or `easy_install`, execute:
    * `python setup.py sdist`
* The resulting build will be in `$PWD/dist/ness6rest-<version>.tar.gz`

### Changelog:
* 2014-10-31: Support added for Nessus 6.0.1
