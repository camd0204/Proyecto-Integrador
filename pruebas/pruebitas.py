import subprocess
def show_network_diagram():
        try:
            last_line=last_run_script()
            command = ['sudo', 'vnx', '-f', last_line, '--show-map']
            print (command)
            # Run the Perl script
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            # Capture the standard output and standard error
            stdout, stderr, = process.communicate()
            # Check the return code
            return_code = process.returncode
            # Return the standard output, standard error, and return code
            return stdout, return_code,stderr
        except Exception as e:
            # Handle any exceptions that may occur
            return None, str(e), 1
def last_run_script():
        with open("/home/lab1/CAMD/Proyecto-Integrador/historic_scripts/history.txt", "r", encoding="utf-8") as txt_file:
            lines = txt_file.readlines()
            last_line = lines[-1]
            return last_line.strip()
        
stdout,ret,stderrr=show_network_diagram()
print(stdout,ret,stderrr)