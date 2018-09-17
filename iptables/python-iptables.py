"""
  要求: 用python达到目的，模块网站：https://pypi.python.org/pypi/python-iptables/0.1.1
  细节: 100.241 		       8001，8080端口
        100.61            5601端口
        200.50,200.51     33066端口
        以上IP的端口需要开放给10.31，做个端口开放记录表
  举例：
        1、在tcp协议中，禁止192.168.10.31 访问本机（本机：192.168.200.xxx）
            本机操作命令：iptables -I INPUT -s 192.168.10.31 -p tcp --dport 1521 -j DROP
        2、在tcp协议中，允许192.168.10.31 访问本机的 3306 端口
            本机操作命令：iptables -I INPUT -s 192.168.10.31 -p tcp --dport 3306 -j ACCEPT
"""

###脚本，第一次修改（实现IP段拒绝访问）：
# vim deny.py
#!/usr/bin/python
import iptc

rule = iptc.Rule()
rule.protocol = "tcp"
match = iptc.Match(rule, "tcp")
match.dport = "22"
rule.add_match(match)
match = iptc.Match(rule, "iprange")
match.src_range = "172.17.0.10-172.17.0.20"
match.dst_range = "172.17.0.165"
rule.add_match(match)
rule.target = iptc.Target(rule, "DROP")
chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")
chain.insert_rule(rule)

###第二次修改（实现单个IP拒绝访问）：
# vim deny.py
rule = iptc.Rule()
rule.protocol = "tcp"
match = iptc.Match(rule, "tcp")
match.dport = "3306"
rule.src = '172.17.0.20'
rule.dst = '172.17.0.165'
rule.target = iptc.Target(rule, "DROP")
chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")
chain.insert_rule(rule)

##第三次修改(实现先关闭远程IP所有访问，在开通3306的端口)
#!/usr/bin/python
import iptc

rule2 = iptc.Rule()
rule2.protocol = "tcp"
match2 = iptc.Match(rule2, "tcp")
rule2.src = '172.17.0.20'
rule2.dst = '172.17.0.165'
rule2.target = iptc.Target(rule2, "DROP")
chain2 = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")
chain2.insert_rule(rule2)

rule = iptc.Rule()
rule.protocol = "tcp"
match = iptc.Match(rule, "tcp")
match.dport = "3306"
rule.src = '172.17.0.20'
rule.dst = '172.17.0.165'
rule.target = iptc.Target(rule, "ACCEPT")
chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")
chain.insert_rule(rule)


###第四次修改(达到要求)：
#!/usr/bin/python
import iptc

rule2 = iptc.Rule()
#rule2.protocol = "tcp"                            # # 协议如果需要all的话，去掉这段相关的就行了
#match2 = iptc.Match(rule2, "tcp")        # 协议如果需要all的话，去掉这段相关的就行了
#rule.add_match(match2)                        # 协议如果需要all的话，去掉这段相关的就行了
rule2.src = '172.17.0.162'
#rule2.dst = '172.17.0.165'                        # 不需要写目标地址，可以去掉
rule2.target = iptc.Target(rule2, "DROP")
chain2 = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")
chain2.insert_rule(rule2)


rule = iptc.Rule()
#rule.protocol = "tcp"                                # 协议如果需要all的话，去掉这段相关的就行了
#match = iptc.Match(rule, "tcp")               # 协议如果需要all的话，去掉这段相关的就行了
#rule.add_match(match)                            # 协议如果需要all的话，去掉这段相关的就行了
rule.src = "172.17.0.162"
#match = iptc.Match(rule, "iprange")        # 范围取值，如果不需要就去掉
#match.src_range = "172.17.0.162"             # 范围取值，如果不需要就去掉
#match.dst_range = "172.17.0.1-172.17.0.254"             # 范围取值，如果不需要就去掉
#rule.add_match(match)                              # # 范围取值，如果不需要就去掉
match = iptc.Match(rule, "state")
match.state = "RELATED,ESTABLISHED"
rule.add_match(match)
rule.target = iptc.Target(rule, "ACCEPT")
chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")
chain.insert_rule(rule)
