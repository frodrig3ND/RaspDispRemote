import platform
import os
import subprocess
import webbrowser


def get_valid_commands():
    return ['python', 'shell', 'website']


class command:
    """
    Desc: Class for commands to executed by host
    """
    def __init__(self, ctype=None, wd=None, target=None):
        command_classes = get_valid_commands()
        self.ctype = ctype
        if ctype in command_classes:
            self.wd = wd
            self.target = target
        else:
            # Should probably raise error
            return "Command type doesn't exist"

    def shell(self):
        """
        Desc: Run passed target as command in shell
        Input: Class object, uses target and working directory
        Output: resturns subprocess outcome or printed error
        """
        try:
            sp = subprocess.run(self.target,
                                cwd=self.wd, shell=True,
                                check=True, capture_output=True)
            sp.check_returncode()
            return sp
        except subprocess.CalledProcessError as e:
            print("Error:\nreturn code: ", e.returncode,
                  "\nOutput: ", e.stderr.decode("utf-8"))
        except FileNotFoundError as e:
            print(e)

    def python(self):
        """
        Desc: Run passed target file as input to python
        Input: Class object, uses target and working directory
        Output: resturns subprocess outcome or printed error
        """
        path = self.wd

        # Check to see what system is being used and serch for
        # env folder at root to use
        hasFile = os.path.isfile(path+'/env')
        if hasFile:
            env_path = self.wd+'/env'
            if platform.system() == 'Windows':
                python_path = env_path+'/Scripts/python.exe {}'
            elif platform.system() == 'Linux':
                python_path = env_path+'/bin/python {}'
        else:
            python_path = 'python {}'
            try:
                sp = subprocess.run(python_path.format(self.target),
                                    cwd=self.wd,
                                    check=True, capture_output=True)
                sp.check_returncode()
                return sp
            except subprocess.CalledProcessError as e:
                print("Error:\nreturn code: ", e.returncode,
                      "\nOutput: ", e.stderr.decode("utf-8"))
            except FileNotFoundError as e:
                print(e)

    def website(self):
        print(self.target)
        try:
            if platform.system() == "Windows":
                brw = webbrowser.get()
                brw.open_new_tab(self.target)
            # This gets hacky, since im running this from systemd
            # we have to deal with no x display and no root running
            # on chromium, which makes sense. So we don't use
            # webbrowser but instead subprocess
            elif platform.system() == "Linux":
                command = "sudo -u pi /usr/bin/chromium {}"
                print('Linux attempt')
                try:
                    sp = subprocess.call(['sh', '/home/pi/TestScript/test_webbrowser.sh'])
                    sp.check_returncode()
                except subprocess.CalledProcessError as e:
                    print("Error:\nreturn code: ", e.returncode,
                          "\nOutput: ", e.stderr.decode("utf-8"))
                except FileNotFoundError as e:
                    print(e)
            else:
                brw = webbrowser.get()
                brw.open_new_tab(self.target, 1)
        except Exception as e:
            raise e
