#!/usr/bin/python

import sys
import subprocess
import json
import logging
import optparse
import tempfile
import os
import MySQLdb
import commands

zabbix_sender = '/you/path/zabbix/bin/zabbix_sender'
zabbix_conf = '/you/path/zabbix/etc/zabbix_agentd.conf'
logging.basicConfig(filename='/data/logs/zabbix/mysql_zabbix.log', level=logging.WARNING, format='%(asctime)s %(levelname)s: %(message)s')

my_cnf_file="/data/scripts/zabbix/.my.cnf"

conn = MySQLdb.connect(read_default_file=my_cnf_file,charset='utf8')
cur1 = conn.cursor()
cur2 = conn.cursor()
cur1.execute('show global status;')
cur2.execute('show global variables;')
data1 = cur1.fetchall()
data2 = cur2.fetchall()
cur1.close()
cur2.close()
conn.close()
mystat1=dict(data1)
mystat2=dict(data2)

def mysql_status (tmpfile):
    result = {}
################### get Mysql Base data , 1 items
    result["Mysql.Status[Uptime]"]=mystat1.get('Uptime')
    result["Mysql.Status[version]"]=mystat2.get('version')
    result["Mysql.Status[port]"]=mystat2.get('port')
################### get Mysql Binary/Relay Logs data , 4 items
    result["Mysql.Status[Binlog_cache_disk_use]"]=mystat1.get('Binlog_cache_disk_use')
    result["Mysql.Status[Binlog_cache_use]"]=mystat1.get('Binlog_cache_use')
    
################### get Mysql Command Counts data ,15 items
    result["Mysql.Status[Com_delete]"]=mystat1.get('Com_delete')
    result["Mysql.Status[Com_delete_multi]"]=mystat1.get('Com_delete_multi')
    result["Mysql.Status[Com_do]"]=mystat1.get('Com_do')
    result["Mysql.Status[Com_commit]"]=mystat1.get('Com_commit')
    result["Mysql.Status[Com_begin]"]=mystat1.get('Com_begin')
    result["Mysql.Status[Com_insert]"]=mystat1.get('Com_insert')
    result["Mysql.Status[Com_insert_select]"]=mystat1.get('Com_insert_select')
    result["Mysql.Status[Com_load]"]=mystat1.get('Com_load')
    result["Mysql.Status[Com_replace]"]=mystat1.get('Com_replace')    
    result["Mysql.Status[Com_replace_select]"]=mystat1.get('Com_replace_select')
    result["Mysql.Status[Com_rollback]"]=mystat1.get('Com_rollback')
    result["Mysql.Status[Com_select]"]=mystat1.get('Com_select')
    result["Mysql.Status[Com_update]"]=mystat1.get('Com_update')
    result["Mysql.Status[Com_update_multi]"]=mystat1.get('Com_update_multi')
    result["Mysql.Status[Questions]"]=mystat1.get('Questions')

################### get Mysql Connections data, 7 items
    result["Mysql.Status[Aborted_clients]"]=mystat1.get('Aborted_clients')
    result["Mysql.Status[Aborted_connects]"]=mystat1.get('Aborted_connects')
    result["Mysql.Status[Threads_running]"]=mystat1.get('Threads_running')
    result["Mysql.Status[Threads_created]"]=mystat1.get('Threads_created')
    result["Mysql.Status[Threads_connected]"]=mystat1.get('Threads_connected')
    result["Mysql.Status[Threads_cached]"]=mystat1.get('Threads_cached')
    result["Mysql.Status[Connections]"]=mystat1.get('Connections')
    result["Mysql.Status[Max_used_connections]"]=mystat1.get('Max_used_connections')
    result["Mysql.Status[max_connections]"]=mystat2.get('max_connections')

