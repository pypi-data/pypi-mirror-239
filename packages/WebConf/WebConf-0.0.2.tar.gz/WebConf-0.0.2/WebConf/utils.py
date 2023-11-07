import argparse
import datetime
import subprocess



def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def execute_command(cmdstring):
    """
    :return 执行结果code，执行过程命令，开始时间
    """
    start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"start execute_command {cmdstring}", flush=True)
    returncode, result = subprocess.getstatusoutput(cmdstring)
    print(f"end execute_command {cmdstring}", flush=True)

    return returncode, result, start_time
