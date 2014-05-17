import re
import subprocess

def ping(remote, count=5):
    try:
        # spawn subprocess with pipes
        ping = subprocess.Popen(["ping", "-n", "-c " + str(count), remote], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, error = ping.communicate()
        # if there was output
        if out:
            try:
                # read fields using regex!
                lost_perc = float(re.findall(r'received, (.*)\% p', out)[0])
                lost = int(round(count * lost_perc / 100.0))
                stats_s = re.findall(r'mdev = (.*) ms', out)[0]
                stats_s_parts = stats_s.split('/')
                minimum = float(stats_s_parts[0])
                average = float(stats_s_parts[1])
                maximum = float(stats_s_parts[2])

                # return stats
                return {
                    'min': minimum,
                    'max': maximum,
                    'avg': average,
                    'lost': lost
                }
            except Exception as e:
                print e
                return None
        else:
            return None
    except subprocess.CalledProcessError:
        return None