################### get Mysql Files and Tables data, 4 items
    result["Mysql.Status[Open_tables]"]=mystat1.get('Open_tables')
    result["Mysql.Status[Open_files]"]=mystat1.get('Open_files')
    result["Mysql.Status[Opened_tables]"]=mystat1.get('Opened_tables')
    result["Mysql.Status[table_open_cache]"]=mystat2.get('table_open_cache')
    result["Mysql.Status[open_files_limit]"]=mystat2.get('open_files_limit')

################### get Mysql Handler data , 9 items
    result["Mysql.Status[Handler_delete]"]=mystat1.get('Handler_delete')
    result["Mysql.Status[Handler_read_first]"]=mystat1.get('Handler_read_first') 
    result["Mysql.Status[Handler_read_key]"]=mystat1.get('Handler_read_key')
    result["Mysql.Status[Handler_read_next]"]=mystat1.get('Handler_read_next')
    result["Mysql.Status[Handler_read_prev]"]=mystat1.get('Handler_read_prev')
    result["Mysql.Status[Handler_read_rnd]"]=mystat1.get('Handler_read_rnd')
    result["Mysql.Status[Handler_read_rnd_next]"]=mystat1.get('Handler_read_rnd_next')
    result["Mysql.Status[Handler_update]"]=mystat1.get('Handler_update')
    result["Mysql.Status[Handler_write]"]=mystat1.get('Handler_write')

################### get Mysql InnoDB Buffer Pool data, 6 items
    result["Mysql.Status[Innodb_buffer_pool_pages_data]"]=mystat1.get('Innodb_buffer_pool_pages_data')
    result["Mysql.Status[Innodb_buffer_pool_pages_free]"]=mystat1.get('Innodb_buffer_pool_pages_free')
    result["Mysql.Status[Innodb_buffer_pool_read_requests]"]=mystat1.get('Innodb_buffer_pool_read_requests')
    result["Mysql.Status[Innodb_buffer_pool_reads]"]=mystat1.get('Innodb_buffer_pool_reads')
    result["Mysql.Status[innodb_buffer_pool_size]"]=mystat2.get('innodb_buffer_pool_size')

################### get Mysql InnoDB Buffer Pool Activity data, 3 items
    result["Mysql.Status[Innodb_pages_created]"]=mystat1.get('Innodb_pages_created')
    result["Mysql.Status[Innodb_pages_read]"]=mystat1.get('Innodb_pages_read')
    result["Mysql.Status[Innodb_pages_written]"]=mystat1.get('Innodb_pages_written')
    
################### get Mysql InnoDB Row Lock Waits data, 1 item
    result["Mysql.Status[Innodb_row_lock_waits]"]=mystat1.get('Innodb_row_lock_waits')

################### get Mysql InnoDB Row Lock Time data, 1 item
    result["Mysql.Status[Innodb_row_lock_time]"]=mystat1.get('Innodb_row_lock_time')


################### get Mysql InnoDB Rows Operations data, 4 item
    result["Mysql.Status[Innodb_rows_deleted]"]=mystat1.get('Innodb_rows_deleted')
    result["Mysql.Status[Innodb_rows_inserted]"]=mystat1.get('Innodb_rows_inserted')
    result["Mysql.Status[Innodb_rows_read]"]=mystat1.get('Innodb_rows_read')
    result["Mysql.Status[Innodb_rows_updated]"]=mystat1.get('Innodb_rows_updated')

################### get Mysql Network Traffic data, 2 items
    result["Mysql.Status[Bytes_received]"]=mystat1.get('Bytes_received')
    result["Mysql.Status[Bytes_sent]"]=mystat1.get('Bytes_sent')

