import os
import sys
import re
import time
import ctypes
import subprocess
from bs4 import BeautifulSoup as bs
import datetime

try:
    from scode.util import *
except ImportError:
    subprocess.run(['python', '-m', 'pip', 'install', '--upgrade', 'scode'])
    from scode.util import *

from scode.selenium import *
from scode.paramiko import *

# ===============================================================================
#                               Definitions
# ===============================================================================

def command(ssh: paramiko.SSHClient, query: str, timeout: float = None):

    stdin, stdout, stderr = ssh.exec_command(query)
    
    if timeout:
        start_time = time.time()
    
    # Wait for the command to terminate  
    while not stdout.channel.exit_status_ready():
        time.sleep(.1)
        if timeout:
            latest_time = time.time()

            if latest_time - start_time > timeout:
                stdout_text = stdout.read().decode('utf-8').strip()
                err_text = stderr.read().decode('utf-8').strip()
                return stdout_text, err_text
    
    stdout_text = stdout.read().decode('utf-8').strip()
    err_text = stderr.read().decode('utf-8').strip()
    return stdout_text, err_text

def ssh_connect(hostname: str, username: str, password: str) -> paramiko.SSHClient:

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, port=22, username=username, password=password,timeout=3)

    return ssh

def err_logging(input_data, program_title=None, path='./error.txt'):
    '''
    Write error_log in 'error.txt'
    If raise error, Send telegram message
    '''
    import sys
    import os
    import re
    from datetime import datetime
    import requests
    try:
        import telegram as tel
    except:
        os.system('pip install python-telegram-bot')
    # Send result message
    telegram_send_message = ''
    error_str = ''

    if '__title__' in globals():
        telegram_send_message += f'??????????????? : {__title__}\n'
    else:
        if program_title == None:
            pwd = os.getcwd()
            program_title = pwd.split('\\')[-1]
            telegram_send_message += f'??????????????? : {program_title}\n'
        else:
            telegram_send_message += f'??????????????? : {program_title}\n'

    try:
        ip_check = requests.get('https://wkwk.kr/ip/')
        ip_address = ip_check.text
        ip_check.close()
    except:
        ip_address = 'None("https://wkwk.kr/ip/"??? ????????? ?????? ?????? ip??? ?????? ??? ??? ????????????.)'
    telegram_send_message += f'IP : {ip_address}\n'

    # Get now datetime
    now = datetime.now().strftime('%y-%m-%d %H:%M:%S')
    error_str += f'------------------------{now}------------------------\n'
    if not isinstance(input_data,(list,dict)):
        raise Exception('Input_data type error : "input_data" is not list and not dict')

    # if input_data is list
    if isinstance(input_data,list):
        for data_dict in input_data:
            for data_key, data_value in data_dict.items():
                error_str += f'{data_key} : {data_value}\n'
                telegram_send_message += f'{data_key} : {data_value}\n'
    # if input_data is dict
    elif isinstance(input_data,dict):
        for data_key, data_value in input_data.items():
            error_str += f'{data_key} : {data_value}\n'
            telegram_send_message += f'{data_key} : {data_value}\n'

    # Get error script
    error_flag = sys.exc_info()
    if isinstance(error_flag,tuple):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        prob_file = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        prob_line_num = exc_tb.tb_lineno
        err_class = re.search("'.*'",str(exc_type).split(' ')[1]).group()
        err_script = str(exc_obj)
    else:
        prob_file = 'None'
        prob_line_num = 'None'
        err_class = 'It is not Error'
        err_script = 'It is not Error'

    error_str += f'Problem_File : {prob_file}\n'
    error_str += f'Problem_Line_Number : {prob_line_num}\n'
    error_str += f'Error_Class : {err_class}\n'
    error_str += f'Error_Script : {err_script}\n'

    telegram_send_message += f'Error_Class : {err_class}\n'
    telegram_send_message += f'Error_Script : {err_script}\n'
    telegram_send_message += f'Problem_Line_Number : {prob_line_num}\n'

    # Write error_log
    try:
        with open(path,'a',encoding='cp949') as err_f:
            err_f.write(error_str)
    except UnicodeEncodeError:
        with open(path,'a',encoding='utf-8') as err_f:
            err_f.write(error_str)
def except_date(db_server,except_lst):
    remove_flag = False
    for except_server in except_lst :
        if except_server in db_server :
            remove_flag = True
            break
    return remove_flag

