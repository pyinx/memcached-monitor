#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import memcache 
import time
import os
import sys

title='''
author:      netcat
des:         memcached monitor
mail:        admin@itsir.org
'''

s=5
us='↑'
ds='↓'
es='='
host=('192.168.0.1:11211','192.168.0.2:11211','192.168.0.3:11211')
d={}
for h in host:
	#d[host]=[hit,get,write_rate,read_rate]
	d[h]=[0,0,0,0]

d1={}
for h in host:
	#d1[host]=[hit,usage,conn,write_rate,read_rate]
	d1[h]=[0,0,0,0,0]
try:
	while True:
		os.system('clear')
		print title
		print '\thost\t\tstate\thit%\t\tusage%\t\tconn\twrite/s\t\tread/s\n'
		for h in host:
			mc=memcache.Client([h],debug=0)
			stat=mc.get_stats()
			if stat==[]:
				state='down'
				get=0
				hit=0
				miss=0
				rate=0
				write_rate=0
				read_rate=0
				conn=0
				usage=0
			else:
				state='up'
				cur_get=int(stat[0][1]['cmd_get'])
				if d[h][1] == 0:
					get=0
				else:
					get=cur_get-d[h][1]
				cur_hit=int(stat[0][1]['get_hits'])
				if d[h][0] == 0:
					hit=0
				else:
					hit=cur_hit-d[h][0]
				miss=int(stat[0][1]['get_misses'])
				write_total=int(stat[0][1]['bytes_written'])
				read_total=int(stat[0][1]['bytes_read'])
				conn=int(stat[0][1]['curr_connections'])
				bytes_max=int(stat[0][1]['limit_maxbytes'])
				bytes=int(stat[0][1]['bytes'])
				usage=round(bytes/bytes_max*100,2)			
	
				if get==0:
					rate=0
				else:
					rate=hit/get*100

				if d[h][2:]==[0,0]:
					write_rate=0
					read_rate=0
				else:
					write_rate=(write_total - d[h][2])/s	
					read_rate=(read_total - d[h][3])/s
					
					if write_rate > 1024*1024*1024:
						write_rate=str(round(write_rate/(1024*1024*1024),2))+'G'
					elif write_rate > 1024*1024:
						write_rate=str(round(write_rate/(1024*1024),2))+'M'
					elif write_rate > 1024:
						write_rate=str(round(write_rate/1024,2))+'K'
					else:
						write_rate=str(write_rate)

					if read_rate > 1024*1024*1024:
                                                read_rate=str(round(read_rate/(1024*1024*1024),2))+'G'
                                        elif read_rate > 1024*1024:
                                                read_rate=str(round(read_rate/(1024*1024),2))+'M'
                                        elif read_rate > 1024:
                                                read_rate=str(round(read_rate/1024,2))+'K'
                                        else:
                                                read_rate=str(read_rate)
				
                                if rate > d1[h][0]:
                                        r_s=us
                                elif rate < d1[h][0]:
                                        r_s=ds
                                else:
                                        r_s=es
                                if usage > d1[h][1]:
                                        u_s=us
                                elif usage < d1[h][1]:
                                        u_s=ds
                                else:
                                        u_s=es
                                if conn > d1[h][2]:
                                        c_s=us
                                elif conn < d1[h][2]:
                                        c_s=ds
                                else:
                                        c_s=es
                                if write_rate > d1[h][3]:
                                        w_s=us
                                elif write_rate < d1[h][3]:
                                        w_s=ds
                                else:
                                        w_s=es
                                if read_rate > d1[h][4]:
                                        R_s=us
                                elif read_rate < d1[h][4]:
                                        R_s=ds
                                else:
                                        R_s=es

				d[h]=[cur_hit,cur_get,write_total,read_total]
				d1[h]=[rate,usage,conn,write_rate,read_rate]
			print '%16s\t%s\t%05.2f%% %s\t%05.2f%% %s\t%d %s\t%7s %s\t%7s %s'%(h,state,rate,r_s,usage,u_s,conn,c_s,write_rate,w_s,read_rate,R_s)
		print '\n(ctrl-c to quit.)'
		time.sleep(s)
except KeyboardInterrupt:
	sys.exit()