################### get Mysql Qcache data, 9 items
    result["Mysql.Status[Qcache_queries_in_cache]"]=mystat1.get('Qcache_queries_in_cache')
    result["Mysql.Status[Qcache_total_blocks]"]=mystat1.get('Qcache_total_blocks')
    result["Mysql.Status[Qcache_free_blocks]"]=mystat1.get('Qcache_free_blocks')
    result["Mysql.Status[Qcache_free_memory]"]=mystat1.get('Qcache_free_memory')
    result["Mysql.Status[Qcache_hits]"]=mystat1.get('Qcache_hits')
    result["Mysql.Status[Qcache_inserts]"]=mystat1.get('Qcache_inserts')
    result["Mysql.Status[Qcache_lowmem_prunes]"]=mystat1.get('Qcache_lowmem_prunes')
    result["Mysql.Status[Qcache_not_cached]"]=mystat1.get('Qcache_not_cached')
    result["Mysql.Status[query_cache_size]"]=mystat2.get('query_cache_size')
    result["Mysql.Status[query_cache_limit]"]=mystat2.get('query_cache_limit')
    result["Mysql.Status[query_cache_min_res_unit]"]=mystat2.get('query_cache_min_res_unit')

################### get Sorts data , 4 items
    result["Mysql.Status[Sort_merge_passes]"]=mystat1.get('Sort_merge_passes')
    result["Mysql.Status[Sort_range]"]=mystat1.get('Sort_range')
    result["Mysql.Status[Sort_rows]"]=mystat1.get('Sort_rows')
    result["Mysql.Status[Sort_scan]"]=mystat1.get('Sort_scan')

################### get Select Types ,5 items
    result["Mysql.Status[Select_full_join]"]=mystat1.get('Select_full_join')
    result["Mysql.Status[Select_full_range_join]"]=mystat1.get('Select_full_range_join')
    result["Mysql.Status[Select_range]"]=mystat1.get('Select_range')
    result["Mysql.Status[Select_range_check]"]=mystat1.get('Select_range_check')
    result["Mysql.Status[Select_scan]"]=mystat1.get('Select_scan')

################### get Table Locks ,4 items
    result["Mysql.Status[slow_launch_time]"]=mystat2.get('slow_launch_time')
    result["Mysql.Status[Slow_queries]"]=mystat1.get('Slow_queries')
    result["Mysql.Status[Table_locks_immediate]"]=mystat1.get('Table_locks_immediate')
    result["Mysql.Status[Table_locks_waited]"]=mystat1.get('Table_locks_waited')

################### get Temporary Objects ,3 items
    result["Mysql.Status[Created_tmp_disk_tables]"]=mystat1.get('Created_tmp_disk_tables')
    result["Mysql.Status[Created_tmp_files]"]=mystat1.get('Created_tmp_files')
    result["Mysql.Status[Created_tmp_tables]"]=mystat1.get('Created_tmp_tables')

################### get Transaction Handler ,4 items
    result["Mysql.Status[Handler_commit]"]=mystat1.get('Handler_commit')
    result["Mysql.Status[Handler_rollback]"]=mystat1.get('Handler_rollback')
    result["Mysql.Status[Handler_savepoint]"]=mystat1.get('Handler_savepoint')
    result["Mysql.Status[Handler_savepoint_rollback]"]=mystat1.get('Handler_savepoint_rollback')

################### get slave status data ,6 items
    result["Mysql.Status[Slave_open_temp_tables]"]=mystat1.get('Slave_open_temp_tables')
    result["Mysql.Status[Slave_running]"]=mystat1.get('Slave_running')
    result["Mysql.Status[Slave_retried_transactions]"]=mystat1.get('Slave_retried_transactions') 

################### get Mysql InnoDB I/O data ,4 items
    result["Mysql.Status[Innodb_data_reads]"]=mystat1.get('Innodb_data_reads')
    result["Mysql.Status[Innodb_data_writes]"]=mystat1.get('Innodb_data_writes')
    result["Mysql.Status[Innodb_data_fsyncs]"]=mystat1.get('Innodb_data_fsyncs')
    result["Mysql.Status[Innodb_log_writes]"]=mystat1.get('Innodb_log_writes')