def run():

    debug = False
    output_file_path = 'output.txt'
    output2_file_path = 'output2.txt'
    error_file_path = 'error.txt'
    car_file_path = 'car_list.txt'
    ex_file_path = 'except_list.txt'

    try:
        car_lst = [x.strip() for x in open(car_file_path).read().splitlines()]
    except UnicodeDecodeError:
        try:
            car_lst = [x.strip() for x in open(car_file_path, encoding='cp949').read().splitlines()]
        except UnicodeDecodeError:
            car_lst = [x.strip() for x in open(car_file_path, encoding='utf-8').read().splitlines()]

    while '' in car_lst :
        car_lst.remove('')
    try:
        except_lst = [x.strip() for x in open(ex_file_path).read().splitlines()]
    except UnicodeDecodeError:
        try:
            except_lst = [x.strip() for x in open(ex_file_path, encoding='cp949').read().splitlines()]
        except UnicodeDecodeError:
            except_lst = [x.strip() for x in open(ex_file_path, encoding='utf-8').read().splitlines()]

    while '' in except_lst :
        except_lst.remove('')

    
    # Inintialize

    open(output_file_path, 'w').close()
    open(output2_file_path, 'w').close()
    open(error_file_path, 'w').close()
    len_car_lst = len(car_lst)

    if len_car_lst == 0 :
        print('car_list.txt ????????? ???????????? ?????? 1??? ?????? ???????????????.')
        sys.exit()
    
    start = time.time()

    # TODO: ????????????

    # >>>>>>>>>>>>>>>>>>>>>>>>>> DB??? ????????? ?????? ?????? ??????
    host = 'aaa.e-e.kr'
    user = 'root'
    password = 'xptmxm12'
    db = 'aws_admin'

    # >>>>>>>>>>>>>>>>>>>>>>>>>> DB?????? ?????? list data??? ?????????
    try :
        conn = ssh_connect(hostname=host,username=user,password=password)
        Select_sql = " SELECT server_name,server_ip,aws_name,use_flag FROM site_list WHERE category LIKE '%??????????????????%' OR category LIKE '%??????????????????%' OR category LIKE '%??????????????????%' OR category LIKE '%??????????????????%'ORDER BY server_name "
        query_stdout, query_stderr = execute_sql_query(conn, user, password, db, Select_sql)
    except paramiko.AuthenticationException :
        print(f'DB ?????? ????????? ??????????????????.')
        print(f'?????? ?????? ?????? - host : {host}, user : {user}, password : {password}, db : {db}')
        sys.exit()
    except Exception as e :
        print(f'Error ?????? : ???????????? ??????????????????. \n{e}')
        print(f'?????? ?????? ?????? - host : {host}, user : {user}, password : {password}, db : {db}')
        input_data = {'error' : e, 'reason' : 'plz check the information about DB'}
        err_logging(input_data)
        sys.exit()

    db_server_list = query_stdout.split('\n')[1:]
    DB_list = {}
    len_except_lst = len(except_lst)
    for db_server in db_server_list :
        if len_except_lst != 0 :
            remove_flag = except_date(db_server,except_lst)
            if remove_flag :
                continue
        server_name = db_server.split('\t')[0]
        server_ip = db_server.split('\t')[1]
        use_flag = db_server.split('\t')[3]
        
        if server_ip == '' :
            continue
        if use_flag == '0' :
            continue
        DB_list.update({server_ip : server_name})

    len_DB_list = len(DB_list)
    time.sleep(.1)
    print('=='*30)
    
    p = re.compile('[\d]{4}-[\d]{2}-[\d]{2}?')
    print(f"{'=='*20}???????????? ??????{'=='*20}")
    print(f'?????? ??? ?????? ?????? : {len_except_lst} ??? ?????????.')


    # >>>>>>>>>>>>>>>>>>>>>>>>>> ?????? ????????? ??????

    # DB_list = {'xxx.164.101.xxx' : 'aws101'}
    for idx,(host,server_name) in enumerate(DB_list.items(),start=1) :
        try :
            no_j_flag = False
            cur_time = datetime.datetime.now().strftime("%H:%M:%S")
            print(f'{cur_time} >> {idx} / {len_DB_list} ?????? ?????? ????????? ?????????????????????.\n ?????? ?????? : {server_name}\n ?????? ip : {host}')
            host = host
            user = 'root'
            password = 'password'
            try :
                conn = ssh_connect(hostname=host,username=user,password=password)
            except paramiko.BadAuthenticationType:
                raise ValueError('Bad authentication type.')
            except paramiko.AuthenticationException:
                raise ValueError('Authentication failed.')
            except TimeoutError :
                raise ValueError('Time out -connect failed.')
            except Exception as e :
                raise ValueError('unknown error - connect failed')






            # >>>>>>>>>>>>>>>>>>>>>>>>> j-landing ?????? ?????? ??????
        
            common_query = 'ls /home/users/common'
            stdout, stderr = command(ssh=conn, query=common_query)
            common_file_lst = stdout.split('\n')
            if debug : print(common_file_lst)

            if 'j-landing' not in common_file_lst :
                no_j_flag = True
            else :
                common_query = 'ls /home/users/common/j-landing'
                stdout, stderr = command(ssh=conn, query=common_query)
                landing_file_lst = stdout.split('\n')
                if debug : print(landing_file_lst)



        # >>>>>>>>>>>>>>>>>>>>>>>>>> ??? car ????????? ??????

            for file_name in car_lst :
                
                # >>>>>>>>>>>>>>>>>>>>>>>>>> J-landing ?????? ?????? ???

                if no_j_flag :
                    print(f"{file_name} >> 'j-landing ?????? ??????' ")
                    fwrite(output_file_path,f'{server_name}\t{host}\t{file_name}\t?????? ??????')
                    #?????? ?????? ??????
                    continue


                # >>>>>>>>>>>>>>>>>>>>>>>>>> car ?????? ?????? ???

                if file_name not in landing_file_lst :
                    print(f"{file_name} >> '{file_name} ????????? ???????????? ????????????.")
                    fwrite(output_file_path,f'{server_name}\t{host}\t{file_name}\t?????? ??????')
                    #?????? ?????? ??????
                    continue


                # >>>>>>>>>>>>>>>>>>>>>>>>>> ???????????? ?????? ?????? ??????

                car_folder_query = f'ls /home/users/common/j-landing/{file_name}'
                stdout, stderr = command(ssh=conn, query=car_folder_query)
                car_file_lst = stdout.split('\n')
                if debug : print(car_file_lst)

                # >>>>>>>>>>>>>>>>>>>>>>>>>> ???????????? ?????? ?????? ???

                if 'update' not in car_file_lst :
                    print(f"{file_name} >> '{file_name} ??? update ????????? ???????????? ????????????.")
                    fwrite(output_file_path,f'{server_name}\t{host}\t{file_name}\t?????? ??????')
                    #?????? ?????? ??????
                    continue


                # >>>>>>>>>>>>>>>>>>>>>>>>>> index.html ?????? ??????

                try :
                    query = f'cat /home/users/common/j-landing/{file_name}/update/index.html'
                    stdout, stderr = command(ssh=conn, query=query)

                    # >>>>>>>>>>>>>>>>>>>>>>>>>> index.html ?????? ???

                    if stdout == '' :
                        date = '?????? ??????'
                        input_data = {'seq' : idx,'server-name' : server_name, 'ip' : host, 'reason' : '????????? ????????? ???????????? ????????????.'}
                        err_logging(input_data)


                    # >>>>>>>>>>>>>>>>>>>>>>>>>> index.html ??????

                    else :
                        date = re.findall(p,stdout)
                        if date == [] :
                            date = '?????? ??????'
                        else :
                            date = date[0]

                        if debug : print(f'Date : {date}\nHTML : {stdout}')

                    

                    print(f'{file_name} >> ????????? ?????? : {date}')
                    fwrite(output_file_path,f'{server_name}\t{host}\t{file_name}\t{date}')
                    
                except Exception as e :
                    print(f'{file_name} >> Error')

        except Exception as e :
            print('????????? ????????? ?????? ???????????????..\n')
            input_data = {'seq' : idx,'server-name' : server_name, 'ip' : host, 'reason' : e}
            err_logging(input_data)
            print('=='*30)
            fwrite(output_file_path,f'{server_name}\t{host}\t????????????x')


        # >>>>>>>>>>>>>>>>>>>>>>>>>> ?????? ??????
            
        conn.close()
        time.sleep(.1)
        print('=='*30)

    sec = time.time() - start
    taking_time = str(datetime.timedelta(seconds=sec)).split(".")[0]
    print(f'???????????? : {taking_time}')

