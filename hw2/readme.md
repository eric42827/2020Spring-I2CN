Go-back-N
Timer跟著最小的
Timeout時把Sliding Window中沒有收到ack的全部重傳
重送後Reset Timer

Receiver為Cumulative Ack
如果收到out-of order的就丟掉,一樣回傳原本ㄉCumulative Ack