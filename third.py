import fourth as dc
from threading import Thread

fun_dic = {"1001":dc.decode_1001, "1002":dc.decode_1002,"1003":dc.decode_1003,"1004":dc.decode_1004,
        "3001": dc.decode_3001, "3002":dc.decode_3002, "3003":dc.decode_3003, 
        "3004": dc.decode_3004, "3005":dc.decode_3005}
def process_data(con, data, debug):
    code = data[2:6]
    #disabling threading because it will create a two point listen for a single thread
    #t1 = Thread(target = fun_dic[code], args = ((con, data)))
    #t1.start()
    if debug:
        print(data)
    if(code in fun_dic.keys()):
    	fun_dic[code](con, data, dc.debug[3])
    else:
    	print("*****************************(o_o) function not in fun dic******************************")
    