################### get MyISAM Indexs data ,4 items
    result["Mysql.Status[Key_read_requests]"]=mystat1.get('Key_read_requests')
    result["Mysql.Status[Key_write_requests]"]=mystat1.get('Key_write_requests')
    result["Mysql.Status[Key_reads]"]=mystat1.get('Key_reads')
    result["Mysql.Status[Key_writes]"]=mystat1.get('Key_writes')

################### get MyISAM Key Cache data ,3 items
    result["Mysql.Status[key_buffer_size]"]=mystat2.get('key_buffer_size')
    result["Mysql.Status[Key_blocks_unused]"]=mystat1.get('Key_blocks_unused')
    result["Mysql.Status[Key_blocks_used]"]=mystat1.get('Key_blocks_used')

################### get Mysql Innodb Log File data, 1 item
    result["Mysql.Status[innodb_log_file_size]"]=mystat2.get('innodb_log_file_size')

################### get Mysql Innodb Lock Wait Timeout data, 1 item
    result["Mysql.Status[innodb_lock_wait_timeout]"]=mystat2.get('innodb_lock_wait_timeout')

################### get Mysql InnoDB Log data, 4 items
    result["Mysql.Status[innodb_log_buffer_size]"]=mystat2.get('innodb_log_buffer_size')
    result["Mysql.Status[Innodb_os_log_written]"]=mystat1.get('Innodb_os_log_written')

################### get Mysql InnoDB I/O Pending data, 9 items
    result["Mysql.Status[pending_normal_aio_reads]"]=commands.getoutput("""/you/path/mysql/bin/mysql --defaults-file="/data/scripts/zabbix/.my.cnf" -e "SHOW ENGINE INNODB STATUS\G;"  |grep "Pending normal aio reads"|awk -F' ' '{print $5}' """)
    result["Mysql.Status[pending_normal_aio_writes]"]=commands.getoutput("""/you/path/mysql/bin/mysql --defaults-file="/data/scripts/zabbix/.my.cnf" -e "SHOW ENGINE INNODB STATUS\G;"  |grep "aio writes"|awk -F' ' '{print $13}' """)
    result["Mysql.Status[pending_flushes(fsync)_log]"]=commands.getoutput("""/you/path/mysql/bin/mysql --defaults-file="/data/scripts/zabbix/.my.cnf" -e "SHOW ENGINE INNODB STATUS\G;"  |grep "Pending flushes (fsync) log"|awk -F' ' '{print $5}'|awk -F';' '{print $1}' """)
    result["Mysql.Status[pending_flushes_buffer_pool]"]=commands.getoutput("""/you/path/mysql/bin/mysql --defaults-file="/data/scripts/zabbix/.my.cnf" -e "SHOW ENGINE INNODB STATUS\G;"  |grep "Pending flushes (fsync) log"|awk -F' ' '{print $8}' """)
    result["Mysql.Status[pending_log_writes]"]=commands.getoutput("""/you/path/mysql/bin/mysql --defaults-file="/data/scripts/zabbix/.my.cnf" -e "SHOW ENGINE INNODB STATUS\G;"  |grep "pending log writes"|awk -F' ' '{print $1}' """)
    result["Mysql.Status[pending_ibuf_aio_reads]"]=commands.getoutput("""/you/path/mysql/bin/mysql --defaults-file="/data/scripts/zabbix/.my.cnf" -e "SHOW ENGINE INNODB STATUS\G;"  |grep "ibuf aio reads" |awk -F',' '{print $1}' |awk -F' ' '{print $4}' """)
    result["Mysql.Status[pending_chkp_writes]"]=commands.getoutput("""/you/path/mysql/bin/mysql --defaults-file="/data/scripts/zabbix/.my.cnf" -e "SHOW ENGINE INNODB STATUS\G;"  |grep 'pending chkp writes'|awk -F' ' '{print $5}' """)
    result["Mysql.Status[pending_aio_sync_ios]"]=commands.getoutput("""/you/path/mysql/bin/mysql --defaults-file="/data/scripts/zabbix/.my.cnf" -e "SHOW ENGINE INNODB STATUS\G;"  |grep 'sync i/o' |awk -F' ' '{print $NF}' """)
    result["Mysql.Status[pending_aio_log_ios]"]=commands.getoutput("""/you/path/mysql/bin/mysql --defaults-file="/data/scripts/zabbix/.my.cnf" -e "SHOW ENGINE INNODB STATUS\G;"  |grep 'sync i/o' |awk -F',' '{print $2}'|awk -F' ' '{print $NF}' """)
  
