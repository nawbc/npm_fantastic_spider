### 安装
   - python3
   - redis 
   - mysql
   - Scrapy==1.7.4 
   - selenium==3.141.0
   - PyMySQL==0.9.3
   - requests==2.12.4
   - redis==3.3.11
   - beautifulsoup4==4.8.1


scrapy 不可用 有时间再整

------
### 使用
1. 更改 ./npm_fantastic_no_scrapy/npm_fantastic.py 中的用户密码
2. 启动  `./start.sh -a`
   <br />
   默认开启 挑选优质库
   ```
     -m [number][0-100]         维护度
     -q [number]                质量
     -p [number]                受欢迎度
     -a                         抓取全部库
     --proxy                    代理      
   ```
   
3. `python3 ./npm_fantastic_no_scrapy/free_ip_proxy/start.py 抓取高匿代理ip 需要redis` 

### 原理
dfs 遍历关键词

