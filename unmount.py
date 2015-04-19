import subprocess

subprocess.Popen(["fusermount", "-u", "cache/node1"])
subprocess.Popen(["fusermount", "-u", "cache/node2"])
subprocess.Popen(["fusermount", "-u", "cache/node3"])
subprocess.Popen(["fusermount", "-u", "cache/node4"])
subprocess.Popen(["fusermount", "-u", "cache/node5"])
#subprocess.Popen(["fusermount", "-u", "cache/node4"])