################### get Mysql Innodb  Insert Buffer data, 1 item
    result["Mysql.Status[ibuf_merges]"]=commands.getoutput("""/you/path/mysql/bin/mysql --defaults-file="/data/scripts/zabbix/.my.cnf" -e "SHOW ENGINE INNODB STATUS\G;"  |grep 'Ibuf'|awk -F',' '{print $4}'|awk -F' ' '{print $1}' """)

################### get Mysql InnoDB Memory Allocation , 2 items
    result["Mysql.Status[total_mem_alloc]"]=commands.getoutput("""/you/path/mysql/bin/mysql --defaults-file="/data/scripts/zabbix/.my.cnf" -e "SHOW ENGINE INNODB STATUS\G;"  |grep 'Total memory allocated'|awk -F';' '{print $1}' |awk -F' ' '{print $NF}' """)
    result["Mysql.Status[additional_mem_pool_alloc]"]=commands.getoutput("""/you/path/mysql/bin/mysql --defaults-file="/data/scripts/zabbix/.my.cnf" -e "SHOW ENGINE INNODB STATUS\G;"  |grep 'additional pool allocated'|awk -F';' '{print $2}' |awk -F' ' '{print $NF}' """)   

################### get Mysql InnoDB Semaphores , 3 items
    result["Mysql.Status[spin_waits]"]=commands.getoutput("""/you/path/mysql/bin/mysql --defaults-file="/data/scripts/zabbix/.my.cnf" -e "SHOW ENGINE INNODB STATUS\G;"  |grep 'Mutex' |awk -F',' '{print $1}'|awk -F' ' '{print $NF}' """)
    result["Mysql.Status[spin_rounds]"]=commands.getoutput("""/you/path/mysql/bin/mysql --defaults-file="/data/scripts/zabbix/.my.cnf" -e "SHOW ENGINE INNODB STATUS\G;"  |grep 'Mutex' |awk -F',' '{print $2}'|awk -F' ' '{print $NF}' """)
    result["Mysql.Status[os_waits]"]=commands.getoutput("""/you/path/mysql/bin/mysql --defaults-file="/data/scripts/zabbix/.my.cnf" -e "SHOW ENGINE INNODB STATUS\G;"  |grep 'Mutex' |awk -F',' '{print $3}'|awk -F' ' '{print $NF}' """)

    for key in result:
        value=result.get(key)
        tmpfile.write("- %s %s\n" % (key, value))
 
     
def send_data_to_zabbix(conf,tmpfile):
    args = zabbix_sender + ' -c {0} -i {1} -vv'
    return_code = 0
    process = subprocess.Popen(args.format(conf, tmpfile.name),shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out, err = process.communicate()
    logging.debug("Finished sending data")
    return_code = process.wait()
    logging.info("Found return code of " + str(return_code))
    if return_code != 0:
       logging.warning(out)
       logging.warning(err)
    else:
       logging.debug(err)
       logging.debug(out)
    return return_code
 
 
def main():
    return_code = 0
    rdatafile1 = tempfile.NamedTemporaryFile(delete=False)
    mysql_status(rdatafile1)
    rdatafile1.close()
    return_code = send_data_to_zabbix(zabbix_conf,rdatafile1)

#### os.unlink is used to remove a file
    os.unlink(rdatafile1.name)
    print return_code

if __name__ == "__main__":
    main()