# ===============================================================================
#                            Program infomation
# ===============================================================================

__author__ = '?????????'
__requester__ = '????????? ??????'
__registration_date__ = '230111'
__latest_update_date__ = '230111'
__version__ = 'v1.00'
__title__ = '20230111_????????? wcar????????? ?????? ?????? ????????????'
__desc__ = '20230111_????????? wcar????????? ?????? ?????? ????????????'
__changeLog__ = {
    'v1.00': ['Initial Release.'],
}
version_lst = list(__changeLog__.keys())

full_version_log = '\n'
short_version_log = '\n'

for ver in __changeLog__:
    full_version_log += f'{ver}\n' + '\n'.join(['    - ' + x for x in __changeLog__[ver]]) + '\n'

if len(version_lst) > 5:
    short_version_log += '.\n.\n.\n'
    short_version_log += f'{version_lst[-2]}\n' + '\n'.join(['    - ' + x for x in __changeLog__[version_lst[-2]]]) + '\n'
    short_version_log += f'{version_lst[-1]}\n' + '\n'.join(['    - ' + x for x in __changeLog__[version_lst[-1]]]) + '\n'

# ===============================================================================
#                                 Main Code
# ===============================================================================

if __name__ == '__main__':

    ctypes.windll.kernel32.SetConsoleTitleW(f'{__title__} {__version__} ({__latest_update_date__})')

    sys.stdout.write(f'{__title__} {__version__} ({__latest_update_date__})\n')

    sys.stdout.write(f'{short_version_log if short_version_log.strip() else full_version_log}\n')

    run()
